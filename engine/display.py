"""Terminal display helpers with color output."""

import os
import shutil
from datetime import timedelta

# ANSI colors
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
BLUE   = "\033[94m"
MAGENTA= "\033[95m"
CYAN   = "\033[96m"
WHITE  = "\033[97m"

CATEGORY_COLORS = {
    "api":        BLUE,
    "automation": YELLOW,
    "async":      MAGENTA,
    "langchain":  CYAN,
}

DIFFICULTY_COLORS = {
    "easy":   GREEN,
    "medium": YELLOW,
    "hard":   RED,
}

DIFFICULTY_STARS = {
    "easy":   "★☆☆",
    "medium": "★★☆",
    "hard":   "★★★",
}


def _term_width():
    return shutil.get_terminal_size((80, 24)).columns


def _hr(char="─"):
    return char * _term_width()


class Display:
    def banner(self):
        w = _term_width()
        lines = [
            "",
            f"{CYAN}{BOLD}" + "╔" + "═" * (w - 2) + "╗" + RESET,
            f"{CYAN}{BOLD}" + "║" + "  SYNELIUM CODING GAME  —  15 min/day Python practice".center(w - 2) + "║" + RESET,
            f"{CYAN}{BOLD}" + "╚" + "═" * (w - 2) + "╝" + RESET,
            "",
        ]
        print("\n".join(lines))

    def challenge_header(self, challenge, elapsed=None, time_limit=900):
        cat_color = CATEGORY_COLORS.get(challenge["category"], WHITE)
        diff_color = DIFFICULTY_COLORS.get(challenge["difficulty"], WHITE)
        stars = DIFFICULTY_STARS.get(challenge["difficulty"], "")

        print(_hr())
        print(
            f"{BOLD}[{challenge['id']}]{RESET}  "
            f"{cat_color}{challenge['category'].upper()}{RESET}  "
            f"{diff_color}{stars} {challenge['difficulty']}{RESET}"
        )
        print(f"{BOLD}{challenge['title']}{RESET}")
        print(_hr())
        print()
        print(challenge["description"])
        print()

        if challenge.get("context"):
            print(f"{DIM}Context:{RESET}")
            print(f"{DIM}{challenge['context']}{RESET}")
            print()

        if elapsed is not None:
            remaining = time_limit - elapsed
            color = GREEN if remaining > 300 else (YELLOW if remaining > 60 else RED)
            mins, secs = divmod(int(remaining), 60)
            print(f"{color}Time remaining: {mins:02d}:{secs:02d}{RESET}")
            print()

    def show_starter(self, starter_code: str):
        print(f"{DIM}Starter code (edit the file opened in your editor):{RESET}")
        print(f"{DIM}{_hr('·')}{RESET}")
        for line in starter_code.splitlines():
            print(f"{DIM}{line}{RESET}")
        print(f"{DIM}{_hr('·')}{RESET}")
        print()

    def test_results(self, results: list[dict], elapsed: float):
        passed = sum(1 for r in results if r["passed"])
        total = len(results)
        color = GREEN if passed == total else (YELLOW if passed > 0 else RED)

        print()
        print(_hr())
        print(f"{BOLD}Test Results: {color}{passed}/{total} passed{RESET}")
        print(_hr())

        for i, r in enumerate(results, 1):
            icon = f"{GREEN}✓{RESET}" if r["passed"] else f"{RED}✗{RESET}"
            print(f"  {icon}  Test {i}: {r['description']}")
            if not r["passed"]:
                if r.get("expected") is not None:
                    print(f"      {DIM}Expected: {r['expected']}{RESET}")
                if r.get("got") is not None:
                    print(f"      {DIM}Got:      {r['got']}{RESET}")
                if r.get("error"):
                    print(f"      {RED}Error: {r['error']}{RESET}")

        mins, secs = divmod(int(elapsed), 60)
        print()
        print(f"  Time: {mins:02d}:{secs:02d}")
        print()

    def score_summary(self, score: int, xp_earned: int, streak: int):
        color = GREEN if score >= 80 else (YELLOW if score >= 50 else RED)
        print(f"{BOLD}Score: {color}{score}/100{RESET}   "
              f"{YELLOW}+{xp_earned} XP{RESET}   "
              f"{'🔥 ' if streak > 1 else ''}Streak: {streak} day{'s' if streak != 1 else ''}")
        print()

    def show_hint(self, hint: str):
        print(f"{YELLOW}{BOLD}Hint:{RESET} {hint}")
        print()

    def show_solution(self, solution: str):
        print(f"{CYAN}{BOLD}Solution:{RESET}")
        print(f"{DIM}{_hr('·')}{RESET}")
        for line in solution.splitlines():
            print(f"{DIM}{line}{RESET}")
        print(f"{DIM}{_hr('·')}{RESET}")
        print()

    def show_stats(self, stats: dict):
        self.banner()
        print(f"{BOLD}Your Progress{RESET}")
        print(_hr())
        print(f"  Total XP:        {YELLOW}{stats['total_xp']}{RESET}")
        print(f"  Challenges done: {stats['completed']}")
        print(f"  Current streak:  {'🔥 ' if stats['streak'] > 1 else ''}{stats['streak']} day{'s' if stats['streak'] != 1 else ''}")
        print(f"  Sessions played: {stats['sessions']}")
        print()
        print(f"{BOLD}By Category:{RESET}")
        for cat, data in stats["by_category"].items():
            color = CATEGORY_COLORS.get(cat, WHITE)
            bar = "█" * data["completed"] + "░" * max(0, data["total"] - data["completed"])
            print(f"  {color}{cat:<12}{RESET} {bar}  {data['completed']}/{data['total']}")
        print()
        print(f"{BOLD}By Difficulty:{RESET}")
        for diff, data in stats["by_difficulty"].items():
            color = DIFFICULTY_COLORS.get(diff, WHITE)
            print(f"  {color}{diff:<8}{RESET} {data['completed']}/{data['total']} completed")
        print()

    def list_challenges(self, challenges, progress):
        self.banner()
        completed_ids = set(progress.data.get("completed_ids", []))
        print(f"{BOLD}All Challenges{RESET}")
        print(_hr())
        current_cat = None
        for c in challenges:
            if c["category"] != current_cat:
                current_cat = c["category"]
                color = CATEGORY_COLORS.get(current_cat, WHITE)
                print(f"\n{color}{BOLD}{current_cat.upper()}{RESET}")
            done = f"{GREEN}✓{RESET}" if c["id"] in completed_ids else " "
            diff_color = DIFFICULTY_COLORS.get(c["difficulty"], WHITE)
            stars = DIFFICULTY_STARS.get(c["difficulty"], "")
            print(f"  [{done}] {c['id']:<12} {diff_color}{stars}{RESET}  {c['title']}")
        print()

    def prompt_ready(self, filepath: str):
        print(f"{BOLD}Challenge file:{RESET} {CYAN}{filepath}{RESET}")
        print(f"Edit it, save, then press {BOLD}ENTER{RESET} to run tests  |  "
              f"Type {BOLD}hint{RESET} for a hint  |  "
              f"Type {BOLD}skip{RESET} to skip  |  "
              f"Type {BOLD}quit{RESET} to exit")
        print()

    def time_up(self):
        print(f"\n{RED}{BOLD}⏰ Time's up! Session complete.{RESET}\n")

    def session_complete(self, session_stats: dict):
        print(_hr("═"))
        print(f"{BOLD}{GREEN}Session complete!{RESET}")
        print(f"  Challenges attempted: {session_stats['attempted']}")
        print(f"  Challenges passed:    {session_stats['passed']}")
        print(f"  XP earned this session: {YELLOW}{session_stats['xp']}{RESET}")
        print(_hr("═"))
        print()
