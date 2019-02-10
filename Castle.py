import pygame
from Map import *
from Utilities import *


class Castle(pygame.sprite.Sprite):
    image = load_image("castle_big.png")
    SMALL_HEIGHT = 4
    BIG_HEIGHT = 10

    def __init__(self, x, y, is_big):
        super().__init__(all_sprites, castle_group)
        self.cx = x
        self.image = Castle.image
        self.rect = self.image.get_rect()
        x_off = 4
        if not is_big:
            y -= Castle.SMALL_HEIGHT
        else:
            y -= Castle.BIG_HEIGHT
        self.rect.x, self.rect.y = (x - x_off - 1) * PPM, y * PPM
        print(self.rect)

    def get_centre(self):
        return self.rect.x + 4 * PPM