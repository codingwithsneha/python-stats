import argparse
import sys
from datetime import datetime, timedelta
from random import randint
from subprocess import Popen


def run(cmd):
    p = Popen(cmd)
    p.wait()


def message(date):
    return date.strftime("Contribution: %Y-%m-%d %H:%M")


def contributions_per_day(max_commits):
    return randint(1, min(max_commits, 20))


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
    parser = argparse.ArgumentParser(description="Generate GitHub contributions for last 365 days")
    parser.add_argument("-mc", "--max_commits", type=int, default=8, help="max commits per day")
    parser.add_argument("-fr", "--frequency", type=int, default=70, help="chance per day (0-100)")
    parser.add_argument("-nw", "--no_weekends", action="store_true")
    return parser.parse_args(argv)


def main(argv=sys.argv[1:]):
    args = arguments(argv)

    if not (run(["git", "rev-parse", "--is-inside-work-tree"]) is None):
        pass

    # IMPORTANT: email MUST match GitHub email
    run(["git", "config", "user.name", "codingwithsneha"])
    run(["git", "config", "user.email", "iamsneha@gmail.com"])

    today = datetime.now()
    start_date = today - timedelta(days=365)

    for i in range(365):
        day = start_date + timedelta(days=i)

        if args.no_weekends and day.weekday() >= 5:
            continue

        if randint(1, 100) > args.frequency:
            continue

        commits_today = contributions_per_day(args.max_commits)

        for n in range(commits_today):
            commit_time = day.replace(
                hour=randint(9, 22),
                minute=randint(0, 59)
            )
            contribute(commit_time)

    run(["git", "pull", "--rebase", "origin", "main"])
    run(["git", "push", "origin", "main"])

    print("✅ 365 days of contributions pushed successfully")


if __name__ == "__main__":
    main()
