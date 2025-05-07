import pygame

class CameraGroup(pygame.sprite.LayeredUpdates):
    def __init__(self, player):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.offset = pygame.math.Vector2(0, 0)

        # Optional: center offset for smooth scrolling
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2
    def draw(self):
        self.offset.x = self.player.rect.centerx - self.half_w
        self.offset.y = self.player.rect.centery - self.half_h

        # Draw all sprites, ordered by layer then Y-axis for depth
        for sprite in sorted(self.sprites(), key=lambda s: (self.get_layer_of_sprite(s), s.rect.centery)):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)
