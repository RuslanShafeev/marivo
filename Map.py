from MapBase import MapBase
import json
from Tile import *
from Goomba import Goomba
from Koopa import Koopa, JumpingKoopa
from collections import defaultdict

player_type = 'normal'  # Тип игрока. может быть normal, fire
player_state = 'small'  # состояние игрока. Может быть small, big


def load_json(name):
    """Метод безопасной загрузки и преобразования json-файла"""
    fullname = os.path.join('data', 'levels', name + '.json')
    try:
        with open(fullname, encoding='utf8') as file:
            lvl = defaultdict(list, json.loads(file.read()))
    except Exception as message:
        print('Cannot load level:', fullname)
        raise SystemExit(message)
    # Ключи в словарях в json не могут быть int и float, поэтому приходится приводить тип
    for key in lvl:
        if type(lvl[key]) is dict:
            for deep_key in list(lvl[key]):
                lvl[key][float(deep_key)] = lvl[key][deep_key]
                del lvl[key][deep_key]
    return lvl


def load_level(lvl, utils, resetscore=False):
    """Функция, удаляющая все старые и создающая новые спрайты на экране,
    т.е. загружающая уровень"""
    global cur, map, player
    cur = lvl
    utils.hud.reset(resetscore)  # Обнуляем hud перед загрузкой новой карты
    if resetscore:  # Обнуляем тип и состояние игрока, если нужно
        global player_state, player_type
        player_state, player_type = 'small', 'normal'

    # Полностью очищаем экран
    utils.all_sprites.empty()
    [group.empty() for group in utils.groups]

    level = load_json(lvl)  # Загружаем и преобразуем json

    # Создаем класс карты, наполняем экран новыми спрайтами
    map = MapBase(level['world'], *level["size"])
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
    player = map.add_player(level["player"], player_state, player_type)
    utils.hud.set_world(map.world_name)  # Не забываем про название уровня в hud


def get_player():
    return player

def get_map():
    return map