#!/usr/bin/env python3
"""
Synelium Coding Game — Flask web app for playing on mobile/browser.
Run: python web_app.py
Then open http://<your-ip>:5000 on your phone.
"""

import random
from flask import Flask, request, jsonify, render_template

from engine.runner import run_challenge, score_results, xp_for_score
from engine.progress import Progress
from challenges import get_all_challenges, get_by_category, get_by_id

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/challenge")
def api_challenge():
    category = request.args.get("category", "random")
    difficulty = request.args.get("difficulty")
    challenge_id = request.args.get("id")

    progress = Progress()

    if challenge_id:
        challenge = get_by_id(challenge_id)
    else:
        pool = get_by_category(category) if category != "random" else get_all_challenges()
        if difficulty:
            pool = [c for c in pool if c["difficulty"] == difficulty]

        completed = set(progress.data.get("completed_ids", []))
        fresh = [c for c in pool if c["id"] not in completed]
        challenge = random.choice(fresh if fresh else pool) if pool else None

    if not challenge:
        return jsonify({"error": "No challenges found"}), 404

    return jsonify({
        "id": challenge["id"],
        "title": challenge["title"],
        "category": challenge["category"],
        "difficulty": challenge["difficulty"],
        "description": challenge["description"],
        "context": challenge.get("context", ""),
        "starter_code": challenge["starter_code"],
        "hint_count": len(challenge.get("hints", [])),
    })


@app.route("/api/submit", methods=["POST"])
def api_submit():
    data = request.get_json()
    challenge_id = data.get("challenge_id")
    user_code = data.get("code", "")
    elapsed = data.get("elapsed", 0)

    challenge = get_by_id(challenge_id)
    if not challenge:
        return jsonify({"error": "Challenge not found"}), 404

    results = run_challenge(challenge, user_code)
    score = score_results(results, elapsed)
    xp = xp_for_score(score, challenge["difficulty"])

    progress = Progress()
    progress.record_attempt(challenge_id, score, xp, elapsed)

    passed = sum(1 for r in results if r["passed"])
    all_passed = passed == len(results)

    return jsonify({
        "results": results,
        "score": score,
        "xp": xp,
        "streak": progress.data.get("streak", 1),
        "passed": passed,
        "total": len(results),
        "solution": challenge.get("solution", "") if not all_passed else None,
    })


@app.route("/api/hint/<challenge_id>/<int:hint_index>")
def api_hint(challenge_id, hint_index):
    challenge = get_by_id(challenge_id)
    if not challenge:
        return jsonify({"error": "Challenge not found"}), 404

    hints = challenge.get("hints", [])
    if not hints:
        return jsonify({"hint": None})

    return jsonify({
        "hint": hints[hint_index % len(hints)],
        "index": hint_index,
        "total": len(hints),
    })


@app.route("/api/session/start", methods=["POST"])
def api_session_start():
    progress = Progress()
    progress.start_session()
    return jsonify({"streak": progress.data.get("streak", 1)})


@app.route("/api/session/end", methods=["POST"])
def api_session_end():
    data = request.get_json() or {}
    progress = Progress()
    progress.end_session({
        "attempted": data.get("attempted", 0),
        "passed": data.get("passed", 0),
        "xp": data.get("xp", 0),
        "duration": data.get("duration", 0),
    })
    return jsonify({"ok": True})


@app.route("/api/stats")
def api_stats():
    progress = Progress()
    return jsonify(progress.get_stats())


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5000)
    args = parser.parse_args()
    print(f"\n  Open http://{args.host}:{args.port} in your browser / phone\n")
    app.run(host=args.host, port=args.port, debug=False)
