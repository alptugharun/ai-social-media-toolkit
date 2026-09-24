import unittest
from datetime import datetime, timezone

from tools.maps_opportunity_radar import Lane, render_report
from tools.places_market_scan import build_payload


class PlacesMarketScanTests(unittest.TestCase):
    def test_build_payload_count(self):
        payload = build_payload(
            latitude=36.88,
            longitude=30.70,
            radius=750,
            included_types=["cafe"],
            min_rating=4.2,
            mode="count",
        )
        self.assertEqual(payload["insights"], ["INSIGHT_COUNT"])
        self.assertEqual(
            payload["filter"]["locationFilter"]["circle"]["latLng"]["latitude"],
            36.88,
        )
        self.assertEqual(
            payload["filter"]["typeFilter"]["includedTypes"],
            ["cafe"],
        )
        self.assertEqual(
            payload["filter"]["operatingStatus"],
            ["OPERATING_STATUS_OPERATIONAL"],
        )
        self.assertEqual(
            payload["filter"]["ratingFilter"]["minRating"],
            4.2,
        )

    def test_build_payload_places_requests_ids(self):
        payload = build_payload(
            latitude=36.88,
            longitude=30.70,
            radius=300,
            included_types=["restaurant"],
            mode="places",
        )
        self.assertEqual(
            payload["insights"],
            ["INSIGHT_COUNT", "INSIGHT_PLACES"],
        )


class MapsOpportunityReportTests(unittest.TestCase):
    def test_report_has_no_guarantee_and_human_gate(self):
        lane = Lane(
            slug="google-maps-mcp",
            query="google maps mcp",
            total_count=100,
            top_stars=1000,
            median_stars_per_day=2.5,
            demand_score=80,
        )
        candidate = {
            "name": "local-business-intelligence-agent",
            "job": "Solve a permitted local workflow.",
            "direct_supply": 5,
            "gap_score": 90.0,
            "score": 88.0,
        }
        report = render_report(
            datetime(2026, 9, 24, tzinfo=timezone.utc),
            [lane],
            [],
            [candidate],
        )
        self.assertIn("does **not** guarantee", report)
        self.assertIn("Maps Policy Guard", report)
        self.assertIn("Human Review Gate", report)

    def test_generic_wrapper_is_not_the_recommended_contract(self):
        report = render_report(
            datetime(2026, 9, 24, tzinfo=timezone.utc),
            [
                Lane(
                    slug="google-maps-mcp",
                    query="google maps mcp",
                    total_count=500,
                    top_stars=5000,
                    median_stars_per_day=5,
                    demand_score=90,
                )
            ],
            [],
            [
                {
                    "name": "local-business-intelligence-agent",
                    "job": "Higher-level workflow intelligence.",
                    "direct_supply": 4,
                    "gap_score": 95.0,
                    "score": 91.0,
                },
                {
                    "name": "generic-google-maps-mcp",
                    "job": "Generic wrapper.",
                    "direct_supply": 500,
                    "gap_score": 10.0,
                    "score": 30.0,
                },
            ],
        )
        self.assertIn("another generic Google Maps MCP wrapper", report)


if __name__ == "__main__":
    unittest.main()
