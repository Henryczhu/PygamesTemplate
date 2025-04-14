import pygame
import math


class MagicBullet:
    def __init__(self, x, y, target):
        self.sheet = pygame.image.load('../res/Magic_Bullet_03.png')
        self.sheet = pygame.transform.scale_by(self.sheet, 3)
        self.frames = []
        self.getFrames()
        self.x = x
        self.y = y
        self.target = target
        self.speed = 7
        self.range = 1500
        self.dir = self.getDir(self.target.x, self.target.y)
        self.tick = 0

    def getFrames(self):
        for col in range(31):
            rect = pygame.Rect(96 * col, 0, 96, 96)
            self.frames.append(self.sheet.subsurface(rect))

    def getDir(self, targetX, targetY):
        return math.atan2((targetY - self.y), (targetX - self.x))

    def update(self):
        self.tick += 0.1
        self.dir = self.getDir(self.target.x, self.target.y)
        self.x += math.cos(self.dir) * self.speed
        self.y += math.sin(self.dir) * self.speed
        self.range -= self.speed
        if self.range <= 0:
            return 'delete'

    def render(self, screen):
        rotated = pygame.transform.rotate(self.frames[int(self.tick % 31)], -math.degrees(self.dir))
        screen.blit(rotated, (self.x - 48, self.y - 48))
