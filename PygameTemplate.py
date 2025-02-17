import pygame
from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 100
SCREEN_HEIGHT = 100
FRAME_RATE = 10
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Game')
# ----------------------------------------


# ----------------------------------------


run = True
while run:
    clock.tick(FRAME_RATE)
    screen.fill((0, 0, 0))

    # ----------------------------------------


    # ----------------------------------------


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
