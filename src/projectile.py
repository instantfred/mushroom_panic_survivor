import pygame
from settings import TILE_SIZE

class Projectile(pygame.sprite.Sprite):
    def __init__(self, pos, direction, speed, lifespan, image, damage=10, weapon_type="basic"):
        super().__init__()
        self.original_image = image
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2(direction).normalize()
        self.speed = speed
        self.spawn_time = pygame.time.get_ticks()
        self.lifespan = lifespan
        self.damage = damage
        self.weapon_type = weapon_type
        
        # Trail effect
        self.trail_positions = []
        self.max_trail_length = 5
        
        # Rotate image to match direction
        angle = pygame.math.Vector2(1, 0).angle_to(self.direction)
        self.image = pygame.transform.rotate(self.original_image, -angle)
        self.rect = self.image.get_rect(center=pos)

    def update(self, dt):
        # Store current position for trail
        self.trail_positions.append(self.rect.center)
        if len(self.trail_positions) > self.max_trail_length:
            self.trail_positions.pop(0)
            
        # Move projectile
        self.rect.x += self.direction.x * self.speed * dt
        self.rect.y += self.direction.y * self.speed * dt

        # Check lifespan
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifespan:
            self.kill()

    def draw(self, surface):
        # Draw trail
        if len(self.trail_positions) > 1:
            pygame.draw.lines(surface, (255, 255, 0), False, self.trail_positions, 2)
        
        # Draw projectile
        surface.blit(self.image, self.rect)

    def handle_collision(self, sprite):
        # Handle collision with different types of sprites
        if hasattr(sprite, 'take_damage'):
            sprite.take_damage(self.damage)
        self.kill()
