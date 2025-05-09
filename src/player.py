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

        # Health and damage attributes
        self.max_health = 100
        self.health = self.max_health
        self.is_hurt = False
        self.hurt_timer = 0
        self.invincibility_duration = 0.3  # seconds of invincibility after taking damage
        self.flash_timer = 0
        self.flash_duration = 0.2  # Duration of the flash effect
        self.is_flashing = False

        # Health bar attributes
        self.health_bar_width = 50
        self.health_bar_height = 5
        self.health_bar_rect = pygame.Rect(0, 0, self.health_bar_width, self.health_bar_height)

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
        self.weapon = Weapon(
            owner=self,
            projectile_group=projectile_group,
            effect_type="blue_orb",
            cooldown=2000,  # 2 seconds between shots
            speed=250,
            lifespan=2000, # 2 seconds lifespan
            damage=10,
            weapon_type="effect"
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
        # Update flash timer
        if self.is_flashing:
            self.flash_timer -= dt
            if self.flash_timer <= 0:
                self.is_flashing = False

        frames = self.flipped_animations[self.status] if self.facing_left else self.animations[self.status]
        self.frame_index += self.animation_speed * dt
        if self.frame_index >= len(frames):
            self.frame_index = 0
        self.image = frames[int(self.frame_index)]

        # Apply flash effect if active
        if self.is_flashing:
            # Create a copy of the current frame
            flash_image = self.image.copy()
            # Create a white surface with the same size
            flash_surface = pygame.Surface(flash_image.get_size(), pygame.SRCALPHA)
            flash_surface.fill((255, 0, 0, 128))  # Red with 50% opacity
            # Blend the red surface with the original image
            flash_image.blit(flash_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            # Apply the flash effect
            self.image = flash_image

    def take_damage(self, amount):
        if not self.is_hurt:  # Only take damage if not in invincibility period
            self.health -= amount
            self.is_hurt = True
            self.hurt_timer = self.invincibility_duration
            self.is_flashing = True
            self.flash_timer = self.flash_duration
            # Ensure health doesn't go below 0
            self.health = max(0, self.health)
            if self.health <= 0:
                self.die()

    def die(self):
        # Handle player death
        print("Player died!")

    def update(self, dt):
        # Update hurt timer
        if self.is_hurt:
            self.hurt_timer -= dt
            if self.hurt_timer <= 0:
                self.is_hurt = False

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

    def draw_health_bar(self, surface, offset):
        # Calculate health bar position (centered below player)
        if self.is_flashing:
            pulse_scale = 1 + 0.2 * (self.flash_timer / self.flash_duration)
            health_bar_pos = (
                self.rect.centerx - offset.x - (self.health_bar_width * pulse_scale) // 2,
                self.rect.bottom - offset.y + 3
            )
        else:
            health_bar_pos = (
                self.rect.centerx - offset.x - self.health_bar_width // 2,
                self.rect.bottom - offset.y + 3  # pixels below the player
            )
        
        # Draw background (gray)
        pygame.draw.rect(surface, (100, 100, 100), 
                        (*health_bar_pos, self.health_bar_width, self.health_bar_height))
        
        # Calculate current health width
        current_health_width = int((self.health / self.max_health) * self.health_bar_width)
        
        # Draw health (red)
        if current_health_width > 0:
            pygame.draw.rect(surface, (255, 0, 0),
                           (*health_bar_pos, current_health_width, self.health_bar_height))