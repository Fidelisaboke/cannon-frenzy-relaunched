import os
# Force Pygame to connect directly to the PulseAudio server to fix WSL stuttering
os.environ['SDL_AUDIODRIVER'] = 'pulseaudio'

from cannon_frenzy import CannonFrenzy

if __name__ == '__main__':
    CannonFrenzy().run()