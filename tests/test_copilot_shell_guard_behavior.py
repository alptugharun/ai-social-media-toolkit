"""Behavioral regression checks for the Copilot preToolUse safety hook."""

from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "copilot_shell_guard.py"


class ShellGuardBehaviorTests(unittest.TestCase):
    def check(self, command: str, *, serialized_args: bool = True, tool_name: str = "bash") -> dict:
        args = {"command": command, "description": "A safe example description"}
        event = {"toolName": tool_name, "toolArgs": json.dumps(args) if serialized_args else args}
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            input=json.dumps(event),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_normal_shell_commands_remain_unchanged(self):
        for command in ("git status --short", "python -m unittest -q", "git push origin feature/test", "rm -rf .pytest_cache"):
            for encoded in (True, False):
                with self.subTest(command=command, encoded=encoded):
                    self.assertEqual(self.check(command, serialized_args=encoded), {})

    def test_root_delete_is_denied_for_option_permutations(self):
        root = "/"
        cases = (
            f"rm -rf {root}",
            f"rm -fr {root}",
            f"rm -r -f {root}",
            f"rm --force --recursive {root}",
            f"rm -rf -- {root}",
            "rm -fr .",
            "rm -f -r ..",
            "echo done && rm -fr ./",
        )
        for case in cases:
            with self.subTest(command=case):
                response = self.check(case)
                self.assertEqual(response.get("permissionDecision"), "deny")
                self.assertIn("recursive-root-delete", response.get("permissionDecisionReason", ""))

    def test_other_sensitive_actions_are_denied(self):
        cases = (
            "git push --force origin feature/test",
            "git reset --hard",
            "gh release upload v0.3.0-alpha.1 artifact.zip --clobber",
        )
        for command in cases:
            with self.subTest(command=command):
                self.assertEqual(self.check(command).get("permissionDecision"), "deny")

    def test_hard_reset_flag_order_is_guarded(self):
        # Git accepts --hard after a revision and after quiet flags.
        cases = (
            "git reset HEAD --hard",
            "git reset -q --hard",
            "git reset -q HEAD --hard",
            "git reset --quiet --hard",
            "git -C workspace reset HEAD --hard",
            "git reset HEAD --hard; echo done",
        )
        for command in cases:
            with self.subTest(command=command):
                decision = self.check(command)
                self.assertEqual(decision.get("permissionDecision"), "deny")
                self.assertIn("hard-reset", decision.get("permissionDecisionReason", ""))

        # A later shell command must not turn a harmless reset into a denial.
        for command in (
            "git reset --soft HEAD~1",
            "git reset HEAD --mixed",
            "git reset HEAD && echo --hard",
            "git reset HEAD; echo --hard",
        ):
            with self.subTest(command=command):
                self.assertEqual(self.check(command), {})

    def test_global_git_options_protect_branch_deletes_and_flag_combinations(self):
        """Reject destructive Git actions with leading global flags."""
        cases = (
            "git -C /tmp/project push --force origin topic",
            "git -C../project reset --hard",
            "git -c core.quotePath=false push -f origin topic",
            "git --git-dir=.git push --delete main",
            "git --work-tree ../work branch -D master",
            "git -C . -c core.quotePath=false push --force-with-lease origin topic",
        )
        for command in cases:
            with self.subTest(command=command):
                self.assertEqual(self.check(command).get("permissionDecision"), "deny")

        # Global flags alone must not turn a normal operation into a denial.
        for command in (
            "git -C . push origin feature/test",
            "git --no-pager status",
        ):
            with self.subTest(command=command):
                self.assertEqual(self.check(command), {})

    def test_non_shell_tools_are_unaffected(self):
        self.assertEqual(self.check("git push --force", tool_name="read"), {})

    def test_descriptive_field_is_not_mistaken_for_command(self):
        event = {"toolName": "bash", "toolArgs": json.dumps({"command": "git status", "description": "git push --force"})}
        proc = subprocess.run([sys.executable, str(SCRIPT)], input=json.dumps(event), text=True, capture_output=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout), {})

    def test_uninspectable_shell_arguments_are_denied(self):
        for args in ("not json", {}, {"description": "unrelated"}, [], None):
            with self.subTest(args=args):
                event = {"toolName": "bash", "toolArgs": args}
                proc = subprocess.run([sys.executable, str(SCRIPT)], input=json.dumps(event), text=True, capture_output=True)
                self.assertEqual(proc.returncode, 0, proc.stderr)
                self.assertEqual(json.loads(proc.stdout).get("permissionDecision"), "deny")


    def test_git_global_options_preserve_sensitive_command_detection(self):
        # Git permits global flags before its subcommand; the guard must not
        # mistake a guarded push/reset for a harmless operation.
        cases = {
            "git -C workspace push origin main --force": "force-push",
            "git --git-dir=.git push -f origin main": "force-push",
            "git -c core.quotePath=false push origin main --force-with-lease": "force-push",
            "git --no-pager push origin main --force": "force-push",
            "git -C workspace reset --hard HEAD": "hard-reset",
        }
        for command, expected_rule in cases.items():
            with self.subTest(command=command):
                decision = self.check(command)
                self.assertEqual(decision.get("permissionDecision"), "deny")
                self.assertIn(expected_rule, decision.get("permissionDecisionReason", ""))

        # Non-destructive equivalents should continue to defer to host policy.
        for command in ("git -C workspace status", "git --no-pager log -1"):
            with self.subTest(command=command):
                self.assertEqual(self.check(command), {})

    def test_snake_case_shell_payload_is_inspected(self):
        event = {"tool_name": "bash", "tool_input": {"command": "git push -f origin main"}}
        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            input=json.dumps(event),
            text=True,
            capture_output=True,
            check=False,
            timeout=5,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        decision = json.loads(result.stdout)
        self.assertEqual(decision.get("permissionDecision"), "deny")
        self.assertIn("force-push", decision.get("permissionDecisionReason", ""))


    def test_shell_command_boundaries_do_not_hide_dangerous_flags(self):
        # Valid shell separators must neither hide a dangerous option nor
        # make an option belonging to a later command look like a Git flag.
        blocked = {
            "git push origin main -f; echo done": "force-push",
            "git push --force&& echo done": "force-push",
            "git push --force-with-lease=main": "force-push",
            "gh release upload v1 asset.zip --clobber; echo done": "release-clobber",
            "git push origin --delete main; echo done": "delete-protected-branch",
            "git branch -D master && echo done": "delete-local-protected-branch",
        }
        for command, rule in blocked.items():
            with self.subTest(command=command):
                decision = self.check(command)
                self.assertEqual(decision.get("permissionDecision"), "deny")
                self.assertIn(rule, decision.get("permissionDecisionReason", ""))

        safe = (
            "git push origin topic && echo --force",
            "git push origin topic; echo --force",
            "gh release upload v1 asset.zip; echo --clobber",
            "git push origin topic && echo --delete main",
            "git branch -D feature && echo master",
        )
        for command in safe:
            with self.subTest(command=command):
                self.assertEqual(self.check(command), {})




    def test_git_push_native_refspec_delete_and_force_modes(self):
        # Git accepts --delete ahead of the remote, -d, and empty-source
        # refspecs. Prefixing a refspec with + forces the update.
        blocked = {
            "git push --delete origin main": "delete-protected-branch",
            "git push -d origin master": "delete-protected-branch",
            "git push --delete origin refs/heads/master": "delete-protected-branch",
            "git push --delete origin \"main\"": "delete-protected-branch",
            "git -C workspace push --delete origin main": "delete-protected-branch",
            "git push origin :main": "delete-protected-branch",
            "git push origin \":refs/heads/master\"": "delete-protected-branch",
            "git push origin +HEAD:main": "force-push",
            "git push origin +topic": "force-push",
            "git push origin +topic:feature": "force-push",
        }
        for command, expected in blocked.items():
            with self.subTest(command=command):
                decision = self.check(command)
                self.assertEqual(decision.get("permissionDecision"), "deny")
                self.assertIn(expected, decision.get("permissionDecisionReason", ""))

        safe = (
            "git push origin topic",
            "git push --delete origin topic",
            "git push origin :topic",
            "git push origin main",
            "git push origin main:topic",
            "git push origin topic && echo --delete main",
            "git push origin --delete topic && echo main",
            "git push origin topic; echo +main",
        )
        for command in safe:
            with self.subTest(command=command):
                self.assertEqual(self.check(command), {})



    def test_local_protected_branch_deletion_variants(self):
        # Git supports -d/--delete, -D, grouped flags, -- and global options.
        blocked = (
            "git branch -d main",
            "git branch --delete master",
            "git branch -D -- main",
            "git branch -d -f main",
            "git branch -fd master",
            "git branch --delete --force main",
            "git branch --force --delete master",
            "git -C workspace branch -D -- master",
            "git branch -D topic master",
        )
        for command in blocked:
            with self.subTest(command=command):
                decision = self.check(command)
                self.assertEqual(decision.get("permissionDecision"), "deny")
                self.assertIn("delete-local-protected-branch", decision.get("permissionDecisionReason", ""))

        safe = (
            "git branch --list main",
            "git branch -D topic",
            "git branch --delete --force topic",
            "git branch -D topic && echo main",
            "git branch -d topic; echo master",
        )
        for command in safe:
            with self.subTest(command=command):
                self.assertEqual(self.check(command), {})

    def test_git_push_bulk_ref_update_modes_are_denied(self):
        # Per git-push docs, --mirror forces changed refs and deletes absent
        # refs; --prune can delete remote branches missing locally.
        blocked = {
            "git push --mirror origin": "mirror-push",
            "git push origin --mirror": "mirror-push",
            "git -C workspace push --mirror origin": "mirror-push",
            "git push --prune origin": "prune-push",
            "git push origin --prune": "prune-push",
        }
        for command, rule in blocked.items():
            with self.subTest(command=command):
                decision = self.check(command)
                self.assertEqual(decision.get("permissionDecision"), "deny")
                self.assertIn(rule, decision.get("permissionDecisionReason", ""))

        for command in (
            "git push origin topic",
            "git push origin main && echo --mirror",
            "git push origin topic; echo --prune",
        ):
            with self.subTest(command=command):
                self.assertEqual(self.check(command), {})


if __name__ == "__main__":
    unittest.main()
