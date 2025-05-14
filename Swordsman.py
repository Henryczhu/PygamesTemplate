import pygame
import random


class Swordsman(pygame.sprite.Sprite):

    def __init__(self, tileGrid):
        pygame.sprite.Sprite.__init__(self)
        self.sheet = pygame.image.load('../res/MiniSwordMan.png')
        self.x = 800
        self.y = 450
        self.xVel = 0
        self.yVel = 0
        self.falling = False
        self.width = 160
        self.height = 160
        self.images = {}
        self.getSubimages()
        self.ani_length = {'idle': 4, 'run': 6, 'fall': 3, 'attack': 6, 'hit': 3, 'die': 4}
        self.ani_frame = 0
        self.ani_speed = 0.05
        self.ani = 'idle'
        self.rect = pygame.transform.scale(self.images[self.ani][0], (160, 160)).get_rect()
        self.dir = 0
        self.tileGrid = tileGrid
        self.circles = []
        self.sleep = 0
        self.total_health = 100
        self.health = self.total_health
        self.attacking = False

    def getSubimages(self):
        ani_names = ['idle', 'run', 'fall', 'attack', 'hit', 'die']
        for row in range(6):
            rowImages = []
            for col in range(6):
                rect = pygame.Rect(32 * col, 32 * row, 32, 32)
                rowImages.append(self.sheet.subsurface(rect))
            self.images.update({ani_names[row] : rowImages})

    def getTileAt(self, x, y):
        row = int((900 - y + 32) / 64)
        col = int((x + 32) / 64)
        index = row * 200 + col
        return self.tileGrid[index]

    def checkCollision(self, xVel, yVel):
        self.circles = []
        for row in range(3):
            for col in range(3):
                if row == 1 and col == 1:
                    continue
                cx = int(self.x) + (row - 1) * 32 - 75
                cy = int(900 - self.y) + (col - 1) * 24 - 32
                self.circles.append([cx, cy])

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
                        self.y = tile_row * 64 - 92
                        self.yVel = 0
                    if yVel < 0:
                        self.y = tile_row * 64 + 24
                        self.yVel = 0
                        self.falling = False


    def attack(self):
        self.attacking = True
        self.ani = 'attack'
        self.ani_frame = 0
        self.ani_speed = 0.1
        self.sleep = 50


    def update(self, camX, camY):
        self.animation()
        self.x += self.xVel
        self.checkCollision(self.xVel, 0)
        self.y += self.yVel
        self.checkCollision(0, self.yVel)
        self.rect.center = (800 + (self.x - camX) - 80, 450 - (self.y - camY) - 80)

    def animation(self):
        self.ani_frame += self.ani_speed
        if self.sleep > 0:
            self.sleep -= 1
            return
        self.attacking = False
        if self.xVel == 0:
            self.ani = 'idle'
            self.ani_speed = 0.05
        else:
            self.ani = 'run'
            self.ani_speed = 0.1

    def gotHit(self, damage, enemy_x):
        self.health -= damage
        if enemy_x < self.x:
            self.xVel = 50
            self.yVel = 5
        else:
            self.xVel = -50
            self.yVel = 5

    def drawHealthBar(self, screen):
        pygame.draw.rect(screen, (25, 38, 27), (20, 20, 300, 30))
        pygame.draw.rect(screen, (41, 255, 82), (20, 20, int(300 * (self.health / self.total_health)), 30))

    def render(self, screen):
        img = pygame.transform.scale(
            self.images[self.ani][int(self.ani_frame) % self.ani_length[self.ani]], (160, 160))
        img = pygame.transform.flip(img, self.dir, 0)
        screen.blit(img, self.rect)
        self.drawHealthBar(screen)
