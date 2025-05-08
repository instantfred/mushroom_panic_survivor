import pygame
import os
from settings import TILE_SIZE
from weapon import Weapon

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, obstacles, projectile_group):
        super().__init__()
        self.frame_index = 0
        self.animation_speed = 10  # Frames per second
        self.image = None
        self.speed = 200  # pixels per second
        self.facing_left = False
        self.map_bounds = None  # Will be set by Level class
        self.obstacles = obstacles
        self.last_direction = (1, 0)  # Default to right direction

        # Load and slice animations
        self.animations = {
            'idle': self.load_animation('player_idle.png', 9),
            'walk': self.load_animation('player_walk.png', 4),
        }
        # Cache flipped frames
        self.flipped_animations = {
            'idle': [pygame.transform.flip(frame, True, False) for frame in self.animations['idle']],
            'walk': [pygame.transform.flip(frame, True, False) for frame in self.animations['walk']]
        }

        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # Set up projectile image and weapon
        self.projectile_image = pygame.Surface((16, 16))
        self.projectile_image.fill("yellow")

        self.weapon = Weapon(
            owner=self,
            projectile_group=projectile_group,
            image=self.projectile_image
        )

    def load_animation(self, filename, num_frames):
        path = os.path.join('assets', 'sprites', filename)
        sprite_sheet = pygame.image.load(path).convert_alpha()
        print(f"Loading {filename}: {sprite_sheet.get_width()}x{sprite_sheet.get_height()}")
        return [sprite_sheet.subsurface(pygame.Rect(i * TILE_SIZE, 0, TILE_SIZE, TILE_SIZE))
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
            self.last_direction = (direction.x, direction.y)  # Store the last valid direction
        return direction

    def move_and_collide(self, direction, dt):
        if direction.length() == 0:
            return

        # Store original position
        original_x = self.rect.x
        original_y = self.rect.y

        # Calculate movement
        movement = direction * self.speed * dt

        # Try moving on X axis first
        self.rect.x += movement.x
        for sprite in self.obstacles:
            if self.rect.colliderect(sprite.rect):
                self.rect.x = original_x
                break

        # Then try moving on Y axis
        self.rect.y += movement.y
        for sprite in self.obstacles:
            if self.rect.colliderect(sprite.rect):
                self.rect.y = original_y
                break

        # Ensure we stay within map bounds
        if self.map_bounds:
            self.rect.clamp_ip(self.map_bounds)

    def animate(self, dt):
        frames = self.flipped_animations[self.status] if self.facing_left else self.animations[self.status]
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(frames):
            self.frame_index = 0
        self.image = frames[int(self.frame_index)]

    def update(self, dt):
        direction = self.handle_input()
        self.status = "walk" if direction.length() > 0 else "idle"
        self.move_and_collide(direction, dt)
        self.auto_attack()
        self.animate(dt)

    def auto_attack(self):
        # Determine the direction based on player's movement or last direction
        direction = self.handle_input()
        if direction.length() > 0:
            # Use the movement direction
            self.weapon.shoot(direction=(direction.x, direction.y))
        else:
            # Use the last movement direction
            self.weapon.shoot(direction=self.last_direction)