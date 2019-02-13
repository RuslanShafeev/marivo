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
    world_name = '1-1'

    empty = [69, 70, 86, 88, 153, 154]
    bricks = {
        5: [80, 81, 82, 83, 84, 85, 86, 87, 91, 92, 93, 121, 122, 123, 128, 131],
        9: [21, 23, 25, 77, 79, 100, 118, 129, 130, 168, 169, 171]
    }

    quests = {
        5: [23, 94, 109, 129, 130],
        9: [17, 22, 24, 78, 101, 106, 109, 112, 170]
    }
    flower = [(109, 5)]
    sizeup = [(22, 9), (78, 9)]
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
    grass_hills = {
        12: [(1, 2), (16, 1), (48, 2), (64, 1), (96, 2),
             (112, 1), (144, 2), (160, 1), (192, 2), (208, 1), (212, 2)]
    }
    grass = {
        12: [11, 13, 23, 41, 60, 71, 90, 108, 120, 137, 158, 168, 206]
    }
    clouds = {
        1: [12, 31, 56, 78, 92, 94, 100, 138, 160, 172, 202, 209],
        2: [4, 23, 42, 63, 84, 106, 121, 135, 142, 157, 213]
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
    InvincibleTile(64, 8, world, "MushroomLiveUp")
    Brick(94, 9, Map.world, "Coin")
    map.add_quests(quests, sizeup=sizeup, liveup=liveup, star=star, flower=flower)
    map.add_tubes(tubes)
    for enemy_class, enemies_arr in enemies:
        map.add_enemies(enemy_class, enemies_arr)
    map.add_decor(grass_hills=grass_hills, grass=grass, clouds=clouds)
    map.add_world_name(world_name)

    player = Player(3.5, 11, Map.player_state, Map.player_type, Map.world)

    return map, player
