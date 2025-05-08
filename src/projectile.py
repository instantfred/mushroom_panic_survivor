import pygame
from settings import TILE_SIZE

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, direction, speed, lifespan, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2(direction).normalize()
        self.speed = speed
        self.spawn_time = pygame.time.get_ticks()
        self.lifespan = lifespan  # in milliseconds

    def update(self, dt):
        # Move projectile
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt

        # Check lifespan
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifespan:
            self.kill()
