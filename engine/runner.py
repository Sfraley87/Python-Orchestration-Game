"""
Safely execute user code and run test cases against it.
Uses subprocess with a timeout to prevent runaway code.
"""

import subprocess
import sys
import os
import tempfile
import json
import textwrap
from pathlib import Path


RUNNER_TIMEOUT = 10  # seconds per test run


def run_challenge(challenge: dict, user_code: str) -> list[dict]:
    """
    Execute user_code and run the challenge's test cases.
    Returns list of result dicts: {passed, description, expected, got, error}
    """
    results = []
    for test in challenge["tests"]:
        result = _run_single_test(user_code, test, challenge.get("setup_code", ""))
        results.append(result)
    return results


def _run_single_test(user_code: str, test: dict, setup_code: str = "") -> dict:
    """Run a single test case in a subprocess sandbox."""
    assert_code = test.get("assert_code", "")
    description = test.get("description", "Test")

    # Build script via concatenation — NOT an f-string — so curly braces in
    # user/assert code are never interpreted as format variables.
    header = (
        "import sys, json, asyncio, os, re, time\n"
        "from pathlib import Path\n"
        "from unittest.mock import MagicMock, patch, AsyncMock\n"
    )
    trailer = (
        'try:\n'
        '    result = None\n'
        '    expected = None\n'
        + textwrap.indent(assert_code, "    ") + "\n"
        '    print(json.dumps({"passed": True,'
        ' "got": str(result) if result is not None else None,'
        ' "expected": str(expected) if expected is not None else None}))\n'
        'except AssertionError as e:\n'
        '    print(json.dumps({"passed": False, "error": str(e),'
        ' "got": str(result) if "result" in dir() else None,'
        ' "expected": str(expected) if "expected" in dir() else None}))\n'
        'except Exception as e:\n'
        '    print(json.dumps({"passed": False,'
        ' "error": type(e).__name__ + ": " + str(e)}))\n'
    )
    script = (
        header + "\n"
        "# --- setup ---\n"
        + setup_code + "\n\n"
        "# --- user code ---\n"
        + user_code + "\n\n"
        "# --- test ---\n"
        + trailer
    )

    try:
        proc = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            text=True,
            timeout=RUNNER_TIMEOUT,
            env={**os.environ, "PYTHONPATH": str(Path(__file__).parent.parent)},
        )
        output = proc.stdout.strip()
        stderr = proc.stderr.strip()

        if output:
            data = json.loads(output.splitlines()[-1])  # last line = result
            return {
                "description": description,
                "passed": data.get("passed", False),
                "expected": data.get("expected"),
                "got": data.get("got"),
                "error": data.get("error") or (stderr[:200] if not data.get("passed") else None),
            }
        else:
            return {
                "description": description,
                "passed": False,
                "error": stderr[:300] if stderr else "No output from test",
                "expected": None,
                "got": None,
            }
    except subprocess.TimeoutExpired:
        return {
            "description": description,
            "passed": False,
            "error": f"Timed out after {RUNNER_TIMEOUT}s",
            "expected": None,
            "got": None,
        }
    except Exception as e:
        return {
            "description": description,
            "passed": False,
            "error": str(e),
            "expected": None,
            "got": None,
        }


def score_results(results: list[dict], elapsed: float, time_limit: float = 900) -> int:
    """Calculate score 0-100."""
    if not results:
        return 0
    passed = sum(1 for r in results if r["passed"])
    base = int((passed / len(results)) * 80)
    # Speed bonus: up to 20 pts if finished in first 60% of time
    time_bonus = 0
    if passed == len(results):
        time_ratio = elapsed / time_limit
        if time_ratio < 0.6:
            time_bonus = int((1 - time_ratio / 0.6) * 20)
    return min(100, base + time_bonus)


def xp_for_score(score: int, difficulty: str) -> int:
    multipliers = {"easy": 1, "medium": 2, "hard": 3}
    mult = multipliers.get(difficulty, 1)
    return int((score / 100) * 50 * mult)
