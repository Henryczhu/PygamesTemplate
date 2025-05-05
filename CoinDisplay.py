import math
import pygame


class CoinDisplay:
    def __init__(self):
        img = pygame.image.load('../res/coin.png').convert_alpha()
        self.image = img.subsurface(0, 0, 16, 16)
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.x = 0
        self.y = 32

    def render(self, screen, len_money):
        self.x = 1178 * (0.97 - (0.0185 * len_money))
        screen.blit(self.image, (self.x - 24, self.y - 24))

