import os
import subprocess
from datetime import datetime, timedelta
import threading
from colorama import Fore
import sys
from colorama import Fore, init
init(autoreset=True)
class Bar(object):
    """contains functions for all progress bars"""
    def from_percentage(percentage: int, color=Fore.WHITE, char="██", bar_length=10):
        """creates a progress bar from a percentage."""
        if not (0 <= percentage <= 100):
            raise ValueError("percentage must be between 0 and 100")
        segments = round((percentage / 100) * bar_length)
        raw_text = char * segments
        padded_bar = raw_text.ljust(bar_length * len(char))
        
        return color + padded_bar + Fore.RESET
def check_git_repo():
    """check if the current directory is a git repository."""
    try:
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("error: no git repository found in the current directory.")
        print("solution: run 'git init' and restart the script.")
        exit(1)

def commit_range(start, end):
    """Make a commit for each day in the given range and update progress."""
    total_days = (end - start).days + 1  # total number of commits needed
    completed = 0  # track completed commits
    delta = timedelta(days=1)

    while start <= end:
        date_str = start.strftime('%Y-%m-%d 12:00:00')
        env = os.environ.copy()
        env['GIT_COMMITTER_DATE'] = date_str
        env['GIT_AUTHOR_DATE'] = date_str
        try:
            with open("commit.txt", "a") as f:
                f.write(f"Commit for {date_str}\n")
            
            # suppress git output
            subprocess.run(["git", "add", "commit.txt"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env)
            subprocess.run(["git", "commit", "-m", f"Automated commit for {date_str}"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env)

        except subprocess.CalledProcessError as e:
            print(f"error during commit on {date_str}: {e}")
            exit(1)

        completed += 1
        percentage = (completed / total_days) * 100

        # overwrite the same line instead of printing new lines
        sys.stdout.write(f"\r{Bar.from_percentage(int(percentage), color=Fore.GREEN)} {int(percentage)}%")
        sys.stdout.flush()  # force output update

        start += delta

def main():
    print("2024-in-github")
    year = input("year > ")

    check_git_repo()

    start = input(f"the script will make a commit for every day in {year}. this can take a while. start? (y/N) > ")
    if start.lower() != 'y':
        print("Aborted.")
        exit(0)

    start_date, end_date = datetime(int(year), 1, 1), datetime(int(year), 12, 31)
    total_days = (end_date - start_date).days + 1

    print(f"total commits to be made: {total_days}")

    # start commit process
    thread = threading.Thread(target=commit_range, args=(start_date, end_date))
    thread.start()
    thread.join()

    print("\nall commits completed.")
    print("next step: run 'git push origin <branch>' to push your commits to git.")

if __name__ == "__main__":
    main()
