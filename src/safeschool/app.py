"""Flask web application."""

from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path

from flask import Flask, jsonify, render_template, request

# ensure src on path when run as script
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from safeschool.config import get_settings
from safeschool import db

settings = get_settings()

app = Flask(
    __name__,
    template_folder=str(Path(__file__).parent / "templates"),
    static_folder=str(Path(__file__).parent / "static"),
)
app.config["JSON_AS_ASCII"] = False

logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO))


def _filters_from_args() -> dict:
    keys = ["year", "wojewodztwo", "powiat", "gmina", "typ_podmiotu",
            "przyczyna", "miejsce", "zajecia", "rodzaj_wypadku"]
    out = {}
    for k in keys:
        v = request.args.get(k)
        if v:
            out[k] = v
    return out


@app.route("/")
def index():
    db_path = settings.db_path
    totals = db.totals(db_path) if db_path.exists() else {"total_accidents": 0, "records": 0, "years": []}
    filters = _filters_from_args()
    by_woj = db.aggregate_by(db_path, "wojewodztwo", filters, 16) if db_path.exists() else []
    by_typ = db.aggregate_by(db_path, "typ_podmiotu", filters, 12) if db_path.exists() else []
    by_przyczyna = db.aggregate_by(db_path, "przyczyna", filters, 10) if db_path.exists() else []
    by_miejsce = db.aggregate_by(db_path, "miejsce", filters, 10) if db_path.exists() else []
    trend = db.trend_by_year(db_path, filters) if db_path.exists() else []
    filter_options = {}
    for col in ["year", "wojewodztwo", "typ_podmiotu", "przyczyna", "miejsce", "zajecia"]:
        try:
            filter_options[col] = db.distinct(db_path, col) if db_path.exists() else []
        except Exception:
            filter_options[col] = []
    return render_template(
        "index.html",
        totals=totals,
        filters=filters,
        by_woj=by_woj,
        by_typ=by_typ,
        by_przyczyna=by_przyczyna,
        by_miejsce=by_miejsce,
        trend=trend,
        filter_options=filter_options,
    )


@app.route("/search")
def search_page():
    db_path = settings.db_path
    filters = _filters_from_args()
    limit = min(int(request.args.get("limit", 50)), 200)
    offset = int(request.args.get("offset", 0))
    rows, total = db.search(db_path, filters, limit, offset) if db_path.exists() else ([], 0)
    filter_options = {}
    for col in ["year", "wojewodztwo", "typ_podmiotu", "przyczyna", "miejsce", "zajecia"]:
        try:
            filter_options[col] = db.distinct(db_path, col) if db_path.exists() else []
        except Exception:
            filter_options[col] = []
    from urllib.parse import urlencode
    base_qs = urlencode(filters)
    return render_template(
        "search.html",
        rows=rows,
        total=total,
        limit=limit,
        offset=offset,
        filters=filters,
        filter_options=filter_options,
        base_qs=base_qs,
    )


@app.route("/api/aggregate")
def api_aggregate():
    db_path = settings.db_path
    by = request.args.get("by", "wojewodztwo")
    filters = _filters_from_args()
    limit = int(request.args.get("limit", 20))
    data = db.aggregate_by(db_path, by, filters, limit) if db_path.exists() else []
    return jsonify(data)


@app.route("/api/trend")
def api_trend():
    db_path = settings.db_path
    filters = _filters_from_args()
    return jsonify(db.trend_by_year(db_path, filters) if db_path.exists() else [])


@app.route("/health")
def health():
    return jsonify({"status": "ok", "db_exists": settings.db_path.exists()})


if __name__ == "__main__":
    app.run(host=settings.host, port=settings.port, debug=settings.debug)
