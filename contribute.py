from datetime import datetime, timedelta
from random import randint
from subprocess import Popen


def run(cmd):
    Popen(cmd).wait()


def message(date):
    return date.strftime("Contribution: %Y-%m-%d %H:%M")


def contribute(commit_time):
    with open("README.md", "a", encoding="utf-8") as f:
        f.write(message(commit_time) + "\n")

    run(["git", "add", "README.md"])
    run([
        "git",
        "commit",
        "-m",
        message(commit_time),
        "--date",
        commit_time.strftime("%Y-%m-%d %H:%M:%S")
    ])


def main():
    TOTAL_DAYS = 365
    MAX_COMMITS_PER_DAY = 5
    FREQUENCY = 70       # % chance per day
    SKIP_WEEKENDS = False

    # MUST match GitHub email
    run(["git", "config", "user.name", "codingwithsneha"])
    run(["git", "config", "user.email", "iamsneha@gmail.com"])

    today = datetime.now()
    start_date = today - timedelta(days=TOTAL_DAYS)

    for i in range(TOTAL_DAYS):
        day = start_date + timedelta(days=i)

        if SKIP_WEEKENDS and day.weekday() >= 5:
            continue

        if randint(1, 100) > FREQUENCY:
            continue

        commits_today = randint(1, MAX_COMMITS_PER_DAY)

        for _ in range(commits_today):
            commit_time = day.replace(
                hour=randint(9, 22),
                minute=randint(0, 59),
                second=randint(0, 59)
            )
            contribute(commit_time)

        run(["git", "push", "--force", "origin", "main"])
    print("✅ Contributions for last 365 days pushed successfully")


if __name__ == "__main__":
    main()
