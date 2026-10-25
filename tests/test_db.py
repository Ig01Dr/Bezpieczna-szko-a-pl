"""Tests for the storage layer."""

import sqlite3
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from safeschool import db


class TestDb(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.db = Path(self.tmp) / "t.db"
        db.init_db(self.db)
        rows = [
            {"year": "2018/2019", "wojewodztwo": "MAZOWIECKIE", "powiat": "warszawski",
             "gmina": "Warszawa", "typ_podmiotu": "Szkoła podstawowa", "rodzaj_wypadku": "upadek",
             "przyczyna": "nieuwaga ucznia", "miejsce": "korytarz", "zajecia": "przerwa", "liczba": 3},
            {"year": "2019/2020", "wojewodztwo": "MAZOWIECKIE", "powiat": "warszawski",
             "gmina": "Warszawa", "typ_podmiotu": "Przedszkole", "rodzaj_wypadku": "uderzenie",
             "przyczyna": "poślizgnięcie", "miejsce": "plac zabaw", "zajecia": "zabawa", "liczba": 2},
            {"year": "2018/2019", "wojewodztwo": "ŚLĄSKIE", "powiat": "katowicki",
             "gmina": "Katowice", "typ_podmiotu": "Szkoła podstawowa", "rodzaj_wypadku": "upadek",
             "przyczyna": "nieuwaga ucznia", "miejsce": "schody", "zajecia": "lekcja", "liczba": 1},
        ]
        db.insert_rows(self.db, rows)

    def test_totals(self):
        t = db.totals(self.db)
        self.assertEqual(t["total_accidents"], 6)
        self.assertEqual(t["records"], 3)
        self.assertEqual(len(t["years"]), 2)

    def test_aggregate_by(self):
        res = db.aggregate_by(self.db, "wojewodztwo")
        labels = [r["label"] for r in res]
        self.assertIn("MAZOWIECKIE", labels)
        maz = next(r for r in res if r["label"] == "MAZOWIECKIE")
        self.assertEqual(maz["value"], 5)

    def test_trend(self):
        tr = db.trend_by_year(self.db)
        self.assertEqual(len(tr), 2)

    def test_search_filter(self):
        rows, total = db.search(self.db, {"wojewodztwo": "ŚLĄSKIE"})
        self.assertEqual(total, 1)
        self.assertEqual(rows[0]["liczba"], 1)

    def test_search_pagination(self):
        rows, total = db.search(self.db, {}, limit=2, offset=0)
        self.assertEqual(len(rows), 2)
        self.assertEqual(total, 3)

    def test_distinct(self):
        vals = db.distinct(self.db, "typ_podmiotu")
        self.assertIn("Przedszkole", vals)

    def test_invalid_column(self):
        with self.assertRaises(ValueError):
            db.aggregate_by(self.db, "foo")


if __name__ == "__main__":
    unittest.main()
