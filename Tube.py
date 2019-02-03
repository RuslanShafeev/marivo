import pygame
from Map import *
from Utilities import *


class TubePart(pygame.sprite.Sprite):
    parts = {"Base": load_image("tube_base.png"), "Head": load_image("tube_head.png")}

    def __init__(self, part):
        super().__init__(all_sprites, tiles_group)

        self.image = TubePart.parts[part]
        self.rect = self.image.get_rect()

    def move(self, x, y):
        self.rect = self.rect.move((x - 1) * PPM, y * PPM)


class Tube:
    def __init__(self, x, y, pow):
        for i in range(pow - 1):
            tube_part = TubePart("Base")
            tube_part.move(x, y - i)
        tube_part = TubePart("Head")
        tube_part.move(x, y - pow + 1)