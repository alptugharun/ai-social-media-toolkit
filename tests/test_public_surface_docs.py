from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / "docs" / "public-surface-map.json"
EN = ROOT / "docs" / "START-FROM-ZERO.md"
TR = ROOT / "docs" / "START-FROM-ZERO_TR.md"
TRUST = ROOT / "docs" / "TRUST-MATRIX.md"

REQUIRED_FIELDS = {
    "id", "name", "kind", "what", "why", "who",
    "first_step", "expected_result", "verify", "limitations", "help"
}


class PublicSurfaceDocsTests(unittest.TestCase):
    def setUp(self):
        self.payload = json.loads(MAP.read_text(encoding="utf-8"))
        self.en = EN.read_text(encoding="utf-8")
        self.tr = TR.read_text(encoding="utf-8")
        self.trust = TRUST.read_text(encoding="utf-8")

    def test_surface_contract_is_complete_and_unique(self):
        ids = []
        for surface in self.payload["surfaces"]:
            self.assertTrue(REQUIRED_FIELDS.issubset(surface), surface.get("id"))
            for field in REQUIRED_FIELDS:
                self.assertTrue(str(surface[field]).strip(), f"{surface.get('id')}:{field}")
            ids.append(surface["id"])
        self.assertEqual(len(ids), len(set(ids)))

    def test_every_public_surface_is_named_in_both_beginner_guides(self):
        for surface in self.payload["surfaces"]:
            self.assertIn(surface["name"], self.en, surface["id"])
            self.assertIn(surface["name"], self.tr, surface["id"])

    def test_guides_explain_first_result_and_failure_boundary(self):
        for text in (self.en, self.tr):
            lower = text.lower()
            self.assertIn("pass", lower)
            self.assertIn("fail", lower)
            self.assertIn("blocked", lower)
            self.assertIn("mcp", lower)
            self.assertIn("agent skill", lower)
            self.assertIn("automation", lower)
        self.assertIn("security", self.en.lower())
        self.assertIn("güvenlik", self.tr.lower())

    def test_trust_matrix_tracks_major_external_surfaces(self):
        for name in ("M8ven", "OpenSSF", "Official MCP Registry", "Glama", "skills.sh"):
            self.assertIn(name, self.trust)
        self.assertIn("Never do for a score", self.trust)


if __name__ == "__main__":
    unittest.main()
