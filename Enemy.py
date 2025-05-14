import math
import pygame
import random


class Enemy(pygame.sprite.Sprite):
    def __init__(self, tileGrid, x, y):  # constructor
        pygame.sprite.Sprite.__init__(self)
        self.sheet = pygame.image.load('../res/Enemy.png')
        self.x = x
        self.y = y
        self.xVel = 0
        self.yVel = 0
        self.falling = False
        self.width = 90
        self.height = 65
        self.images = {}
        self.getSubimages()
        self.ani_length = {'run': 3}
        self.ani_frame = 0
        self.ani_speed = 0.05
        self.ani = 'run'
        self.rect = pygame.transform.scale(self.images[self.ani][0], (120, 160)).get_rect()
        self.dir = 0
        self.tileGrid = tileGrid
        self.circles = []
        self.damage = 10
        self.cooldown = 0

    def getSubimages(self):
        frames = []
        frames.append(self.sheet.subsurface(41, 0, 34, 48))
        frames.append(self.sheet.subsurface(193, 0, 34, 48))
        frames.append(self.sheet.subsurface(347, 0, 34, 48))
        self.images.update({ 'run': frames })

    def getTileAt(self, x, y):
        row = int((900 - y + 32) / 64)
        col = int((x + 32) / 64)
        index = row * 200 + col
        return self.tileGrid[index]

    def checkCollision(self, xVel, yVel):
        for row in range(3):
            for col in range(3):
                if row == 1 and col == 1:
                    continue
                cx = int(self.x) + (row - 1) * 32 - 75
                cy = int(900 - self.y) + (col - 1) * 24 - 32

                if self.getTileAt(cx, cy) != 0:
                    tile_col = int((cx + 32) / 64)
                    tile_row = int((900 - cy + 32) / 64)

                    if xVel > 0:
                        self.x = tile_col * 64 + 10
                        self.xVel = 0
                    if xVel < 0:
                        self.x = tile_col * 64 + 140
                        self.xVel = 0

                    if yVel > 0:
                        self.y = tile_row * 64 - 32
                        self.yVel = 0
                    if yVel < 0:
                        self.y = tile_row * 64 + 24
                        self.yVel = 0
                        self.falling = False

    def animation(self):
        self.ani_frame += self.ani_speed
        # if self.xVel == 0:
        #     self.ani = 'idle'
        #     self.ani_speed = 0.05
        # else:
        #     self.ani = 'run'
        #     self.ani_speed = 0.1
        #     if self.xVel < 0:
        #         self.dir = 1
        #     if self.xVel > 0:
        #         self.dir = 0

    def movement(self, dist):
        if self.dir == 0:
            self.xVel += 0.5
        if self.dir == 1:
            self.xVel -= 0.5
        self.xVel *= 0.85
        if abs(self.xVel) < 0.2:
            self.xVel = 0
        if dist < 10:
            self.xVel = 0

        self.yVel += -1.2
        self.yVel *= 0.96
        if abs(self.yVel) < 0.5:
            self.yVel = 0

    def lineOfSight(self, px, py):
        self.circles = []
        dist = int(math.dist((self.x, self.y), (px, py)))
        dir = math.atan2((py - self.y), (px - self.x))
        x = self.x
        y = self.y
        x += math.cos(dir) * 10
        y += math.sin(dir) * 10
        for i in range(10, dist):
            x += math.cos(dir)
            y += math.sin(dir)
            if self.getTileAt(x, 890 - y) != 0:
                return False
            self.circles.append((x, y))
        return True

    def update(self, camX, camY, px, py):
        if self.cooldown > 0:
            self.cooldown -= 1
        if self.lineOfSight(px, py):
            if px > self.x:
                self.dir = 0
            if px < self.x:
                self.dir = 1
        else:
            if random.randint(1, 50) == 1:
                if self.dir == 1:
                    self.dir = 0
                else:
                    self.dir = 1
        self.movement(abs(px - self.x))
        self.animation()
        self.x += self.xVel
        self.checkCollision(self.xVel, 0)
        self.y += self.yVel
        self.checkCollision(0, self.yVel)
        self.rect.center = (800 + (self.x - camX) - 80, 450 - (self.y - camY) - 80)

    def render(self, screen, camX, camY):
        img = pygame.transform.scale(
            self.images[self.ani][int(self.ani_frame) % self.ani_length[self.ani]], (120, 160))
        img = pygame.transform.flip(img, self.dir, 0)
        screen.blit(img, self.rect)
        for circle in self.circles:
            pygame.draw.circle(screen, (255, 255, 255), (800 + (circle[0] - camX) - 80, 450 - (circle[1] - camY) - 80), 2)

