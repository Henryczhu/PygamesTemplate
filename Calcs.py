import math


def findClosestEnemy(enemies, x, y):
    smallest = -1
    if len(enemies) == 0:
        return False
    for i in range(len(enemies)):
        distance = math.dist((enemies[i].x, enemies[i].y), (x, y))
        if distance < smallest or smallest == -1:
            smallest = distance
            sI = i
    return enemies[sI]


def checkCollision(enemy, projs):
    hits = []
    for proj in projs:
        dist = math.dist((enemy.x, enemy.y), (proj.x, proj.y))
        if dist < 20:
            hits.append(proj)
    return hits

