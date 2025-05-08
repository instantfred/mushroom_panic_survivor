import pygame
from projectile import Projectile

class Weapon:
    def __init__(self, owner, projectile_group, image, cooldown=500, speed=300, lifespan=2000, damage=10, weapon_type="basic"):
        self.owner = owner  # the player or enemy using the weapon
        self.projectile_group = projectile_group
        self.image = image
        self.cooldown = cooldown
        self.speed = speed
        self.lifespan = lifespan
        self.damage = damage
        self.weapon_type = weapon_type
        self.last_shot = 0
        
        # Cooldown visualization
        self.cooldown_surface = pygame.Surface((20, 4))
        self.cooldown_surface.fill((50, 50, 50))
        self.cooldown_rect = self.cooldown_surface.get_rect()
        
        # Sound effects
        self.shoot_sound = None  # Will be loaded if sound file exists
        try:
            self.shoot_sound = pygame.mixer.Sound("assets/sounds/shoot.wav")
        except:
            print("No shoot sound found")

    def shoot(self, direction=(1, 0)):
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.cooldown:
            self.last_shot = now
            
            # Create projectile with weapon properties
            projectile = Projectile(
                pos=self.owner.rect.center,
                direction=direction,
                speed=self.speed,
                lifespan=self.lifespan,
                image=self.image,
                damage=self.damage,
                weapon_type=self.weapon_type
            )
            self.projectile_group.add(projectile)
            
            # Play sound if available
            if self.shoot_sound:
                self.shoot_sound.play()

    def draw_cooldown(self, surface, pos):
        # Draw cooldown bar
        current_time = pygame.time.get_ticks()
        cooldown_progress = min(1.0, (current_time - self.last_shot) / self.cooldown)
        
        # Create progress bar
        progress_width = int(self.cooldown_rect.width * cooldown_progress)
        progress_surface = pygame.Surface((progress_width, self.cooldown_rect.height))
        progress_surface.fill((0, 255, 0) if cooldown_progress == 1.0 else (255, 0, 0))
        
        # Draw both surfaces
        surface.blit(self.cooldown_surface, pos)
        surface.blit(progress_surface, pos)
