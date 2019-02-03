import pygame
from Utilities import *


class TilesBase(pygame.sprite.Sprite):
    IMAGES = {name: surf for name, surf in
              zip(['normal', 'underground', 'castle', 'underwater'],
                  cut_sheet(load_image("Tile.png"), 10, 4))}

    def __init__(self, x, y):
        super().__init__(all_sprites, tiles_group)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move((x - 1) * PPM, y * PPM)

    def interact(self, mario_state):
        self.kill()

    def update(self):
        pass


class Floor(TilesBase):
    def __init__(self, x, y, world):
        self.image = TilesBase.IMAGES[world][0]
        super().__init__(x, y)


class Brick(TilesBase):
    def __init__(self, x, y, world):
        self.image = TilesBase.IMAGES[world][1]
        super().__init__(x, y)


class BrickPlain(TilesBase):
    def __init__(self, x, y, world):
        self.image = TilesBase.IMAGES[world][2]
        super().__init__(x, y)


class CastleBlock(TilesBase):
    def __init__(self, x, y, world):
        self.image = TilesBase.IMAGES[world][3]
        super().__init__(x, y)


class CubbleStone(TilesBase):
    def __init__(self, x, y, world):
        self.image = TilesBase.IMAGES[world][4]
        super().__init__(x, y)


class CubbleStone(TilesBase):
    def __init__(self, x, y, world):
        self.image = TilesBase.IMAGES[world][5]
        super().__init__(x, y)


class Quest(TilesBase):
    def __init__(self, x, y, world, item):
        self.frames = TilesBase.IMAGES[world][6:10]
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        super().__init__(x, y)

        self.moving = False
        self.max_delta = 5
        self.cur_delta = 0
        self.item = item

    def update(self):
        if self.image is self.frames[3]:
            return
        self.cur_frame = (self.cur_frame + 1) % 60
        self.image = self.frames[self.cur_frame // 10 % 3]
        if self.moving:
            if self.cur_delta < self.max_delta:
                self.rect.y -= 3
                self.cur_delta += 1
            else:
                self.moving = False
                print(self.item)
        elif self.cur_delta > 0:
            self.rect.y += 3
            self.cur_delta -= 1
            if not self.cur_delta:
                self.image = self.frames[3]

    def interact(self, mario_state):
        self.moving = True


class Stone(TilesBase):
    def __init__(self, x, y, world):
        self.image = TilesBase.IMAGES[world][10]
        super().__init__(x, y)
