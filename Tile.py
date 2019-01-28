import pygame
from Map import *
from Utilities import *


class Tile(pygame.sprite.Sprite):
    tiles = {name: surf for name, surf in zip(['Floor', 'Brick', 'BrickPlain', 'CastleBlock'],
                                              cut_sheet(load_image('tiles.png'), 28, 1)[0])}

    def __init__(self, x, y, name):
        super().__init__(all_sprites, tiles_group)

        self.image = Tile.tiles[name]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
