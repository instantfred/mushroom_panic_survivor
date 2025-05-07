import pygame

from settings import SCREEN_HEIGHT, SCREEN_WIDTH


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((40, 40))  # Placeholder: simple square
        self.image.fill((255, 200, 0))  # Yellow mushroom-ish color
        self.rect = self.image.get_rect(center=pos)
        self.speed = 200  # pixels per second

    def handle_input(self):
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            direction.y = -1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            direction.y = 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            direction.x = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            direction.x = 1

        if direction.length() > 0:
            direction = direction.normalize()
        return direction

    def update(self, dt):
        direction = self.handle_input()
        self.rect.x += direction.x * self.speed * dt
        self.rect.y += direction.y * self.speed * dt

        # Keep player within bounds
        self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
