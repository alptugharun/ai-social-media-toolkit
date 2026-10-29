import io
import json
import unittest
import urllib.error
import urllib.parse
from unittest.mock import patch
from datetime import datetime, timezone

from tools.github_growth_radar import (LaneResult, SEARCH_REQUEST_INTERVAL_SECONDS, describe_github_http_error, md_escape, parse_trending, render_report, score_lanes, search_repositories, stars_per_day)


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



    @patch("tools.github_growth_radar.fetch_json")
    @patch("tools.github_growth_radar.time.sleep")
    def test_search_repositories_is_paced_with_headroom(self, mock_sleep, mock_fetch):
        mock_fetch.return_value = {"items": [], "total_count": 0}
        self.assertEqual(search_repositories("AI agents", "test-token", per_page=3)["total_count"], 0)
        self.assertGreaterEqual(SEARCH_REQUEST_INTERVAL_SECONDS, 6.0)
        mock_sleep.assert_called_once_with(SEARCH_REQUEST_INTERVAL_SECONDS)
        url, token = mock_fetch.call_args.args
        self.assertEqual(token, "test-token")
        params = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)
        self.assertEqual(params["q"], ["AI agents"])
        self.assertEqual(params["per_page"], ["3"])

    def test_http_error_diagnostic_exposes_primary_limit_without_query(self):
        error = urllib.error.HTTPError(
            "https://api.github.com/search/repositories?q=private-secret&per_page=5",
            403,
            "Forbidden",
            {"X-RateLimit-Remaining": "0", "X-RateLimit-Reset": "1790000000"},
            io.BytesIO(json.dumps({"message": "API rate limit exceeded"}).encode()),
        )
        message = describe_github_http_error(error)
        self.assertIn("GitHub API error: 403 Forbidden", message)
        self.assertIn("endpoint=/search/repositories", message)
        self.assertIn("category=primary-rate-limit", message)
        self.assertIn("reset=1790000000", message)
        self.assertNotIn("private-secret", message)

    def test_http_error_diagnostic_identifies_secondary_limit(self):
        error = urllib.error.HTTPError(
            "https://api.github.com/search/repositories?q=test",
            403,
            "Forbidden",
            {"X-RateLimit-Remaining": "24", "Retry-After": "60"},
            io.BytesIO(json.dumps({"message": "You have exceeded a secondary rate limit."}).encode()),
        )
        message = describe_github_http_error(error)
        self.assertIn("category=secondary-rate-limit", message)
        self.assertIn("retry_after=60", message)

    def test_http_error_diagnostic_does_not_mislabel_ambiguous_403(self):
        error = urllib.error.HTTPError(
            "https://api.github.com/search/repositories?q=another-secret",
            403,
            "Forbidden",
            {"X-RateLimit-Remaining": "20"},
            io.BytesIO(json.dumps({"message": "Resource not accessible by integration"}).encode()),
        )
        message = describe_github_http_error(error)
        self.assertIn("category=unknown-403-or-429", message)
        self.assertNotIn("another-secret", message)
        self.assertNotIn("Resource not accessible", message)

if __name__ == "__main__":
    unittest.main()


# Strategic challenge output is validated through integration rendering tests.
