import Level1, Level2

world = 'normal'
player_type = 'normal'
player_state = 'small'

lvl1 = Level1
lvl2 = Level2
cur = lvl1


def load_level(lvl, utils=None):
    global cur, map, player
    if utils is not None:
        utils.hud.info['SCORE'] = 0
        utils.hud.info['TIME'] = 400
        utils.hud.info['WORLD'] = '1-2'
        utils.hud.count = False
        utils.all_sprites.empty()
        utils.decor_group.empty()
        utils.players_group.empty()
        utils.enemies_group.empty()
        utils.tiles_group.empty()
        utils.castle_group.empty()
        utils.items_group.empty()
        utils.particles_group.empty()
    cur = lvl
    map, player = cur.init()


load_level(cur)