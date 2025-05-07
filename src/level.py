import pygame
from map_layout import level_map
from settings import TILE_SIZE, SCREEN_HEIGHT, SCREEN_WIDTH
from player import Player


from settings import SCREEN_HEIGHT, SCREEN_WIDTH

class Level:
    def __init__(self, surface):
        self.display_surface = surface

        # Sprite groups
        self.tiles = pygame.sprite.Group()             # All terrain tiles (walls, floors, etc.)
        self.obstacle_sprites = pygame.sprite.Group()  # Collision obstacles
        self.visible_sprites = None                    # Camera group for rendering
        self.player_sprite = None
        
        # Tile graphics
        self.ground_tile = pygame.image.load("assets/tiles/floor_01.png").convert_alpha()
        self.wall_tile = pygame.image.load("assets/tiles/wall_01.png").convert_alpha()
        self.chest_tile = pygame.image.load("assets/tiles/chest_01.png").convert_alpha()

        self.build_level()

    def build_level(self):
        # Calculate map boundaries
        map_width = len(level_map[0]) * TILE_SIZE
        map_height = len(level_map) * TILE_SIZE

        for row_index, row in enumerate(level_map):
            for col_index, cell in enumerate(row):
                x = col_index * TILE_SIZE
                y = row_index * TILE_SIZE

                # Always place a floor tile first
                floor_tile = Tile((x, y), self.ground_tile)
                self.tiles.add(floor_tile)

                # Then add other tiles if needed
                if cell == "X":
                    wall_tile = Tile((x, y), self.wall_tile)
                    self.tiles.add(wall_tile)
                    self.obstacle_sprites.add(wall_tile)
                elif cell == "C":
                    chest_tile = Tile((x, y), self.chest_tile)
                    self.tiles.add(chest_tile)
                    self.obstacle_sprites.add(chest_tile)  # Make chests solid for now
                elif cell == "P":
                    self.player_sprite = Player((x + TILE_SIZE // 2, y + TILE_SIZE // 2), self.obstacle_sprites)
                    # Set map boundaries for player
                    self.player_sprite.map_bounds = pygame.Rect(0, 0, map_width, map_height)

        # Camera setup after player created
        self.visible_sprites = CameraGroup(self.player_sprite)
        self.visible_sprites.add(self.player_sprite)
        self.visible_sprites.add(self.tiles)  # Add all tiles to visible sprites

    def run(self, dt):
        self.visible_sprites.update(dt)
        self.visible_sprites.draw()



class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)


class CameraGroup(pygame.sprite.Group):
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

        # Draw all sprites except player
        for sprite in sorted(self.sprites(), key=lambda s: s.rect.centery):
            if sprite != self.player:  # Skip player for now
                offset_pos = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_pos)
        
        # Draw player last (on top)
        offset_pos = self.player.rect.topleft - self.offset
        self.display_surface.blit(self.player.image, offset_pos)
