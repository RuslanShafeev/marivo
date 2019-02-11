from Tile import *
from Player import Player
from Goomba import Goomba
from Tube import Tube
from Koopa import *
from Castle import Castle
from FlagPole import *
from MapBase import MapBase


def init():
    world = 'normal'

    empty = [69, 70, 86, 88, 153, 154]
    bricks = {
        5: [80, 81, 82, 83, 84, 85, 86, 87, 91, 92, 93, 121, 122, 123, 128, 131],
        9: [21, 23, 25, 77, 79, 100, 118, 129, 130, 168, 169, 171]
    }

    quests = {
        5: [23, 94, 109, 129, 130],
        8: [64],
        9: [17, 22, 24, 78, 94, 101, 106, 109, 112, 170]
    }
    sizeup = [(22, 9), (78, 9), (109, 5)]
    liveup = [(64, 8)]
    star = [(101, 9)]

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
            [181, 182, 183, 184, 185, 186, 187, 188, 189, 198]
    }

    tubes = {
        12: [(28, 2), (38, 3), (46, 4), (57, 4), (163, 2), (179, 2)]
    }

    goombas = {
        12: [21, 40, 52, 54, 95, 96, 123, 125, 126, 128, 173, 175]
    }
    koopas = {
        6.25: [106]
    }

    tiles = [(Brick, bricks), (CastleBlock, stones)]
    enemies = [(Goomba, goombas), (Koopa, koopas)]

    castle = (204, 12, False)
    flagpole = (198, 12)

    map = MapBase(world, 212, 14)
    map.add_floor(empty)
    map.add_castle(*castle)
    map.add_flagpole(*flagpole)
    for tile_class, tiles_arr in tiles:
        map.add_tiles(tile_class, tiles_arr)
    map.add_quests(quests, sizeup=sizeup, liveup=liveup, star=star)
    map.add_tubes(tubes)
    for enemy_class, enemies_arr in enemies:
        map.add_enemies(enemy_class, enemies_arr)

    player = Player(3.5, 11, 'fire')

    return map, player