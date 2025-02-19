from colorama import Fore, init
import time, random

init(autoreset=True)

class Bar(object):
    """Contains functions for all progress bars"""
    def from_percentage(percentage: int, color=Fore.WHITE, char="██", bar_length=10):
        """Creates a progress bar from a percentage."""
        if not (0 <= percentage <= 100):
            raise ValueError("Percentage must be between 0 and 100")
        segments = round((percentage / 100) * bar_length)
        raw_text = char * segments
        padded_bar = raw_text.ljust(bar_length * len(char))
        
        return color + padded_bar + Fore.RESET
    
if __name__ == "__main__":
    print("progressbarlib is not meant to be run directly. please import it in your script :3")