"""Tests for data loading."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from safeschool.data_loader import load_csv


class TestLoader(unittest.TestCase):
    def test_load_sample(self):
        sample = Path(__file__).resolve().parents[1] / "tests" / "sample.csv"
        if not sample.exists():
            self.skipTest("sample.csv not available")
        rows = load_csv(sample, "2018/2019")
        self.assertGreater(len(rows), 100)
        self.assertEqual(rows[0]["year"], "2018/2019")
        self.assertIn("wojewodztwo", rows[0])
        self.assertTrue(all(isinstance(r["liczba"], int) for r in rows))

    def test_load_empty_dir(self):
        # ensure load_csv handles a small synthetic file
        d = Path(tempfile.mkdtemp()) / "x.csv"
        d.write_text("Wojewodztwo,Powiat,Gmina,TypPodmiotu,RodzajWypadku,PrzyczynaWypadku,MiejsceWypadku,RodzajZajec,LiczbaWypadkow\nMAZOWIECKIE,warszawski,Warszawa,Szkoła,upadek,brak,korytarz,lekcja,5\n", encoding="utf-8")
        rows = load_csv(d, "2020/2021")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["liczba"], 5)
        self.assertEqual(rows[0]["wojewodztwo"], "MAZOWIECKIE")


if __name__ == "__main__":
    unittest.main()
