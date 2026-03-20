"""
Game session: picks a challenge, opens editor, runs tests, tracks time.
"""

import os
import sys
import time
import random
import tempfile
import subprocess
import threading
from pathlib import Path

from engine.display import Display
from engine.progress import Progress
from engine.runner import run_challenge, score_results, xp_for_score
from challenges import get_all_challenges, get_by_category, get_by_id

SESSION_TIME = 15 * 60  # 15 minutes


class Session:
    def __init__(
        self,
        category: str = "random",
        difficulty: str | None = None,
        challenge_id: str | None = None,
        show_solution: bool = False,
    ):
        self.category = category
        self.difficulty = difficulty
        self.challenge_id = challenge_id
        self.show_solution = show_solution
        self.display = Display()
        self.progress = Progress()
        self.session_stats = {"attempted": 0, "passed": 0, "xp": 0}

    def _pick_challenge(self) -> dict | None:
        if self.challenge_id:
            return get_by_id(self.challenge_id)

        pool = get_by_category(self.category) if self.category != "random" else get_all_challenges()
        if self.difficulty:
            pool = [c for c in pool if c["difficulty"] == self.difficulty]

        # Prefer not-yet-completed challenges
        completed = set(self.progress.data.get("completed_ids", []))
        fresh = [c for c in pool if c["id"] not in completed]
        return random.choice(fresh if fresh else pool) if pool else None

    def _write_challenge_file(self, challenge: dict) -> str:
        tmpdir = Path(tempfile.mkdtemp(prefix="synelium_"))
        fpath = tmpdir / f"{challenge['id']}.py"
        header = f"# Challenge: {challenge['title']}\n# Category: {challenge['category']}  |  Difficulty: {challenge['difficulty']}\n#\n"
        desc_lines = "\n".join(f"# {line}" for line in challenge["description"].splitlines())
        fpath.write_text(header + desc_lines + "\n\n" + challenge["starter_code"])
        return str(fpath)

    def _open_editor(self, fpath: str):
        editor = os.environ.get("EDITOR", os.environ.get("VISUAL", "nano"))
        try:
            subprocess.run([editor, fpath])
        except FileNotFoundError:
            # fallback
            try:
                subprocess.run(["nano", fpath])
            except FileNotFoundError:
                print(f"Could not open editor. Edit the file manually: {fpath}")

    def _read_user_code(self, fpath: str) -> str:
        return Path(fpath).read_text()

    def run(self):
        self.display.banner()
        self.progress.start_session()

        session_start = time.monotonic()

        while True:
            elapsed_session = time.monotonic() - session_start
            if elapsed_session >= SESSION_TIME:
                self.display.time_up()
                break

            challenge = self._pick_challenge()
            if not challenge:
                print("No challenges found for those filters.")
                break

            fpath = self._write_challenge_file(challenge)
            self.display.challenge_header(
                challenge,
                elapsed=elapsed_session,
                time_limit=SESSION_TIME,
            )
            self.display.prompt_ready(fpath)

            challenge_start = time.monotonic()
            hint_index = 0
            submitted = False

            while True:
                cmd = input("> ").strip().lower()

                if cmd == "quit":
                    self._finish_session(session_start)
                    return

                if cmd == "skip":
                    print("Skipping challenge...\n")
                    break

                if cmd == "hint":
                    hints = challenge.get("hints", [])
                    if hints:
                        self.display.show_hint(hints[hint_index % len(hints)])
                        hint_index += 1
                    else:
                        print("No hints available for this challenge.\n")
                    continue

                if cmd in ("", "test", "run", "submit"):
                    user_code = self._read_user_code(fpath)
                    elapsed_challenge = time.monotonic() - challenge_start
                    results = run_challenge(challenge, user_code)
                    self.display.test_results(results, elapsed_challenge)

                    score = score_results(results, elapsed_challenge)
                    xp = xp_for_score(score, challenge["difficulty"])
                    self.progress.record_attempt(challenge["id"], score, xp, elapsed_challenge)
                    self.display.score_summary(score, xp, self.progress.data.get("streak", 1))

                    self.session_stats["attempted"] += 1
                    self.session_stats["xp"] += xp
                    passed = sum(1 for r in results if r["passed"])
                    if passed == len(results):
                        self.session_stats["passed"] += 1

                    if self.show_solution or score < 60:
                        sol = challenge.get("solution", "# No solution provided")
                        show = input("Show solution? [y/N] ").strip().lower()
                        if show == "y":
                            self.display.show_solution(sol)

                    submitted = True
                    again = input("Next challenge? [Y/n] ").strip().lower()
                    if again == "n":
                        self._finish_session(session_start)
                        return
                    break

                if cmd:
                    print("Commands: ENTER=run tests, hint, skip, quit")

            if not submitted:
                continue

        self._finish_session(session_start)

    def _finish_session(self, session_start: float):
        elapsed = time.monotonic() - session_start
        self.session_stats["duration"] = round(elapsed)
        self.progress.end_session(self.session_stats)
        self.display.session_complete(self.session_stats)
