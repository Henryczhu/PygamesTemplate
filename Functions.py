from enemies import RedEnemy, BlueEnemy, GreenEnemy


def spawnRed(x, y, path, enemy_list):
    enemy_list.append(RedEnemy.RedEnemy(x, y, path))

def spawnBlue(x, y, path, enemy_list):
    enemy_list.append(BlueEnemy.BlueEnemy(x, y, path))

def spawnGreen(x, y, path, enemy_list):
    enemy_list.append(GreenEnemy.GreenEnemy(x, y, path))

def spawnWave(wave):
    file = open('../res/waves/' + str(1 + int(wave / 10)) + '.txt', 'r')
    encoded = file.readlines()[wave - 1]
    enemies = []
    count = []
    count.append(int(encoded[0: encoded.find('x')]))
    enemies.append(encoded[encoded.find('x') + 1: encoded.find('_')])
    time = int(encoded[encoded.find('_') + 1: len(encoded)])
    total_count = 0
    for num in count:
        total_count += num
    return count, enemies, time, total_count


