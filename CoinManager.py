import random
import pygame
from money import Coin


class CoinManager:
    def __init__(self):
        img = pygame.image.load('../res/coin.png').convert_alpha()
        self.image = img
        self.images = []
        self.coins = []
        self.loadRects()
        self.font = pygame.font.SysFont("Comic Sans MS", 40)

    def loadRects(self):
        for col in range(5):
            rect = pygame.Rect(col * 16, 0, 16, 16)
            img = self.image.subsurface(rect)
            self.images.append(img)

    def render(self, screen, money):
        for coin in self.coins:
            coin.render(screen)
        money_text = self.font.render(str(money), 1, (0, 0, 0))
        screen.blit(money_text, (1212 * (0.97 - (0.0185 * len(str(money)))), 2))

    def createCoin(self, x, y):
        self.coins.append(Coin.Coin(self.images, x, y))
