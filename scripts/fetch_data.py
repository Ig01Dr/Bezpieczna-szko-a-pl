"""Download data from dane.gov.pl and build the SQLite database."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from safeschool.config import get_settings
from safeschool.data_loader import ingest

if __name__ == "__main__":
    s = get_settings()
    n = ingest(s.db_path, s.data_dir, s.dane_gov_dataset_id)
    print(f"Ingested {n} records into {s.db_path}")
