import math

from enemies import RedEnemy, BlueEnemy, GreenEnemy


def spawnEnemy(type, x, y, path, enemy_list):
    if type == 'red':
        spawnRed(x, y, path, enemy_list)
    if type == 'blue':
        spawnBlue(x, y, path, enemy_list)
    if type == 'green':
        spawnGreen(x, y, path, enemy_list)


def spawnRed(x, y, path, enemy_list):
    enemy_list.append(RedEnemy.RedEnemy(x, y, path))


def spawnBlue(x, y, path, enemy_list):
    enemy_list.append(BlueEnemy.BlueEnemy(x, y, path))


def spawnGreen(x, y, path, enemy_list):
    enemy_list.append(GreenEnemy.GreenEnemy(x, y, path))


def spawnWave(wave):
    file = open('../res/waves/' + str(1 + int(wave / 10)) + '.txt', 'r')
    file = file.readlines()
    data = []
    if len(file) >= wave:
        e = file[wave - 1]
        while True:
            if len(e) <= 1:
                break
            amt = int(e[0: e.index('x')])
            color = e[e.index('x') + 1: e.index('_')]
            time = int(e[e.index('_') + 1: e.index('+')])
            wait = math.ceil(time / amt * 100)
            e = e[e.index('+') + 1: len(e)]
            print(e)
            for i in range(amt):
                data.append(color)
                data.append(wait)
    return data
