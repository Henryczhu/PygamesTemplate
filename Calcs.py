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
