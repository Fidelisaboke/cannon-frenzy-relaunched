import os
import sys

from .core.game import CannonFrenzy

def main():
    try:
        game = CannonFrenzy()
        game.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
