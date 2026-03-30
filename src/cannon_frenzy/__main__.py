import os
import sys

# Add the project root to sys.path so we can import 'src' if needed, 
# but usually we run as 'python -m src.cannon_frenzy'
# Force Pygame to connect directly to the PulseAudio server to fix WSL stuttering
os.environ['SDL_AUDIODRIVER'] = 'pulseaudio'

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
