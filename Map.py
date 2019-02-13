import Level1, Level2
import Utilities

world = 'normal'
player_type = 'normal'
player_state = 'small'

lvl1 = Level1
lvl2 = Level2
cur = lvl1


def load_level(lvl, utils, resetscore=False):
    global cur, map, player
    utils.hud.reset(resetscore)
    if resetscore:
        global player_state, player_type, world
        player_state, player_type, world = 'small', 'normal', 'normal'
    utils.all_sprites.empty()
    [group.empty() for group in utils.groups]
    cur = lvl
    map, player = cur.init()
    utils.hud.set_world(map.world_name)


load_level(cur, Utilities, resetscore=True)
