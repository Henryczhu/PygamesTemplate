import pygame
from map import Map
from towers import Tower, MagicTower
from utils import Calcs
from Functions import *
from money import CoinManager, CoinDisplay

pygame.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
FRAME_RATE = 100
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Game')
# ----------------------------------------
enemy_list = []
enemy_deleted = []

map1 = Map.Map()

tower_list = []
tower_list.append(Tower.Tower(650, 230))
tower_list.append(MagicTower.MagicTower(650, 450))

wave = 0
data = []

cm = CoinManager.CoinManager()
coinDisplay = CoinDisplay.CoinDisplay()
money = 0
# ----------------------------------------


run = True
while run:
    clock.tick(FRAME_RATE)
    screen.fill((150, 150, 150))

    # ----------------------------------------
    for tower in tower_list:
        tower.update(enemy_list)

    if len(data) == 0:
        wave += 1
        data = spawnWave(wave)
    else:
        if len(data) % 2 == 0:
            spawnEnemy(data[0], -25, 125, map1.path, enemy_list)
            del data[0]
        else:
            if data[0] > 0:
                data[0] -= 1
            else:
                del data[0]

    enemy_deleted = []
    for enemy in enemy_list:
        if enemy.update() == 'delete':
            enemy_list.remove(enemy)
        else:
            for tower in tower_list:
                hits = Calcs.checkCollision(enemy, tower.projs)
                if len(hits) > 0:
                    money += enemy.value
                    enemy_list.remove(enemy)
                    enemy_deleted.append(enemy)
                    tower.removeBullets(hits)
                    if len(enemy_list) == 0:
                        break

    for tower in tower_list:
        if tower.homing:
            tower.updateProjs(enemy_deleted, enemy_list)

    map1.render(screen)
    
    for tower in tower_list:
        tower.render(screen)

    for enemy in enemy_list:
        enemy.render(screen)

    cm.render(screen, money)
    coinDisplay.render(screen, len(str(money)))

    # ----------------------------------------

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
