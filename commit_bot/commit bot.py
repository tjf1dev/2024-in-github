import os
import subprocess
from datetime import datetime, timedelta
import threading
import progressbarlib
from colorama import Fore
import sys  # Needed for flushing output

def check_git_repo():
    """Check if the current directory is a Git repository."""
    try:
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("Error: No Git repository found in the current directory.")
        print("Solution: Run 'git init' and restart the script.")
        exit(1)

def commit_range(start, end):
    """Make a commit for each day in the given range and update progress."""
    total_days = (end - start).days + 1  # Total number of commits needed
    completed = 0  # Track completed commits
    delta = timedelta(days=1)

    while start <= end:
        date_str = start.strftime('%Y-%m-%d 12:00:00')
        env = os.environ.copy()
        env['GIT_COMMITTER_DATE'] = date_str
        env['GIT_AUTHOR_DATE'] = date_str
        try:
            with open("commit.txt", "a") as f:
                f.write(f"Commit for {date_str}\n")
            
            # Suppress Git output
            subprocess.run(["git", "add", "commit.txt"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env)
            subprocess.run(["git", "commit", "-m", f"Automated commit for {date_str}"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env)

        except subprocess.CalledProcessError as e:
            print(f"Error during commit on {date_str}: {e}")
            exit(1)

        completed += 1
        percentage = (completed / total_days) * 100

        # Overwrite the same line instead of printing new lines
        sys.stdout.write(f"\r{progressbarlib.Bar.from_percentage(int(percentage), color=Fore.GREEN)} {int(percentage)}%")
        sys.stdout.flush()  # Force output update

        start += delta

def main():
    print("Git Commit Bot")
    year = input("Year > ")

    check_git_repo()

    start = input(f"The script will make a commit for every day in {year}. This can take a while. Start? (y/N) > ")
    if start.lower() != 'y':
        print("Aborted.")
        exit(0)

    start_date, end_date = datetime(int(year), 1, 1), datetime(int(year), 12, 31)
    total_days = (end_date - start_date).days + 1

    print(f"Total commits to be made: {total_days}")

    # Start commit process
    thread = threading.Thread(target=commit_range, args=(start_date, end_date))
    thread.start()
    thread.join()

    print("\nAll commits completed.")
    print("Next step: Run 'git push origin <branch>' to push your commits to GitHub.")

if __name__ == "__main__":
    main()
