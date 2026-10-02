import unittest
from datetime import datetime, timezone

from tools.github_growth_radar import LaneResult, md_escape, parse_trending, render_report, score_lanes, stars_per_day


class GitHubGrowthRadarTests(unittest.TestCase):
    def test_parse_trending(self):
        html = """
        <article class="Box-row">
          <h2><a href="/owner/repo">owner / repo</a></h2>
          <span>1,234 stars today</span>
        </article>
        """
        self.assertEqual(
            parse_trending(html),
            [{"full_name": "owner/repo", "stars_today": 1234}],
        )

    def test_parse_trending_ignores_sponsor_link_before_repo_heading(self):
        html = """
        <article class="Box-row">
          <a href="/sponsors/mattpocock">Sponsor</a>
          <h2 class="h3 lh-condensed"><a href="/real-owner/real-repo">real-owner / real-repo</a></h2>
          <span>321 stars today</span>
        </article>
        """
        self.assertEqual(
            parse_trending(html),
            [{"full_name": "real-owner/real-repo", "stars_today": 321}],
        )

    def test_parse_trending_rejects_reserved_non_repo_heading(self):
        html = """
        <article class="Box-row">
          <h2><a href="/sponsors/example">sponsors / example</a></h2>
          <span>99 stars today</span>
        </article>
        """
        self.assertEqual(parse_trending(html), [])

    def test_md_escape_escapes_table_separator(self):
        self.assertEqual(md_escape("a|b\nc"), "a\\|b c")

    def test_stars_per_day_has_one_day_floor(self):
        now = datetime(2026, 9, 24, tzinfo=timezone.utc)
        self.assertEqual(
            stars_per_day(100, "2026-09-24T00:00:00Z", now),
            100.0,
        )

    def test_score_lanes_prefers_stronger_demand(self):
        lanes = [
            LaneResult("a", "A", 100, 10000, 100.0, 2, []),
            LaneResult("b", "B", 10, 100, 1.0, 0, []),
        ]
        score_lanes(lanes)
        self.assertGreater(lanes[0].demand_score, lanes[1].demand_score)

    def test_render_report_labels_proxies(self):
        now = datetime(2026, 9, 24, tzinfo=timezone.utc)
        lane = LaneResult("a", "Agent skills", 10, 100, 4.2, 1, [], 80, 20, 75)
        candidate = {
            "name": "example-skill",
            "job": "Solve a measurable creator workflow.",
            "result_count": 3,
            "novelty_proxy": 90.0,
            "score": 82.0,
        }
        report = render_report(now, [], [lane], [candidate], [])
        self.assertIn("does **not** claim exact GitHub search volume", report)
        self.assertIn("heuristic", report)
        self.assertIn("human review", report.lower())


if __name__ == "__main__":
    unittest.main()


# Strategic challenge output is validated through integration rendering tests.
