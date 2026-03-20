#!/usr/bin/env python3
"""
Synelium Coding Game - 15 min/day Python practice
Topics: APIs, Automation, Async/Orchestration, LangChain/LangGraph
"""

import sys
import argparse
from engine.session import Session
from engine.progress import Progress
from engine.display import Display


def main():
    parser = argparse.ArgumentParser(
        description="Synelium Coding Game - 15 min daily Python practice"
    )
    parser.add_argument(
        "command",
        nargs="?",
        default="play",
        choices=["play", "stats", "list", "replay", "hint"],
        help="Command to run (default: play)",
    )
    parser.add_argument(
        "--category",
        "-c",
        choices=["api", "automation", "async", "langchain", "random"],
        default="random",
        help="Challenge category",
    )
    parser.add_argument(
        "--difficulty",
        "-d",
        choices=["easy", "medium", "hard"],
        default=None,
        help="Difficulty filter",
    )
    parser.add_argument(
        "--id",
        type=str,
        help="Specific challenge ID to play or replay",
    )
    parser.add_argument(
        "--list-solutions",
        action="store_true",
        help="Show solution after completing a challenge",
    )

    args = parser.parse_args()
    display = Display()

    if args.command == "stats":
        progress = Progress()
        display.show_stats(progress.get_stats())
        return

    if args.command == "list":
        from challenges import get_all_challenges
        challenges = get_all_challenges()
        progress = Progress()
        display.list_challenges(challenges, progress)
        return

    # Default: play
    session = Session(
        category=args.category,
        difficulty=args.difficulty,
        challenge_id=args.id,
        show_solution=args.list_solutions,
    )
    session.run()


if __name__ == "__main__":
    main()
