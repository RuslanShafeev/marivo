from Tile import *
from Player import Player
from Goomba import Goomba
from Tube import Tube
from Camera import Camera
from Hud import Hud

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
sizeup_x = [(22, 9), (78, 9), (109, 5)]
liveup_x = [(64, 8)]
star_x = [(101, 9)]

tubes = {
    12: [(28, 2), (38, 3), (46, 4), (57, 4), (163, 2), (179, 2)]
}

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

goombas = {
    12: [21, 40, 52, 54, 95, 96, 123, 125, 126, 128]
}

TEXT_SIZE = 40
hud_texts = ["SCORE", 0, "TIME", 400, "WORLD", "1-1", "COINS", 0, "LIVES", 3]
huds = [None] * 5
dx = SIZE[0] // 6
for i in range(5):
    huds[i] = Hud(dx * (i + 1), 20, hud_texts[2 * i], hud_texts[2 * i + 1], TEXT_SIZE)


def add_score(score):
    set_score(int(huds[0].get_value()) + score)


def set_score(score):
    huds[0].set_value(score)


def add_coins(coins):
    set_coins(int(huds[3].get_value()) + coins)


def set_coins(coins):
    huds[3].set_value(coins)


def add_lives(lives):
    set_lives(int(huds[4].get_value()) + lives)

def set_lives(lives):
    huds[4].set_value(lives)

def tick():
    huds[1].set_value(int(huds[1].get_value()) - 1)

scores = []

player = Player(150, 100, world)

camera = Camera()

for y in goombas:
    for x in goombas[y]:
        Goomba(x, y, world)

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
        quest = 'Coin'
        if (x, y) in sizeup_x:
            quest = 'MushroomSizeUp'
        elif (x, y) in liveup_x:
            quest = 'MushroomLiveUp'
        elif (x, y) in star_x:
            quest = 'Star'
        Quest(x, y, world, quest)

for y in stones:
    for x in stones[y]:
        CastleBlock(x, y, world)

for y in tubes:
    for x, pow in tubes[y]:
        Tube(x, y, pow)
