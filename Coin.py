import math
import pygame


class Coin:
    def __init__(self, images, x, y):
        self.coins = images
        self.x = x
        self.y = y
        self.aniFrame = 0
        self.tick = 0

    def update(self):
        self.tick += 1
        if self.tick % 10 == 0:
            self.aniFrame += 1
            if self.aniFrame > 3:
                self.aniFrame = 0

    def render(self, screen):
        screen.blit(self.coins[self.aniFrame], (self.x - 8, self.y - 8))





