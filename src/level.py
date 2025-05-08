import pygame
from map_layout import level_map
from settings import TILE_SIZE
from player import Player
from enemy import Enemy
from camera import CameraGroup


class Level:
    def __init__(self, surface):
        self.display_surface = surface

        # Sprite groups
        self.tiles = pygame.sprite.Group()             # All terrain tiles (walls, floors, etc.)
        self.obstacle_sprites = pygame.sprite.Group()  # Collision obstacles
        self.visible_sprites = None                    # Camera group for rendering
        self.player_sprite = None
        self.enemy_sprites = pygame.sprite.Group()     # Enemy sprites
        self.projectiles = pygame.sprite.Group()       # Player projectiles
        
        # Tile graphics
        self.ground_tile = pygame.image.load("assets/tiles/floor_01.png").convert_alpha()
        self.wall_tile = pygame.image.load("assets/tiles/wall_01.png").convert_alpha()
        self.chest_tile = pygame.image.load("assets/tiles/chest_01.png").convert_alpha()

        # Enemy spawning
        self.spawn_timer = 0
        self.spawn_cooldown = 3.0  # Spawn an enemy every 3 seconds
        self.enemy_spawn_points = []  # Will store valid spawn positions

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
                    self.player_sprite = Player((x + TILE_SIZE // 2, y + TILE_SIZE // 2), self.obstacle_sprites, self.projectiles)
                    # Set map boundaries for player
                    self.player_sprite.map_bounds = pygame.Rect(0, 0, map_width, map_height)
                elif cell == "E":
                    # Store enemy spawn points
                    self.enemy_spawn_points.append((x + TILE_SIZE // 2, y + TILE_SIZE // 2))

        # Camera setup after player created
        self.visible_sprites = CameraGroup(self.player_sprite)
        # Add tiles to layer 0
        for tile in self.tiles:
            self.visible_sprites.add(tile, layer=0)

        # Add player and enemies to layer 2
        self.visible_sprites.add(self.player_sprite, layer=2)
        for enemy in self.enemy_sprites:
            self.visible_sprites.add(enemy, layer=2)

        # Add projectiles to layer 3
        for projectile in self.projectiles:
            self.visible_sprites.add(projectile, layer=3)    

    def spawn_enemy(self):
        if not self.enemy_spawn_points:
            return

        # Choose a random spawn point
        import random
        spawn_pos = random.choice(self.enemy_spawn_points)
        
        # Create new enemy
        enemy = Enemy(spawn_pos, self.player_sprite)
        self.enemy_sprites.add(enemy)
        self.visible_sprites.add(enemy, layer=2)

    def run(self, dt):
        # Update spawn timer
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_cooldown:
            self.spawn_enemy()
            self.spawn_timer = 0

        # Ensure all projectiles are in the visible_sprites group
        for projectile in self.projectiles:
            if projectile not in self.visible_sprites:
                self.visible_sprites.add(projectile, layer=3)
            
            # Check for collisions with enemies
            for enemy in self.enemy_sprites:
                if projectile.rect.colliderect(enemy.rect):
                    projectile.handle_collision(enemy)

        # Update and draw all sprites
        self.visible_sprites.update(dt)
        self.visible_sprites.draw()

        # Draw weapon cooldown
        if self.player_sprite:
            # Calculate center position for cooldown bar
            cooldown_pos = (self.player_sprite.rect.centerx - self.visible_sprites.offset.x - self.player_sprite.weapon.cooldown_rect.width // 2, 
                          self.player_sprite.rect.y - self.visible_sprites.offset.y - 10)
            self.player_sprite.weapon.draw_cooldown(self.display_surface, cooldown_pos)



class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, image):
        super().__init__()
        self.image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect(topleft=pos)

