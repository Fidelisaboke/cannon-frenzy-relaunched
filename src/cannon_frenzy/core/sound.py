import pygame
from ..utils.paths import get_asset_path

class SoundManager:
    def __init__(self):
        try:
            self.game_start_sound = pygame.mixer.Sound(get_asset_path("audio/sfx/game_start.wav"))
            self.game_start_sound.set_volume(0.5)

            self.game_over_sound = pygame.mixer.Sound(get_asset_path("audio/sfx/game_over.wav"))
            self.game_over_sound.set_volume(0.5)

            self.target_hit_sound = pygame.mixer.Sound(get_asset_path("audio/sfx/target_hit.ogg"))
            self.target_hit_sound.set_volume(0.5)

            # Level Transition sound
            self.level_entry_sound = pygame.mixer.Sound(get_asset_path("audio/music/mixkit-game-level-completed-2059.wav"))
            self.level_entry_sound.set_volume(0.5)
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading sounds: {e}")
            # Mock objects if loading fails to prevent crash
            mock_sound = pygame.mixer.Sound(buffer=b'\x00' * 44) # Minimal silent sound
            self.game_start_sound = mock_sound
            self.game_over_sound = mock_sound
            self.target_hit_sound = mock_sound
            self.level_entry_sound = mock_sound

    def play_start_menu_music(self):
        try:
            pygame.mixer.music.load(get_asset_path("audio/music/mixkit-games-music-706.mp3"))
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(loops=-1)
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading music: {e}")

    def stop_start_menu_music(self):
        pygame.mixer.music.stop()
