import pygame
from Map import *
from Utilities import *


class FlagPole(pygame.sprite.Sprite):
    image = load_image("flagpole.png")

    def __init__(self, x, y):
        super().__init__(all_sprites, castle_group)
        self.image = FlagPole.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (x - 1) * PPM, (y - 10) * PPM
        Flag(x, y)


class Flag(pygame.sprite.Sprite):
    image = load_image("flag.png")

    def __init__(self, x, y):
        super().__init__(all_sprites, castle_group)
        self.image = Flag.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (x - 1.5) * PPM, (y - 9) * PPM