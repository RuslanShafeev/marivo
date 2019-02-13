from Tile import *
from Player import Player
from Goomba import Goomba
from Tube import Tube
from Koopa import *
from Castle import Castle
from FlagPole import *
import Map


class MapBase:
    RIGHT_ADD = 12

    def __init__(self, world_type, width, height):
        self.world_type = world_type
        self.width = width
        self.height = height
        self.castle = None
        self.flagpole = None

    def add_castle(self, x, y, is_big):
        self.castle = Castle(x, y, is_big)

    def add_flagpole(self, x, y):
        self.flagpole = FlagPole(x, y)

    def add_goombas(self, goombas):
        for y in goombas:
            for x in goombas[y]:
                Goomba(x, y, self.world_type)

    def add_koopas(self, koopas):
        for y in koopas:
            for x in koopas[y]:
                Koopa(x, y, self.world_type)

    def add_jkoopas(self, jkoopas):
        for y in jkoopas:
            for x in jkoopas[y]:
                JumpingKoopa(x, y, self.world_type)

    def add_quests(self, quests, sizeup=[], liveup=[], star=[], flower=[]):
        for y in quests:
            for x in quests[y]:
                quest = 'Coin'
                if (x, y) in sizeup:
                    quest = 'MushroomSizeUp'
                elif (x, y) in liveup:
                    quest = 'MushroomLiveUp'
                elif (x, y) in star:
                    quest = 'Star'
                elif (x, y) in flower:
                    quest = 'FireFlower'
                Quest(x, y, self.world_type, quest)

    def add_tiles(self, tile_class, tiles):
        for y in tiles:
            for x in tiles[y]:
                tile_class(x, y, self.world_type)

    def add_enemies(self, enemy_class, enemies):
        for y in enemies:
            for x in enemies[y]:
                enemy_class(x, y, self.world_type)

    def add_floor(self, empty):
        for i in range(1, self.width + MapBase.RIGHT_ADD + 1):
            if i in empty:
                continue
            Floor(i, 13, self.world_type)
            Floor(i, 14, self.world_type)

    def add_tubes(self, tubes):
        for y in tubes:
            for x, pow in tubes[y]:
                Tube(x, y, pow)

    def add_decor(self, grass_hills=[], grass=[], clouds=[]):
        for y in grass_hills:
            for x, h in grass_hills[y]:
                GrassHill(x, y, h)
        for y in grass:
            for x in grass[y]:
                Grass(x, y)
        for y in clouds:
            for x in clouds[y]:
                Cloud(x, y)

    def add_world_name(self, world_name):
        self.world_name = world_name