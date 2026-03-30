""" This module initializes and manages the game. """

import sys
import pygame
from ..config.constants import SCREEN_WIDTH, SCREEN_HEIGHT
from ..config.levels import LEVELS_CONFIG
from ..entities.cannon import Cannon
from ..scenes.level import Level
from ..scenes.menu import Menu
from ..scenes.scoreboard import Scoreboard
from .sound import SoundManager
from ..utils.paths import get_asset_path


class CannonFrenzy:
    def __init__(self):
        # Pre-initialize mixer with a larger buffer; let Pygame match OS frequency
        pygame.mixer.pre_init(buffer=4096)

        # Initialize pygame modules
        pygame.init()
        pygame.mixer.init()

        # Stop the game if pygame fails to initialize
        if not pygame.get_init():
            print("Failed to initialize Pygame!")
            sys.exit()

        # Set game properties
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cannon Frenzy")
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.font = pygame.font.Font(None, 72)

        # Level configurations
        self.levels = [Level(self.screen, **config) for config in LEVELS_CONFIG]
        self.current_level_index = 0
        self.current_level = self.levels[self.current_level_index]

        # Scoreboard
        self.scoreboard = Scoreboard(self.screen)

        # Sound manager
        self.sound_manager = SoundManager()
        self.game_over_sound_played = False

        # Menu manager
        self.menu = Menu(self.screen, self.sound_manager)

        # Background Image
        try:
             self.level_bg_image = pygame.image.load(get_asset_path("images/backgrounds/grasslands.png"))
        except (pygame.error, FileNotFoundError):
             self.level_bg_image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

        # Initial properties -> Level 1
        self.score = 0
        self.game_over = False
        self.cannonballs = []
        self.cannon = Cannon(
            self.screen,
            self.cannonballs,
            self.current_level.cannonballs_left
        )

        # Combo tracker
        self.combo_count = 0
        self.max_combo_streak = 0

        # Flag for tracking background music
        self.background_music_playing = False

    def reset_game(self):
        """Resets the game state."""
        self.game_over_sound_played = False
        self.levels = [Level(self.screen, **config) for config in LEVELS_CONFIG]
        self.current_level_index = 0
        self.current_level = self.levels[self.current_level_index]
        self.score = 0
        self.game_over = False
        self.cannonballs = []
        self.cannon = Cannon(self.screen, self.cannonballs, self.current_level.cannonballs_left)
        self.combo_count = 0
        self.max_combo_streak = 0


    def run(self):
        """Runs the game."""
        # Start menu
        self.menu.start_menu()

        # Game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN and self.game_over:
                    # Press 'R' key to restart the game
                    if event.key == pygame.K_r:
                        self.reset_game()
                        self.sound_manager.game_start_sound.play()

                    # Press 'M' key to go back to the start menu
                    elif event.key == pygame.K_m:
                        self.reset_game()
                        self.menu.start_menu()

            # Game over condition
            if self.cannon.cannonballs_left == 0 and len(self.cannonballs) == 0:
                self.game_over = True

            if self.game_over:
                self.handle_game_over()
            else:
                # Determine background image according to level number
                try:
                    if self.current_level.level_number % 2 == 0:
                        self.level_bg_image = pygame.image.load(get_asset_path("images/backgrounds/desert.png"))
                    else:
                        self.level_bg_image = pygame.image.load(get_asset_path("images/backgrounds/grasslands.png"))
                except (pygame.error, FileNotFoundError):
                    pass # Keep previous or surface

                self.screen.blit(self.level_bg_image, (0, 0))
                self.cannon.draw()
                self.current_level.draw()

                for cannonball in self.cannonballs[:]:
                    cannonball.move()
                    cannonball.draw()

                    if cannonball.is_off_screen():
                        self.cannonballs.remove(cannonball)
                        self.combo_count = 0

                    for target in self.current_level.targets[:]:
                        if target.hit(cannonball):
                            self.sound_manager.target_hit_sound.play()
                            self.current_level.targets.remove(target)
                            self.cannonballs.remove(cannonball)
                            self.combo_count += 1
                            if self.combo_count > self.max_combo_streak:
                                self.max_combo_streak = self.combo_count
                            self.score += 10 + 5 * (self.combo_count - 1)
                            break

                # Check if all targets are hit
                if not self.current_level.targets:
                    self.current_level_index += 1
                    if self.current_level_index < len(self.levels):
                        self.current_level = self.levels[self.current_level_index]
                        cannonballs_left = self.current_level.cannonballs_left
                        self.cannon = Cannon(self.screen, self.cannonballs, cannonballs_left)

                # Display the scoreboard
                self.scoreboard.draw(
                    level_number=self.current_level.level_number,
                    score=self.score,
                    combo_count=self.combo_count,
                    max_combo_streak=self.max_combo_streak,
                    cannonballs_left=self.cannon.cannonballs_left
                )

                # Update the cannon sprite
                self.cannon.update()

            pygame.display.update()
            self.clock.tick(self.fps)

    def handle_game_over(self):
        """Displays the game over screen."""
        pygame.display.update()
        self.clock.tick(self.fps)
        pygame.time.delay(1000)

        # Game over sound
        if not self.game_over_sound_played:
            self.game_over_sound_played = True
            self.sound_manager.game_over_sound.play()

        # Draw the game over screen
        self.menu.game_over_menu(self.score)
