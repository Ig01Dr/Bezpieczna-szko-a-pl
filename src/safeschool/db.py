"""SQLite storage layer for accident records."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterable

SCHEMA = """
CREATE TABLE IF NOT EXISTS accidents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year TEXT NOT NULL,
    wojewodztwo TEXT NOT NULL,
    powiat TEXT,
    gmina TEXT,
    typ_podmiotu TEXT,
    rodzaj_wypadku TEXT,
    przyczyna TEXT,
    miejsce TEXT,
    zajecia TEXT,
    liczba INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX IF NOT EXISTS idx_acc_year ON accidents(year);
CREATE INDEX IF NOT EXISTS idx_acc_woj ON accidents(wojewodztwo);
CREATE INDEX IF NOT EXISTS idx_acc_typ ON accidents(typ_podmiotu);
CREATE INDEX IF NOT EXISTS idx_acc_przyczyna ON accidents(przyczyna);
CREATE INDEX IF NOT EXISTS idx_acc_miejsce ON accidents(miejsce);
"""


def connect(db_path: Path) -> sqlite3.Connection:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: Path) -> None:
    with connect(db_path) as conn:
        conn.executescript(SCHEMA)
        conn.commit()


def insert_rows(db_path: Path, rows: Iterable[dict]) -> int:
    sql = """INSERT INTO accidents
        (year, wojewodztwo, powiat, gmina, typ_podmiotu, rodzaj_wypadku,
         przyczyna, miejsce, zajecia, liczba)
        VALUES (:year, :wojewodztwo, :powiat, :gmina, :typ_podmiotu,
                :rodzaj_wypadku, :przyczyna, :miejsce, :zajecia, :liczba)"""
    with connect(db_path) as conn:
        cur = conn.executemany(sql, rows)
        conn.commit()
        return cur.rowcount


def distinct(db_path: Path, column: str) -> list[str]:
    allowed = {
        "year", "wojewodztwo", "powiat", "gmina", "typ_podmiotu",
        "rodzaj_wypadku", "przyczyna", "miejsce", "zajecia",
    }
    if column not in allowed:
        raise ValueError(f"column not allowed: {column}")
    with connect(db_path) as conn:
        rows = conn.execute(
            f"SELECT DISTINCT {column} FROM accidents WHERE {column} IS NOT NULL ORDER BY {column}"
        ).fetchall()
    return [r[0] for r in rows if r[0] is not None]


def totals(db_path: Path) -> dict:
    with connect(db_path) as conn:
        total = conn.execute("SELECT COALESCE(SUM(liczba),0) FROM accidents").fetchone()[0]
        rows = conn.execute("SELECT COUNT(*) FROM accidents").fetchone()[0]
        years = [r[0] for r in conn.execute("SELECT DISTINCT year FROM accidents ORDER BY year").fetchall()]
    return {"total_accidents": int(total), "records": int(rows), "years": years}


def aggregate_by(db_path: Path, column: str, filters: dict | None = None, limit: int = 20) -> list[dict]:
    allowed = {
        "wojewodztwo", "typ_podmiotu", "rodzaj_wypadku", "przyczyna",
        "miejsce", "zajecia", "year", "powiat", "gmina",
    }
    if column not in allowed:
        raise ValueError(f"column not allowed: {column}")
    where, params = _build_where(filters or {})
    sql = f"""SELECT {column} AS label, COALESCE(SUM(liczba),0) AS value
              FROM accidents {where}
              GROUP BY {column}
              ORDER BY value DESC
              LIMIT ?"""
    params = params + [limit]
    with connect(db_path) as conn:
        rows = conn.execute(sql, params).fetchall()
    return [{"label": r["label"], "value": int(r["value"])} for r in rows]


def trend_by_year(db_path: Path, filters: dict | None = None) -> list[dict]:
    where, params = _build_where(filters or {})
    sql = f"""SELECT year AS label, COALESCE(SUM(liczba),0) AS value
              FROM accidents {where}
              GROUP BY year ORDER BY year"""
    with connect(db_path) as conn:
        rows = conn.execute(sql, params).fetchall()
    return [{"label": r["label"], "value": int(r["value"])} for r in rows]


def search(db_path: Path, filters: dict | None = None, limit: int = 50, offset: int = 0) -> tuple[list[dict], int]:
    where, params = _build_where(filters or {})
    count_sql = f"SELECT COUNT(*) FROM accidents {where}"
    data_sql = f"""SELECT year, wojewodztwo, powiat, gmina, typ_podmiotu,
                          rodzaj_wypadku, przyczyna, miejsce, zajecia, liczba
                   FROM accidents {where}
                   ORDER BY liczba DESC, year DESC
                   LIMIT ? OFFSET ?"""
    with connect(db_path) as conn:
        total = conn.execute(count_sql, params).fetchone()[0]
        rows = conn.execute(data_sql, params + [limit, offset]).fetchall()
    return [dict(r) for r in rows], int(total)


def _build_where(filters: dict) -> tuple[str, list]:
    clauses = []
    params: list = []
    mapping = {
        "year": "year",
        "wojewodztwo": "wojewodztwo",
        "powiat": "powiat",
        "gmina": "gmina",
        "typ_podmiotu": "typ_podmiotu",
        "przyczyna": "przyczyna",
        "miejsce": "miejsce",
        "zajecia": "zajecia",
        "rodzaj_wypadku": "rodzaj_wypadku",
    }
    for key, col in mapping.items():
        val = filters.get(key)
        if val:
            clauses.append(f"{col} = ?")
            params.append(val)
    if clauses:
        return "WHERE " + " AND ".join(clauses), params
    return "", params
