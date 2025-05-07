import sys

import pygame

from settings import BG_COLOR, FPS, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE


def main():
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    # Main game loop
    running = True
    while running:
        # 1. Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # 2. Update game state
        # (We'll add player, enemies, etc. later)

        # 3. Draw everything
        screen.fill(BG_COLOR)
        pygame.display.flip()  # Refresh the screen

        # 4. Control frame rate
        clock.tick(FPS)

    # Clean up
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
