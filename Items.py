import pygame
from Utilities import *
from BaseCharacter import BaseCharacter


class UpSizeMushroom(BaseCharacter):
    def __init__(self, x, y, world):
        self.image = BaseCharacter.ITEMS[world][0]
        super().__init__(x, y, all_sprites, items_group)
        self.vx = 5
        self.create_sides()

    def update(self):
        self.update_coords()
        self.check_player_collisions()
        self.check_tile_collisions()
        self.sides_group.draw(screen)

    def check_player_collisions(self):
        collided = pygame.sprite.spritecollideany(self.left_side, players_group)
        if collided and collided.mario_state == 'small':
            collided.mario_state = 'big'
            collided.update_frames(collided.rect.x, collided.rect.y - collided.rect.h)
            self.kill()

    def create_top_side(self):
        pass

    def update_top_side(self):
        pass
