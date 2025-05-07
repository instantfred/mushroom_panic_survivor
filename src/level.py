import pygame

from settings import SCREEN_HEIGHT, SCREEN_WIDTH

TILE_SIZE = 48


class Level:
    def __init__(self, surface):
        self.display_surface = surface
        self.floor_tile = pygame.image.load("assets/tiles/floor_01.png").convert_alpha()
        self.floor_tile = pygame.transform.scale(
            self.floor_tile, (TILE_SIZE, TILE_SIZE)
        )

    def draw_floor(self):
        tiles_x = SCREEN_WIDTH // TILE_SIZE + 1
        tiles_y = SCREEN_HEIGHT // TILE_SIZE + 1

        for row in range(tiles_y):
            for col in range(tiles_x):
                x = col * TILE_SIZE
                y = row * TILE_SIZE
                self.display_surface.blit(self.floor_tile, (x, y))
