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

    empty = [22, 87, 89, 90, 92, 94, 95, 97, 98, 99]
    bricks = {
        6: [141],
        7: [114, 115, 116, 117, 118, 139, 140],
        8: [11, 14, 17, 57, 58, 59, 60, 61, 62, 132, 138],
        9: [25, 100, 106, 108, 110, 133, 134, 135, 136, 137],
        10: [9, 19],
        11: [48],
        12: [7, 21, 130]
    }

    quests = {
        3: [55, 58, 61, 64, 116],
        4: [11, 14, 17, 96, 107, 109],
        5: [33, 93, 100],
        6: [88, 91],
        8: [64],
        9: [26, 107, 109, 144]
    }
    sizeup = [(17, 4), (100, 5)]
    liveup = [(33, 5)]
    star = [(64, 3)]
    flower = [(109, 4)]

    stones = {
        9: [93, 100],
        10: [88, 91, 93, 96, 100],
        11: [86, 88, 91, 93, 96, 100],
        12: [86, 88, 91, 93, 96, 100, 148]
    }

    tubes = {
        12: [(32, 2), (51, 4), (69, 3), (79, 3), (118, 3)]
    }

    goombas = {
        8: [134],
        12: [10, 12, 17, 43, 45, 55, 60, 73, 75, 77, 107, 109, 116, 123]
    }
    koopas = {
        12: [37, 57, 62, 83, 104, 127]
    }
    jkoopas = {
        12: [15, 66, 114]
    }
    grass_hills = {
        12: [(1, 2), (16, 1), (48, 2), (64, 1), (100, 2),
             (112, 1), (144, 2), (160, 1)]
    }
    grass = {
        12: [11, 13, 23, 41, 60, 71, 108, 120, 137, 165, 168]
    }
    clouds = {
        1: [12, 31, 56, 78, 92, 94, 100, 138, 162],
        2: [4, 23, 42, 63, 84, 106, 121, 135, 142, 157, 167]
    }

    tiles = [(Brick, bricks), (CastleBlock, stones)]
    enemies = [(Goomba, goombas), (Koopa, koopas), (JumpingKoopa, jkoopas)]

    castle = (155, 12, True)
    flagpole = (148, 12)

    map = MapBase(world, 160, 14)
    map.add_floor(empty)
    map.add_castle(*castle)
    map.add_flagpole(*flagpole)
    for tile_class, tiles_arr in tiles:
        map.add_tiles(tile_class, tiles_arr)
    map.add_quests(quests, sizeup=sizeup, liveup=liveup, star=star, flower=flower)
    map.add_tubes(tubes)
    for enemy_class, enemies_arr in enemies:
        map.add_enemies(enemy_class, enemies_arr)
    map.add_decor(grass_hills=grass_hills, grass=grass, clouds=clouds)

    player = Player(3.5, 11, Map.player_state, Map.player_type)

    return map, player