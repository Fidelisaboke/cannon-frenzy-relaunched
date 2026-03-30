import pygame
import random
import math

class Particle:
    """A single visual particle with physics and lifetime."""
    def __init__(self, x, y, vx, vy, color, lifetime, size, gravity=0.1, friction=0.98):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.color = pygame.Color(color)
        self.max_lifetime = lifetime
        self.lifetime = lifetime
        self.size = size
        self.gravity = gravity
        self.friction = friction

    def update(self):
        """Update particle physics and lifetime."""
        self.vx *= self.friction
        self.vy *= self.friction
        self.vy += self.gravity
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1

    def is_alive(self):
        """Return True if particle still has lifetime."""
        return self.lifetime > 0

    def draw(self, screen):
        """Render the particle with a shrinking effect as it ages."""
        if not self.is_alive():
            return
        
        # Simple shrinking effect to simulate fading/dissipating
        current_size = max(1, int(self.size * (self.lifetime / self.max_lifetime)))
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), current_size)

class ParticleManager:
    """Manages collections of particles for various effects."""
    def __init__(self):
        self.particles = []

    def spawn_smoke(self, x, y, angle):
        """Spawns grey smoke drifting away from the muzzle."""
        for _ in range(8):
            angle_rad = math.radians(angle)
            # Spawn at muzzle end (barrel length ~50)
            dist = 45 
            start_x = x + dist * math.cos(angle_rad)
            start_y = y - dist * math.sin(angle_rad)
            
            # Direct drift + random spread
            speed = random.uniform(0.5, 2.0)
            spread_angle = angle_rad + random.uniform(-0.2, 0.2)
            vx = math.cos(spread_angle) * speed + random.uniform(-0.5, 0.5)
            vy = -math.sin(spread_angle) * speed + random.uniform(-1.0, 0.0)
            
            grey_val = random.randint(150, 220)
            self.particles.append(Particle(
                start_x, start_y, vx, vy, 
                color=(grey_val, grey_val, grey_val), 
                lifetime=random.randint(30, 60), 
                size=random.uniform(5, 12), 
                gravity=-0.03  # Smoke slightly rises
            ))

    def spawn_explosion(self, x, y, color):
        """Spawns a burst of colorful debris from an impact point."""
        for _ in range(15):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2.0, 6.0)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            
            self.particles.append(Particle(
                x, y, vx, vy, 
                color=color, 
                lifetime=random.randint(20, 50), 
                size=random.uniform(3, 8), 
                gravity=0.15  # Debris falls
            ))

    def update(self):
        """Update all managed particles and remove dead ones."""
        for p in self.particles[:]:
            p.update()
            if not p.is_alive():
                self.particles.remove(p)

    def draw(self, screen):
        """Draw all particles to the screen."""
        for p in self.particles:
            p.draw(screen)
