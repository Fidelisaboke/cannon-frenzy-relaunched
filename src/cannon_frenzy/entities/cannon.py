import pygame
import math
from ..config.constants import SCREEN_HEIGHT
from ..utils.paths import get_asset_path
from .ball import Cannonball

class Cannon(pygame.sprite.Sprite):
    def __init__(self, screen, cannonballs, cannonballs_left, power=25):
        super().__init__()
        self.screen = screen
        self.cannonballs = cannonballs
        self.cannonballs_left = cannonballs_left
        self.power = power
        self.x = 100
        self.y = SCREEN_HEIGHT - 60
        self.angle = 45

        # Cannon fire sound
        cannon_fire_path = get_asset_path("audio/sfx/cannon_fire.ogg")
        try:
            self.cannon_fire_sound = pygame.mixer.Sound(cannon_fire_path)
            self.cannon_fire_sound.set_volume(0.5)
        except (pygame.error, FileNotFoundError) as e:
            print(f"Unable to load cannon fire sound: {e}")
            self.cannon_fire_sound = None

    def draw(self):
        # Cannon base
        pygame.draw.rect(self.screen, "Black", (self.x - 10, self.y - 30, 20, 30))

        # Cannon barrel
        cannon_length = 50
        end_x = self.x + cannon_length * math.cos(math.radians(self.angle))
        end_y = self.y - cannon_length * math.sin(math.radians(self.angle))
        pygame.draw.line(self.screen, "Red", (self.x, self.y), (end_x, end_y), 5)

    def adjust_angle(self, change):
        """ Adjusts the cannon barrel's angle.
        :param change: Angle to adjust.
        """
        self.angle = max(10, min(80, self.angle + change))  # Restrict angle between 10° and 80°

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.adjust_angle(1)
        if keys[pygame.K_DOWN]:
            self.adjust_angle(-1)
        if keys[pygame.K_SPACE] and len(self.cannonballs) == 0 and self.cannonballs_left > 0:
            if self.cannon_fire_sound:
                self.cannon_fire_sound.play()
            self.cannonballs.append(Cannonball(self.screen, self.x, self.y, self.angle, self.power))
            self.cannonballs_left -= 1

    def update(self):
        self.move()
