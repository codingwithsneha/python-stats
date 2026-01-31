#!/usr/bin/env python
import argparse
import os
import sys
from datetime import datetime, timedelta
from random import randint
from subprocess import Popen


def run(cmd):
    Popen(cmd).wait()


def message(date):
    return date.strftime("Contribution: %Y-%m-%d %H:%M")


def contributions_per_day(args):
    return randint(1, min(args.max_commits, 20))


def contribute(date):
    with open("README.md", "a", encoding="utf-8") as f:
        f.write(message(date) + "\n")

    run(["git", "add", "README.md"])
    run([
        "git",
        "commit",
        "-m",
        message(date),
        "--date",
        date.strftime("%Y-%m-%d %H:%M:%S")
    ])


def arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-nw", "--no_weekends", action="store_true")
    parser.add_argument("-mc", "--max_commits", type=int, default=10)
    parser.add_argument("-fr", "--frequency", type=int, default=80)
    parser.add_argument("-db", "--days_before", type=int, default=20)
    parser.add_argument("-da", "--days_after", type=int, default=0)
    return parser.parse_args(argv)


def main(argv=sys.argv[1:]):
    args = arguments(argv)

    repo_url = "https://github.com/codingwithsneha/grow-project.git"
    repo_name = "grow-project"

    if not os.path.exists(repo_name):
        run(["git", "clone", repo_url])

    os.chdir(repo_name)

    run(["git", "config", "user.name", "codingwithsneha"])
    run(["git", "config", "user.email", "iamsneha@gmail.com"])

    start_date = datetime.now() - timedelta(days=args.days_before)
    total_days = args.days_before + args.days_after

    for i in range(total_days):
        day = start_date + timedelta(days=i)

        if args.no_weekends and day.weekday() >= 5:
            continue

        if randint(0, 100) > args.frequency:
            continue

        for _ in range(contributions_per_day(args)):
            contribute(day)

    run(["git", "pull", "--rebase", "origin", "main"])
    run(["git", "push", "origin", "main"])

    print("✅ Repository updated successfully")


if __name__ == "__main__":
    main()
