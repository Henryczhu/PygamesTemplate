import pygame
from pygame.locals import *
from player import Swordsman
from tiles import TileManager
from enemies import Enemy
import math


def creativeMovement():
    if keyDown.get('w'):
        player.y += 25
    if keyDown.get('a'):
        player.x -= 25
    if keyDown.get('s'):
        player.y -= 25
    if keyDown.get('d'):
        player.x += 25


def getTileIndex(x, y):
    row = int((482 - y + camY) / 64)
    col = int((x + camX - 768) / 64)
    index = row * 200 + col
    return index


def movement():
    global xVel
    global yVel
    global falling
    # x part:
    if keyDown.get('a'):
        xVel -= 2
    if keyDown.get('d'):
        xVel += 2
    xVel *= 0.85
    if abs(xVel) < 0.5:
        xVel = 0
    player.xVel = xVel
    # y part:
    if keyDown.get('space') and not player.falling:
        yVel = 30
        player.falling = True
    yVel += -1.2
    yVel *= 0.96
    if abs(yVel) < 0.5:
        yVel = 0
    player.yVel = yVel

pygame.init()

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 900
FRAME_RATE = 100
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Game')
# ----------------------------------------
gamemode = 0
tile = 0
cooldown = 0
mapTileWidth = 200
mapTileHeight = 100
tm = TileManager.TileManager()
player = Swordsman.Swordsman(tm.tileGrid)
camX = 800
camY = 450
keyDown = {'w': False, 'a': False, 's': False, 'd': False}
mouseDown = False
xVel = 0
yVel = 0
falling = False

enemies = []
enemies.append(Enemy.Enemy(tm.tileGrid, 1600, 450))
enemies.append(Enemy.Enemy(tm.tileGrid, 1200, 450))
# ----------------------------------------


run = True
while run:
    clock.tick(FRAME_RATE)
    screen.fill((0, 0, 0))

    # ----------------------------------------
    if gamemode == 0:
        movement()
    if gamemode == 1:
        creativeMovement()
        if cooldown == 0:
            if keyDown.get('right'):
                tile += 1
                cooldown = 10
            if keyDown.get('left'):
                tile -= 1
                cooldown = 10
            if tile < 0:
                tile = 22
            if tile > 22:
                tile = 0
        else:
            cooldown -= 1

    camX = player.x
    camY = player.y

    if camX < 800:
        camX = 800
    if camY < 450:
        camY = 450
    if camX > mapTileWidth * 64 - 800 - 64:
        camX = mapTileWidth * 64 - 800 - 64
    if camY > mapTileHeight * 64 - 450 - 64:
        camY = mapTileHeight * 64 - 450 - 64

    tm.update(camX, camY, gamemode)
    tm.render(screen, gamemode, tile)

    player.update(camX, camY)
    player.render(screen)

    for enemy in enemies:
        enemy.update(camX, camY, player.x, player.y)
        enemy.render(screen, camX, camY)

    for enemy in enemies:
        dist = math.dist((enemy.x, enemy.y), (player.x, player.y))
        if dist < 30 and enemy.cooldown == 0:
            if player.attacking and player.x < enemy.x and player.dir == 0:
                enemy.xVel = 30
                enemy.yVel = 5
            elif player.attacking and player.x > enemy.x and player.dir == 1:
                enemy.xVel = -30
                enemy.yVel = 5
            else:
                player.health -= enemy.damage
                enemy.cooldown = 30
                if enemy.x < player.x:
                    xVel = 30
                    yVel = 5
                else:
                    xVel = -30
                    yVel = 5

    if mouseDown:
        if gamemode == 1:
            mx, my = pygame.mouse.get_pos()
            tm.placeTile(getTileIndex(mx, my), tile)
        else:
            player.attack()
            xVel = 0

    # ----------------------------------------

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseDown = True
        if event.type == pygame.MOUSEBUTTONUP:
            mouseDown = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if gamemode == 1:
                    tm.save()
            if event.key == pygame.K_w:
                keyDown.update({'w': True})
            if event.key == pygame.K_a:
                player.dir = 1
                keyDown.update({'a': True})
            if event.key == pygame.K_s:
                keyDown.update({'s': True})
            if event.key == pygame.K_d:
                player.dir = 0
                keyDown.update({'d': True})
            if event.key == pygame.K_SPACE:
                keyDown.update({'space': True})
            if event.key == pygame.K_RIGHT:
                keyDown.update({'right': True})
            if event.key == pygame.K_LEFT:
                keyDown.update({'left': True})
            if event.key == pygame.K_c:
                if gamemode == 0:
                    gamemode = 1
                else:
                    gamemode = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                keyDown.update({'w': False})
            if event.key == pygame.K_a:
                keyDown.update({'a': False})
            if event.key == pygame.K_s:
                keyDown.update({'s': False})
            if event.key == pygame.K_d:
                keyDown.update({'d': False})
            if event.key == pygame.K_SPACE:
                keyDown.update({'space': False})
            if event.key == pygame.K_RIGHT:
                keyDown.update({'right': False})
            if event.key == pygame.K_LEFT:
                keyDown.update({'left': False})
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
