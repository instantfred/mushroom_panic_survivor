import pygame
import random

class DisintegrationEffect(pygame.sprite.Sprite):
    def __init__(self, sprite, duration=1.0):
        super().__init__()
        self.original_image = sprite.image.copy()
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=sprite.rect.center)
        self.duration = duration
        self.elapsed_time = 0
        self.particles = []
        self.create_particles()
        
    def create_particles(self):
        # Create particles for disintegration effect
        width = self.original_image.get_width()
        height = self.original_image.get_height()
        
        # Create particles in a grid pattern
        particle_size = 4  # Size of each particle
        for y in range(0, height, particle_size):
            for x in range(0, width, particle_size):
                # Get the color of the pixel at this position
                color = self.original_image.get_at((x, y))
                if color[3] > 0:  # Only create particles for non-transparent pixels
                    self.particles.append({
                        'pos': pygame.Vector2(x, y),
                        'color': color,
                        'velocity': pygame.Vector2(
                            random.uniform(-50, 50),  # Random horizontal velocity
                            random.uniform(50, 150)   # Upward velocity
                        ),
                        'size': random.uniform(2, 4),
                        'alpha': 255
                    })
    
    def update(self, dt):
        self.elapsed_time += dt
        progress = self.elapsed_time / self.duration
        
        # Create a new surface for the effect
        self.image = pygame.Surface(self.original_image.get_size(), pygame.SRCALPHA)
        
        # Update and draw particles
        for particle in self.particles:
            # Update position
            particle['pos'] += particle['velocity'] * dt
            
            # Update alpha (fade out)
            particle['alpha'] = int(255 * (1 - progress))
            
            # Draw particle
            if particle['alpha'] > 0:
                color = (*particle['color'][:3], particle['alpha'])
                pygame.draw.circle(
                    self.image,
                    color,
                    particle['pos'],
                    particle['size']
                )
        
        # Kill the effect when it's done
        if progress >= 1.0:
            self.kill() 