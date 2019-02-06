import pygame
from Utilities import *
from BaseCharacter import BaseCharacter


class Goomba(BaseCharacter):
    def __init__(self, x, y, world):
        self.smert = 0
        self.SMERT_TIME = 5

        self.cur_frame = 0

        self.frames = BaseCharacter.ENEMIES[world]
        self.image = self.frames[self.cur_frame]

        super().__init__(x, y, all_sprites, enemies_group)
        self.vx = -1

    def update(self):
        if self.smert:
            self.smert += 1
            if self.smert == self.SMERT_TIME:
                self.kill()
            return

        self.cur_frame = (self.cur_frame + 1) % 60
        self.image = self.frames[self.cur_frame // 15 % 2]

        self.update_coords()

        self.check_tile_collisions()
        self.check_enemies_collisions()
        self.sides_group.draw(screen)

    def die(self):
        self.image = self.frames[2]
        self.smert = max(1, self.smert)
