import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
import os

TITLE_SIZE = 48

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, obstacles):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 10 # Frames per second
        self.image = None
        self.speed = 200  # pixels per second
        self.facing_left = False
        self.map_bounds = None  # Will be set by Level class
        self.obstacles = obstacles

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
            self.facing_left = True
            direction.x = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.facing_left = False
            direction.x = 1

        if direction.length() > 0:
            direction = direction.normalize()
        return direction
    

    def move_and_collide(self, direction, dt):
        # Store original position
        original_x = self.rect.x
        original_y = self.rect.y

        # Try moving on X axis first
        self.rect.x += direction.x * self.speed * dt
        for sprite in self.obstacles:
            if self.rect.colliderect(sprite.rect):
                self.rect.x = original_x
                break

        # Then try moving on Y axis
        self.rect.y += direction.y * self.speed * dt
        for sprite in self.obstacles:
            if self.rect.colliderect(sprite.rect):
                self.rect.y = original_y
                break

        # Ensure we stay within map bounds
        if self.map_bounds:
            self.rect.clamp_ip(self.map_bounds)

    
    def animate(self, dt):
        frames = self.animations[self.status]
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(frames):
            self.frame_index = 0

        frame = frames[int(self.frame_index)]
        if self.facing_left:
            frame = pygame.transform.flip(frame, True, False)
        self.image = frame

    
    def update(self, dt):
        direction = self.handle_input()
        self.status = "walk" if direction.length() > 0 else "idle"
        self.move_and_collide(direction, dt)
        self.animate(dt)