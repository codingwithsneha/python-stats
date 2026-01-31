# import sys
# from datetime import datetime, timedelta
# from random import randint
# from subprocess import Popen


# # ---------- helpers ----------
# def run(cmd):
#     p = Popen(cmd)
#     p.wait()


# def message(date):
#     return date.strftime("Contribution: %Y-%m-%d %H:%M")


# def contribute(commit_time):
#     with open("README.md", "a", encoding="utf-8") as f:
#         f.write(message(commit_time) + "\n")

#     run(["git", "add", "README.md"])
#     run([
#         "git",
#         "commit",
#         "-m",
#         message(commit_time),
#         "--date",
#         commit_time.strftime("%Y-%m-%d %H:%M:%S")
#     ])


# # ---------- main ----------
# def main():
#     # CONFIG — safe & realistic
#     TOTAL_DAYS = 365
#     MAX_COMMITS_PER_DAY = 5
#     FREQUENCY = 70          # % of days that get commits
#     SKIP_WEEKENDS = False

#     # IMPORTANT: must match GitHub email
#     run(["git", "config", "user.name", "codingwithsneha"])
#     run(["git", "config", "user.email", "iamsneha@gmail.com"])

#     today = datetime.now()
#     start_date = today - timedelta(days=TOTAL_DAYS)

#     for i in range(TOTAL_DAYS):
#         day = start_date + timedelta(days=i)

#         if SKIP_WEEKENDS and day.weekday() >= 5:
#             continue

#         if randint(1, 100) > FREQUENCY:
#             continue

#         commits_today = randint(1, MAX_COMMITS_PER_DAY)

#         for _ in range(commits_today):
#             commit_time = day.replace(
#                 hour=randint(9, 22),
#                 minute=randint(0, 59),
#                 second=randint(0, 59)
#             )
#             contribute(commit_time)

#     run(["git", "pull", "--rebase", "origin", "main"])
#     run(["git", "push", "origin", "main"])

#     print("✅ Contributions for last 365 days pushed successfully")


# if __name__ == "__main__":
#     main()



#!/usr/bin/env python
import argparse
import os
from datetime import datetime, timedelta
from random import randint
from subprocess import Popen, check_output
import sys
import unittest


def main(def_args=sys.argv[1:]):
    args = arguments(def_args)
    curr_date = datetime.now()
    directory = 'repository-' + curr_date.strftime('%Y-%m-%d-%H-%M-%S')
    repository = "https://github.com/codingwithsneha/python-stats.git"
    user_name = "codingwithsneha"
    user_email = "iamsneha@gmail.com"
    
    if repository is not None:
        start = repository.rfind('/') + 1
        end = repository.rfind('.')
        directory = repository[start:end]
    no_weekends = args.no_weekends
    frequency = args.frequency
    days_before = args.days_before
    if days_before < 0:
        sys.exit('days_before must not be negative')
    days_after = args.days_after
    if days_after < 0:
        sys.exit('days_after must not be negative')
    if not os.path.exists(directory):
        os.mkdir(directory)
    os.chdir(directory)
    run(['git', 'init', '-b', 'main'])

    run(['git', 'config', 'user.name', user_name])
    run(['git', 'config', 'user.email', user_email])

    run(['git', 'remote', 'remove', 'origin'])
    run(['git', 'remote', 'add', 'origin', repository])
    
    run(['git', 'fetch', 'origin'])
    run(['git', 'reset', '--hard', 'origin/main'])

    start_date = curr_date.replace(hour=20, minute=0) - timedelta(days_before)
    for day in (start_date + timedelta(n) for n in range(days_before + days_after)):
        if (not no_weekends or day.weekday() < 5) and randint(0, 100) < frequency:
            for commit_time in (day + timedelta(minutes=m) for m in range(contributions_per_day(args))):
                contribute(commit_time)

    run(['git', 'pull', '--rebase', 'origin', 'main'])
    run(['git', 'push', '-u', 'origin', 'main'])

    print('\nRepository generation ' + '\x1b[6;30;42mcompleted successfully\x1b[0m!')

def contribute(date):
    with open(os.path.join(os.getcwd(), 'README.md'), 'a') as file:
        file.write(message(date) + '\n\n')
    run(['git', 'add', '.'])
    run(['git', 'commit', '-m', message(date), '--date', date.strftime('"%Y-%m-%d %H:%M:%S"')])

def run(commands):
    Popen(commands).wait()

def message(date):
    return date.strftime('Contribution: %Y-%m-%d %H:%M')

def contributions_per_day(args):
    max_c = args.max_commits
    return randint(1, min(max_c, 20))

def arguments(argsval):
    parser = argparse.ArgumentParser()
    parser.add_argument('-nw', '--no_weekends', action='store_true', default=False)
    parser.add_argument('-mc', '--max_commits', type=int, default=10)
    parser.add_argument('-fr', '--frequency', type=int, default=80)
    parser.add_argument('-r', '--repository', type=str)
    parser.add_argument('-db', '--days_before', type=int, default=365)
    parser.add_argument('-da', '--days_after', type=int, default=0)
    return parser.parse_args(argsval)

if __name__ == "__main__":
    main()