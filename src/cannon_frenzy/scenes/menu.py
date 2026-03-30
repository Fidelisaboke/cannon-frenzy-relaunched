import sys
import pygame
from ..config.constants import (
    SCREEN_HEIGHT, SCREEN_WIDTH,
    FONT_TITLE, FONT_HUD,
    SIZE_TITLE, SIZE_HEADER, SIZE_HUD
)
from ..utils.paths import get_asset_path

class Menu:
    def __init__(self, screen, sound_manager):
        self.screen = screen
        self.sound_manager = sound_manager
        self.clock = pygame.time.Clock()

        # Fonts
        try:
            self.font = pygame.font.Font(get_asset_path(FONT_TITLE), SIZE_TITLE)
            self.small_font = pygame.font.Font(get_asset_path(FONT_HUD), SIZE_HUD)
        except (pygame.error, FileNotFoundError):
            self.font = pygame.font.Font(None, SIZE_TITLE)
            self.small_font = pygame.font.Font(None, SIZE_HUD)

        # Background images
        try:
            cloud_bg_path = get_asset_path("images/backgrounds/clouds.jpg")
            self.start_menu_bg_image = pygame.image.load(cloud_bg_path)
            self.start_menu_bg_image = pygame.transform.scale(self.start_menu_bg_image, (800, 600))

            night_sky_bg_path = get_asset_path("images/backgrounds/night_sky.jpg")
            self.game_over_menu_bg_image = pygame.image.load(night_sky_bg_path)
            self.game_over_menu_bg_image = pygame.transform.scale(self.game_over_menu_bg_image, (800, 600))
        except (pygame.error, FileNotFoundError) as e:
            print(f"Error loading menu backgrounds: {e}")
            self.start_menu_bg_image = pygame.Surface((800, 600))
            self.game_over_menu_bg_image = pygame.Surface((800, 600))

        # Pre-render static text surfaces (avoids allocating new surfaces every frame)
        self.title_text = self.font.render("Cannon Frenzy", True, "Black")
        self.title_rect = self.title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))

        self.start_text = self.small_font.render("Press S to Start", True, "Black")
        self.start_rect = self.start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    def start_menu(self):
        """Displays the game's start menu."""
        self.sound_manager.play_start_menu_music()

        while True:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                    self.sound_manager.stop_start_menu_music()
                    self.sound_manager.game_start_sound.play()
                    return

            # Draw menu background
            self.screen.blit(self.start_menu_bg_image, (0, 0))

            # Display game title (pre-rendered)
            self.screen.blit(self.title_text, self.title_rect)

            # Display start instructions (pre-rendered)
            self.screen.blit(self.start_text, self.start_rect)

            pygame.display.update()

    def game_over_menu(self, score):
        """Displays the Game over screen"""
        self.screen.blit(self.game_over_menu_bg_image, (0, 0))
        
        try:
            title_font = pygame.font.Font(get_asset_path(FONT_TITLE), SIZE_HEADER)
            hud_font = pygame.font.Font(get_asset_path(FONT_HUD), SIZE_HUD)
        except (pygame.error, FileNotFoundError):
            title_font = pygame.font.Font(None, SIZE_HEADER)
            hud_font = pygame.font.Font(None, SIZE_HUD)

        game_over_text = title_font.render("GAME OVER", True, "Red")
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 180))
        self.screen.blit(game_over_text, game_over_rect)

        score_text = hud_font.render(f"Final Score: {score}", True, "White")
        score_text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 260))
        self.screen.blit(score_text, score_text_rect)

        restart_text = hud_font.render("Press R to Restart", True, "Yellow")
        restart_text_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 360))
        self.screen.blit(restart_text, restart_text_rect)

        start_menu_text = hud_font.render("Press M for Menu", True, "White")
        start_menu_text_rect = start_menu_text.get_rect(center=(SCREEN_WIDTH // 2, 420))
        self.screen.blit(start_menu_text, start_menu_text_rect)

        pygame.display.update()
