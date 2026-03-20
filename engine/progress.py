"""Track user progress, XP, streaks, and session history."""

import json
import os
from datetime import datetime, date
from pathlib import Path

PROGRESS_FILE = Path(__file__).parent.parent / "data" / "progress.json"


class Progress:
    def __init__(self):
        PROGRESS_FILE.parent.mkdir(exist_ok=True)
        self.data = self._load()

    def _load(self) -> dict:
        if PROGRESS_FILE.exists():
            try:
                return json.loads(PROGRESS_FILE.read_text())
            except Exception:
                pass
        return {
            "total_xp": 0,
            "completed_ids": [],
            "attempted_ids": [],
            "sessions": [],
            "streak": 0,
            "last_played": None,
            "scores": {},
        }

    def save(self):
        PROGRESS_FILE.write_text(json.dumps(self.data, indent=2))

    def record_attempt(self, challenge_id: str, score: int, xp: int, elapsed: float):
        if challenge_id not in self.data["attempted_ids"]:
            self.data["attempted_ids"].append(challenge_id)
        if score >= 60 and challenge_id not in self.data["completed_ids"]:
            self.data["completed_ids"].append(challenge_id)
        # Keep best score
        prev = self.data["scores"].get(challenge_id, {})
        if score > prev.get("score", 0):
            self.data["scores"][challenge_id] = {
                "score": score,
                "xp": xp,
                "elapsed": round(elapsed),
                "date": date.today().isoformat(),
            }
        self.data["total_xp"] += xp
        self.save()

    def start_session(self):
        today = date.today().isoformat()
        last = self.data.get("last_played")
        if last:
            last_date = date.fromisoformat(last)
            delta = (date.today() - last_date).days
            if delta == 1:
                self.data["streak"] += 1
            elif delta > 1:
                self.data["streak"] = 1
            # delta == 0 means same day, keep streak
        else:
            self.data["streak"] = 1
        self.data["last_played"] = today
        self.save()

    def end_session(self, session_stats: dict):
        self.data["sessions"].append({
            "date": date.today().isoformat(),
            **session_stats,
        })
        self.save()

    def get_stats(self) -> dict:
        from challenges import ALL_CHALLENGES
        completed = set(self.data["completed_ids"])
        by_cat: dict[str, dict] = {}
        by_diff: dict[str, dict] = {}
        for c in ALL_CHALLENGES:
            cat = c["category"]
            diff = c["difficulty"]
            by_cat.setdefault(cat, {"total": 0, "completed": 0})
            by_diff.setdefault(diff, {"total": 0, "completed": 0})
            by_cat[cat]["total"] += 1
            by_diff[diff]["total"] += 1
            if c["id"] in completed:
                by_cat[cat]["completed"] += 1
                by_diff[diff]["completed"] += 1
        return {
            "total_xp": self.data["total_xp"],
            "completed": len(completed),
            "sessions": len(self.data["sessions"]),
            "streak": self.data.get("streak", 0),
            "by_category": by_cat,
            "by_difficulty": by_diff,
        }
