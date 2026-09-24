import unittest
from datetime import datetime, timezone

from tools.pinterest_growth_radar import Lane, render_report, trend_score


class PinterestGrowthRadarTests(unittest.TestCase):
    def test_trend_score_rewards_recent_growth(self):
        a = trend_score(
            {
                "pct_growth_wow": 100,
                "pct_growth_mom": 10,
                "pct_growth_yoy": 10,
            }
        )
        b = trend_score(
            {
                "pct_growth_wow": 10,
                "pct_growth_mom": 10,
                "pct_growth_yoy": 10,
            }
        )
        self.assertGreater(a, b)

    def test_report_does_not_fabricate_trends(self):
        lane = Lane(
            slug="pinterest-api",
            query="pinterest api automation",
            total_count=10,
            top_stars=100,
            median_stars_per_day=1.2,
            demand_score=60,
        )
        report = render_report(
            datetime(2026, 9, 24, tzinfo=timezone.utc),
            ["US"],
            [],
            ["US: Pinterest Trends API returned HTTP 401."],
            [lane],
            [],
            False,
        )
        self.assertIn("No authenticated/live Trends rows were available", report)
        self.assertIn("No trend values are fabricated", report)
        self.assertIn("human-reviewed", report)

    def test_report_includes_live_rows_when_available(self):
        lane = Lane(
            slug="pinterest-api",
            query="pinterest api automation",
            total_count=10,
            top_stars=100,
            median_stars_per_day=1.2,
            demand_score=60,
        )
        trends = [
            {
                "region": "US",
                "rank": 1,
                "keyword": "example trend",
                "pct_growth_wow": 30,
                "pct_growth_mom": 80,
                "pct_growth_yoy": 10,
                "time_series": {},
                "score": 41.0,
            }
        ]
        report = render_report(
            datetime(2026, 9, 24, tzinfo=timezone.utc),
            ["US"],
            trends,
            [],
            [lane],
            [],
            True,
        )
        self.assertIn("example trend", report)
        self.assertIn("+30%", report)


if __name__ == "__main__":
    unittest.main()
