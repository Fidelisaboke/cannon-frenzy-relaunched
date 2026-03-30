import pygame
from ..utils.paths import get_asset_path

class Target(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, width, height, color="Blue"):
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        try:
            target_image_path = get_asset_path("images/sprites/target.png")
            self.image = pygame.image.load(target_image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (width, height))
        except (pygame.error, FileNotFoundError) as e:
            print(f"Unable to load target image: {e}")
            self.image = pygame.Surface((width, height))
            self.image.fill(pygame.Color(color))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def hit(self, cannonball):
        """ Checks if the target has been hit by a cannonball.
        :param cannonball: Cannonball to check.
        """
        return (
            self.x < cannonball.x < self.x + self.width and
            self.y < cannonball.y < self.y + self.height
        )
