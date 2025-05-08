import pygame
from projectile import Projectile

class Weapon:
    def __init__(self, owner, projectile_group, image, cooldown=500, speed=300, lifespan=2000):
        self.owner = owner  # the player or enemy using the weapon
        self.projectile_group = projectile_group
        self.image = image
        self.cooldown = cooldown
        self.speed = speed
        self.lifespan = lifespan
        self.last_shot = 0

    def shoot(self, direction=(1, 0)):
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.cooldown:
            self.last_shot = now
            projectile = Projectile(
                pos=self.owner.rect.center,
                direction=direction,
                speed=self.speed,
                lifespan=self.lifespan,
                image=self.image
            )
            self.projectile_group.add(projectile)
