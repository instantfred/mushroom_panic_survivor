import sys

import pygame

from level import Level
from player import Player
from settings import FPS, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, BG_COLOR


def main():
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # Level and Player setup
    level = Level(screen)
    player = Player(pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    player_group = pygame.sprite.GroupSingle(player)

    # Main game loop
    running = True
    while running:
        dt = clock.tick(FPS) / 1000  # Delta time in seconds

        # 1. Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 2. Draw everything
        screen.fill(BG_COLOR)
        level.run(dt)
        pygame.display.flip()

    # Clean up
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
