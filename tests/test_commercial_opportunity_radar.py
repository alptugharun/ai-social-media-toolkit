import unittest
from datetime import datetime, timezone

from tools.commercial_opportunity_radar import Lane, render_report, scale


class CommercialOpportunityRadarTests(unittest.TestCase):
    def test_scale_orders_values(self):
        values = scale([1, 10, 100], log=True)
        self.assertLess(values[0], values[1])
        self.assertLess(values[1], values[2])

    def test_report_is_not_revenue_forecast(self):
        lane = Lane(
            slug="creator-tools",
            query="creator tools ai open source",
            total_count=20,
            top_stars=1000,
            median_stars_per_day=4.0,
            demand_score=80,
        )
        readiness = {
            "stars": 0,
            "forks": 0,
            "subscribers": 1,
            "has_discussions": False,
            "has_pages": False,
            "funding_configured": False,
            "release_count_sample": 0,
        }
        candidate = {
            "name": "creator-ops-workspace",
            "job": "A useful hosted workflow.",
            "direct_supply": 3,
            "gap_score": 90.0,
            "score": 88.0,
        }
        report = render_report(
            datetime(2026, 9, 24, tzinfo=timezone.utc),
            [lane],
            [],
            readiness,
            [candidate],
        )
        self.assertIn("not a revenue forecast", report)
        self.assertIn("human approval", report.lower())
        self.assertIn("GitHub Agentic Workflows", report)

    def test_report_does_not_equate_stars_with_revenue(self):
        lane = Lane(
            slug="creator-tools",
            query="creator tools",
            total_count=10,
            top_stars=100,
            median_stars_per_day=1.0,
            demand_score=50,
        )
        readiness = {
            "stars": 1000,
            "forks": 100,
            "subscribers": 10,
            "has_discussions": True,
            "has_pages": True,
            "funding_configured": True,
            "release_count_sample": 2,
        }
        report = render_report(
            datetime(2026, 9, 24, tzinfo=timezone.utc),
            [lane],
            [],
            readiness,
            [],
        )
        self.assertIn("Stars are distribution / interest signals, not customer revenue.", report)


if __name__ == "__main__":
    unittest.main()
