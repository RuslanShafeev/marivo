import Utilities
from MapBase import MapBase
from Player import Player
import json
from Items import *
from Tile import *
from Goomba import Goomba
from Koopa import Koopa, JumpingKoopa
from collections import defaultdict

world = 'normal'
player_type = 'normal'
player_state = 'small'
player = None


def load_json(name):
    fullname = os.path.join('levels', name + '.json')
    try:
        with open(fullname, encoding='utf8') as file:
            lvl = defaultdict(list, json.loads(file.read()))
    except Exception as message:
        print('Cannot load level:', fullname)
        raise SystemExit(message)
    for key in lvl:
        if type(lvl[key]) is dict:
            for deep_key in list(lvl[key]):
                lvl[key][float(deep_key)] = lvl[key][deep_key]
                del lvl[key][deep_key]
    return lvl


def load_level(lvl, utils, resetscore=False):
    global cur, map, player
    cur = lvl
    utils.hud.reset(resetscore)
    if resetscore:
        global player_state, player_type, world
        player_state, player_type, world = 'small', 'normal', 'normal'
    utils.all_sprites.empty()
    [group.empty() for group in utils.groups]

    level = load_json(lvl)

    map = MapBase(world, *level["size"])
    map.add_floor(level["empty"])
    map.add_castle(*level["castle"])
    map.add_flagpole(*level["flagpole"])

    map.add_tiles(Brick, level["bricks"])
    map.add_tiles(CastleBlock, level["stones"])

    map.add_quests(level["quests"], sizeup=level["sizeup"], liveup=level["liveup"],
                   star=level["star"], flower=level["flower"])
    map.add_tubes(level["tubes"])
    map.add_enemies(Goomba, level["goombas"])
    map.add_enemies(Koopa, level["koopas"])
    map.add_enemies(JumpingKoopa, level["jkoopas"])
    map.add_decor(grass_hills=level["grass_hills"], grass=level["grass"], clouds=level["clouds"])
    map.add_world_name(level["world_name"])
    map.add_bonus_brick(level["BonusBrick"])
    map.add_invisible_tile(level["InvincibleTile"])

    player = map.add_player(level["player"], player_state, player_type, world)
    utils.hud.set_world(map.world_name)

