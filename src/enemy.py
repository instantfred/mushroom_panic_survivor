import pygame
from settings import TILE_SIZE
import os

SPRITE_SIZE = 32  # Match actual frame size

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, player, enemy_type='blob'):
        super().__init__()
        self.player = player
        self.enemy_type = enemy_type
        
        # Load enemy stats based on type
        self.stats = self.get_enemy_stats()
        
        # Animation setup
        self.frame_index = 0
        self.animation_speed = self.stats['animation_speed']
        self.facing_left = False
        
        # Load animations
        self.animations = {
            'idle': self.load_animation('blob_spritesheet.png', 0, 2),
            'walk': self.load_animation('blob_spritesheet.png', 1, 4),
            'hurt': self.load_animation('blob_spritesheet.png', 2, 1),
            'attack': self.load_animation('blob_spritesheet.png', 3, 3)
        }
        
        # Set initial state
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        
        # Movement
        self.speed = self.stats['speed']
        self.attack_range = self.stats['attack_range']
        self.attack_cooldown = 0
        self.health = self.stats['health']
        self.is_hurt = False
        self.hurt_timer = 0

    def get_enemy_stats(self):
        # Define stats for different enemy types
        stats = {
            'blob': {
                'health': 20,
                'speed': 80,
                'damage': 10,
                'attack_range': 50,
                'attack_cooldown': 1.0,
                'animation_speed': 8,
                'idle_frames': 2,
                'walk_frames': 4,
                'hurt_frames': 1,
                'attack_frames': 3
            }
            # Add more enemy types here as needed
        }
        return stats.get(self.enemy_type, stats['blob'])  # Default to blob if type not found

    def load_animation(self, filename, row, num_frames):
        path = os.path.join('assets', 'sprites', filename)
        sprite_sheet = pygame.image.load(path).convert_alpha()
        frames = []
        for i in range(num_frames):
            x = i * SPRITE_SIZE
            y = row * SPRITE_SIZE
            rect = pygame.Rect(x, y, SPRITE_SIZE, SPRITE_SIZE)

            # Sanity check: avoid subsurface if rect is invalid
            # print(f"Loading {filename}: size = {sprite_sheet.get_width()}x{sprite_sheet.get_height()}")
            if x + SPRITE_SIZE > sprite_sheet.get_width() or y + SPRITE_SIZE > sprite_sheet.get_height():
                print(f"[ERROR] Tried to extract frame at ({x}, {y}) — outside sprite sheet!")
                continue

            frame = sprite_sheet.subsurface(rect)
            frame = pygame.transform.scale(frame, (TILE_SIZE, TILE_SIZE))  # Optional scaling
            frames.append(frame)

        return frames

    def get_direction_to_player(self):
        # Calculate direction vector to player
        direction = pygame.Vector2(
            self.player.rect.centerx - self.rect.centerx,
            self.player.rect.centery - self.rect.centery
        )
        
        # Normalize the direction vector
        if direction.length() > 0:
            direction = direction.normalize()
            
        return direction

    def move_towards_player(self, dt):
        if self.is_hurt:
            return

        direction = self.get_direction_to_player()
        
        # Update facing direction
        self.facing_left = direction.x < 0
        
        # Move towards player
        self.rect.x += direction.x * self.speed * dt
        self.rect.y += direction.y * self.speed * dt

    def animate(self, dt):
        # Handle hurt animation
        if self.is_hurt:
            self.hurt_timer -= dt
            if self.hurt_timer <= 0:
                self.is_hurt = False
                self.status = 'idle'
        
        # Update animation frame
        frames = self.animations[self.status]
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(frames):
            self.frame_index = 0
            if self.status == 'hurt':
                self.is_hurt = False
                self.status = 'idle'
            elif self.status == 'attack':
                self.status = 'idle'
        
        # Get current frame and flip if needed
        frame = frames[int(self.frame_index)]
        if self.facing_left:
            frame = pygame.transform.flip(frame, True, False)
        self.image = frame

    def take_damage(self, amount):
        self.health -= amount
        self.is_hurt = True
        self.hurt_timer = 0.5  # Hurt animation duration
        self.status = 'hurt'
        if self.health <= 0:
            self.kill()

    def update(self, dt):
        # Update attack cooldown
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

        # Check distance to player
        distance_to_player = pygame.Vector2(
            self.player.rect.centerx - self.rect.centerx,
            self.player.rect.centery - self.rect.centery
        ).length()

        # Update status based on distance to player
        if distance_to_player <= self.attack_range and self.attack_cooldown <= 0:
            self.status = 'attack'
            self.attack_cooldown = self.stats['attack_cooldown']
        elif not self.is_hurt:
            self.status = 'walk' if distance_to_player > self.attack_range else 'idle'

        # Move and animate
        self.move_towards_player(dt)
        self.animate(dt) 