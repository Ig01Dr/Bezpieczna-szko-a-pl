"""Smoke tests for the web layer."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from safeschool.app import app


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health(self):
        r = self.client.get("/health")
        self.assertEqual(r.status_code, 200)
        self.assertIn("status", r.get_json())

    def test_index(self):
        r = self.client.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertIn("SafeSchool", r.get_data(as_text=True))

    def test_search(self):
        r = self.client.get("/search")
        self.assertEqual(r.status_code, 200)

    def test_api(self):
        r = self.client.get("/api/trend")
        self.assertEqual(r.status_code, 200)


if __name__ == "__main__":
    unittest.main()
