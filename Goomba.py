import pygame
from Utilities import *
from PointsUp import PointsUp
from BaseCharacter import BaseCharacter


class Goomba(BaseCharacter):
    IMAGES = {name: surf for name, surf in
              zip(['normal', 'underground', 'castle', 'underwater'],
                  cut_sheet(load_image("Goomba.png"), 3, 4))}

    def __init__(self, x, y, world):
        self.smert = 0
        self.SMERT_TIME = 5

        self.cur_frame = 0

        self.frames = Goomba.IMAGES[world]
        self.image = self.frames[self.cur_frame]

        super().__init__((x - 1) * PPM, y * PPM, all_sprites, enemies_group)
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

    def die(self, rate):
        self.image = self.frames[2]
        self.smert = max(1, self.smert)
        PointsUp(*self.rect.topleft, 200 * rate)
        hud.add_score(200 * rate)

    def fast_die(self):
        self.die(0.5)