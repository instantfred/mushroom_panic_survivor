import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
import os

TITLE_SIZE = 48

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 10 # Frames per second
        self.image = None
        self.speed = 200  # pixels per second

        # Load and slice animations
        self.animations = {
            'idle': self.load_animation('player_idle.png', 9),
            'walk': self.load_animation('player_walk.png', 4),
        }

        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)


    def load_animation(self, filename, num_frames):
        path = os.path.join('assets', 'sprites', filename)
        sprite_sheet = pygame.image.load(path).convert_alpha()
        print(f"Loading {filename}: {sprite_sheet.get_width()}x{sprite_sheet.get_height()}")
        return [sprite_sheet.subsurface(pygame.Rect(i * TITLE_SIZE, 0, TITLE_SIZE, TITLE_SIZE))
                for i in range(num_frames)]


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
    

    def animate(self, dt):
        frames = self.animations[self.status]
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(frames):
            self.frame_index = 0
        self.image = frames[int(self.frame_index)]

    
    def update(self, dt):
        direction = self.handle_input()
        if direction.length() == 0:
            self.status = 'idle'
        else:
            self.status = 'walk'
            self.rect.x += direction.x * self.speed * dt
            self.rect.y += direction.y * self.speed * dt
            self.rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

        self.animate(dt)