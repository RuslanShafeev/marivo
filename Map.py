from Tile import *
from Player import Player
from Goomba import Goomba
from Tube import Tube
from Camera import Camera

world = 'normal'

WIDTH = 212
HEIGHT = 14

bricks = {
    5: [80, 81, 82, 83, 84, 85, 86, 87, 91, 92, 93, 121, 122, 123, 128, 131],
    9: [21, 23, 25, 77, 79, 100, 118, 129, 130, 168, 169, 171]
}
quests = {
    5: [23, 94, 109, 129, 130],
    8: [64],
    9: [17, 22, 24, 78, 94, 101, 106, 109, 112, 170]
}
tubes = {
    12: [(28, 2), (38, 3), (46, 4), (57, 4), (163, 2), (179, 2)]
}

# TODO: добавь текстуру для блоков, которые в конце карты находятся в виде ступенек
stones = {
    5: [188, 189],
    6: [187, 188, 189],
    7: [186, 187, 188, 189],
    8: [185, 186, 187, 188, 189],
    9: [137, 140, 151, 152, 155] +
       [184, 185, 186, 187, 188, 189],
    10: [136, 137, 140, 141, 150, 151, 152, 155, 156] +
        [183, 184, 185, 186, 187, 188, 189],
    11: [135, 136, 137, 140, 141, 142, 149, 150, 151, 152, 155, 156, 157] +
        [182, 183, 184, 185, 186, 187, 188, 189],
    12: [134, 135, 136, 137, 140, 141, 142, 143, 148, 149, 150, 151, 152, 155, 156, 157, 158] +
        [181, 182, 183, 184, 185, 186, 187, 188, 189]
}

empty = [69, 70, 86, 88, 153, 154]

player = Player(150, 100, world)

camera = Camera()

Goomba(750, 300, world)

for i in range(1, WIDTH + 1):
    if i in empty:
        continue
    Floor(i, 13, world)
    Floor(i, 14, world)

for y in bricks:
    for x in bricks[y]:
        Brick(x, y, world)

for y in quests:
    for x in quests[y]:
        Quest(x, y, world, 'upsizemushroom')

for y in stones:
    for x in stones[y]:
        CastleBlock(x, y, world)

for y in tubes:
    for x, pow in tubes[y]:
        Tube(x, y, pow)
