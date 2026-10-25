"""Convenience entrypoint: fetch data if missing, then start the app."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from safeschool.config import get_settings
from safeschool.data_loader import ingest
from safeschool.app import app

settings = get_settings()

if not settings.db_path.exists():
    print("Database not found – downloading data from dane.gov.pl…")
    n = ingest(settings.db_path, settings.data_dir, settings.dane_gov_dataset_id)
    print(f"Ingested {n} records.")

if __name__ == "__main__":
    app.run(host=settings.host, port=settings.port, debug=settings.debug)
