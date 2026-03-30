import pygame
import math
from ..config.constants import SCREEN_HEIGHT, MIN_POWER, MAX_POWER, POWER_CHARGE_SPEED
from ..utils.paths import get_asset_path
from .ball import Cannonball

class Cannon(pygame.sprite.Sprite):
    def __init__(self, screen, cannonballs, cannonballs_left, particles):
        super().__init__()
        self.screen = screen
        self.cannonballs = cannonballs
        self.cannonballs_left = cannonballs_left
        self.particles = particles
        
        # Power states
        self.current_power = MIN_POWER
        self.is_charging = False
        self.charge_direction = 1
        
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
        
        # Power meter
        self.draw_power_meter()

    def draw_power_meter(self):
        """Draws a power meter when charging."""
        if self.is_charging:
            bar_width = 60
            bar_height = 10
            bar_x = self.x - bar_width // 2
            bar_y = self.y - 70
            
            # Border/Background
            pygame.draw.rect(self.screen, (50, 50, 50), (bar_x - 2, bar_y - 2, bar_width + 4, bar_height + 4))
            pygame.draw.rect(self.screen, (100, 100, 100), (bar_x, bar_y, bar_width, bar_height))
            
            # Fill
            power_range = MAX_POWER - MIN_POWER
            power_ratio = (self.current_power - MIN_POWER) / power_range
            fill_width = int(bar_width * power_ratio)
            
            # Color transition (Green -> Yellow -> Red)
            if power_ratio < 0.5:
                color = (int(510 * power_ratio), 255, 0)
            else:
                color = (255, int(510 * (1 - power_ratio)), 0)
                
            pygame.draw.rect(self.screen, color, (bar_x, bar_y, fill_width, bar_height))

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
            
        # Hold-to-charge firing logic
        can_fire = len(self.cannonballs) == 0 and self.cannonballs_left > 0
        
        if keys[pygame.K_SPACE] and can_fire:
            if not self.is_charging:
                self.is_charging = True
                self.current_power = MIN_POWER
                self.charge_direction = 1
            else:
                # Update power charge with oscillation
                self.current_power += self.charge_direction * POWER_CHARGE_SPEED
                if self.current_power >= MAX_POWER:
                    self.current_power = MAX_POWER
                    self.charge_direction = -1
                elif self.current_power <= MIN_POWER:
                    self.current_power = MIN_POWER
                    self.charge_direction = 1
        elif self.is_charging:
            # Release Space to Fire
            if self.cannon_fire_sound:
                self.cannon_fire_sound.play()
            
            # Spawn muzzle smoke
            self.particles.spawn_smoke(self.x, self.y, self.angle)
            
            self.cannonballs.append(Cannonball(self.screen, self.x, self.y, self.angle, self.current_power))
            self.cannonballs_left -= 1
            self.is_charging = False
            self.current_power = MIN_POWER

    def update(self):
        self.move()
