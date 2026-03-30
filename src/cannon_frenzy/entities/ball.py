import pygame
import math
from ..config.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Cannonball(pygame.sprite.Sprite):
    def __init__(self, screen, x, y, angle, power):
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.radius = 8
        self.speed_x = power * math.cos(math.radians(angle))
        self.speed_y = -power * math.sin(math.radians(angle))
        self.gravity = 0.5  # Gravity effect

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.speed_y += self.gravity  # Simulate gravity

    def draw(self):
        pygame.draw.circle(self.screen, "Black", (int(self.x), int(self.y)), self.radius)

    def is_off_screen(self):
        """ Checks if the cannonball is off-screen. """
        return self.x > SCREEN_WIDTH or self.y > SCREEN_HEIGHT
