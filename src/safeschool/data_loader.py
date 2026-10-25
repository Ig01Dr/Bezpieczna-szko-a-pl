"""Download and ingest school-accident data from dane.gov.pl."""

from __future__ import annotations

import csv
import io
import re
import urllib.request
from pathlib import Path

import pandas as pd

DANE_API = "https://api.dane.gov.pl/1.4"


def list_resources(dataset_id: int) -> list[dict]:
    url = f"{DANE_API}/datasets/{dataset_id}/resources?per_page=100"
    with urllib.request.urlopen(url) as resp:
        data = __import__("json").loads(resp.read())
    return data.get("data", [])


def _csv_url(resource: dict) -> str | None:
    for f in resource["attributes"].get("files", []):
        if f.get("format") == "csv":
            return f["download_url"]
    return None


def _year_from_title(title: str) -> str:
    m = re.search(r"(\d{4}/\d{4})", title)
    if m:
        return m.group(1)
    m = re.search(r"(\d{4})", title)
    return m.group(1) if m else "unknown"


def download_all(data_dir: Path, dataset_id: int = 40) -> list[tuple[str, Path]]:
    """Download every yearly CSV and return list of (year_label, path)."""
    data_dir.mkdir(parents=True, exist_ok=True)
    out: list[tuple[str, Path]] = []
    for res in list_resources(dataset_id):
        title = res["attributes"].get("title", "")
        if "w roku szkolnym" not in title:
            continue
        url = _csv_url(res)
        if not url:
            continue
        year = _year_from_title(title)
        dest = data_dir / f"accidents_{year.replace('/', '-')}.csv"
        if not dest.exists():
            urllib.request.urlretrieve(url, dest)
        out.append((year, dest))
    out.sort(key=lambda x: x[0])
    return out


COLUMN_MAP = {
    "wojewodztwo": "wojewodztwo",
    "powiat": "powiat",
    "gmina": "gmina",
    "typpodmiotu": "typ_podmiotu",
    "rodzajwypadku": "rodzaj_wypadku",
    "przyczynawypadku": "przyczyna",
    "miejscewypadku": "miejsce",
    "rodzajzajec": "zajecia",
    "liczbawypadkow": "liczba",
}


def _normalize(name: str) -> str:
    return "".join(ch for ch in name.lower() if ch.isalnum())


def load_csv(path: Path, year: str) -> list[dict]:
    df = pd.read_csv(path, encoding="utf-8-sig")
    # map source columns to canonical names via normalized keys
    col_lookup = {_normalize(c): c for c in df.columns}
    rows: list[dict] = []
    for _, r in df.iterrows():
        row = {"year": year}
        for norm, dst in COLUMN_MAP.items():
            src = col_lookup.get(norm)
            if src is None:
                val = None
            else:
                val = r.get(src)
            if pd.isna(val):
                val = None
            row[dst] = val
        try:
            row["liczba"] = int(row["liczba"] or 0)
        except (TypeError, ValueError):
            row["liczba"] = 0
        # clean string fields
        for k in ("wojewodztwo", "powiat", "gmina", "typ_podmiotu", "rodzaj_wypadku",
                  "przyczyna", "miejsce", "zajecia"):
            if row.get(k) is not None:
                row[k] = str(row[k]).strip()
        rows.append(row)
    return rows


def ingest(db_path: Path, data_dir: Path, dataset_id: int = 40) -> int:
    from .db import init_db, insert_rows

    init_db(db_path)
    # clear existing
    import sqlite3
    with sqlite3.connect(str(db_path)) as conn:
        conn.execute("DELETE FROM accidents")
        conn.commit()

    total = 0
    for year, path in download_all(data_dir, dataset_id):
        rows = load_csv(path, year)
        total += insert_rows(db_path, rows)
    return total
