import pygame
from Utilities import *
from Map import *


class Goomba(pygame.sprite.Sprite):
    IMAGES = {name: surf for name, surf in
              zip(['normal', 'underground', 'castle', 'underwater'],
                  cut_sheet(load_image("Goomba.png"), 3, 4))}

    def __init__(self, x, y, world):
        super().__init__(all_sprites, enemies_group)
        self.smert = 0
        self.SMERT_TIME = 5

        self.cur_frame = 0

        self.frames = self.IMAGES[world]
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

        self.max_v = 10
        self.vy = 0
        self.step_x = -1

        self.create_sides()

    def update(self):
        if self.smert:
            self.image = self.frames[2]
            self.smert += 1
            if self.smert == self.SMERT_TIME:
                self.kill()
            return

        self.cur_frame = (self.cur_frame + 1) % 60
        self.image = self.frames[self.cur_frame // 15 % 2]

        self.vy += GRAVITY
        self.vy = max(min(self.vy, self.max_v), -self.max_v)
        self.rect = self.rect.move(self.step_x, self.vy)

        self.check_collisions()
        self.sides_group.draw(screen)

    def check_collisions(self):
        self.update_sides()

        colided_tile = pygame.sprite.spritecollideany(self.left_side, tiles_group.sprites() +
                                                      enemies_group.sprites())
        if colided_tile:
            self.rect.x = colided_tile.rect.right
            self.step_x = -self.step_x
            self.update_sides()

        colided_tile = pygame.sprite.spritecollideany(self.right_side, tiles_group.sprites() +
                                                      enemies_group.sprites())
        if colided_tile:
            self.rect.right = colided_tile.rect.x
            self.step_x = -self.step_x
            self.update_sides()

        colided_tile = pygame.sprite.spritecollideany(self.down_side, tiles_group.sprites() +
                                                      enemies_group.sprites())
        if colided_tile:
            self.rect.bottom = colided_tile.rect.y
            self.vy = min(0, self.vy)
            self.update_sides()

    def create_sides(self):
        self.sides_group = pygame.sprite.Group()
        self.top_side = pygame.sprite.Sprite(self.sides_group)
        self.down_side = pygame.sprite.Sprite(self.sides_group)
        self.left_side = pygame.sprite.Sprite(self.sides_group)
        self.right_side = pygame.sprite.Sprite(self.sides_group)
        self.update_sides()

        self.top_side.image = pygame.Surface((self.rect.w, 1))
        self.top_side.image.fill((0, 255, 0))
        self.down_side.image = pygame.Surface((self.rect.w, 1))
        self.down_side.image.fill((0, 255, 0))
        self.left_side.image = pygame.Surface((1, self.rect.h - self.max_v))
        self.left_side.image.fill((0, 255, 0))
        self.right_side.image = pygame.Surface((1, self.rect.h - self.max_v))
        self.right_side.image.fill((0, 255, 0))

    def update_sides(self):
        self.top_side.rect = pygame.Rect(self.rect.x, self.rect.y - 1,
                                         self.rect.w, 1)
        self.down_side.rect = pygame.Rect(self.rect.x, self.rect.bottom, self.rect.w, 1)

        self.left_side.rect = pygame.Rect(self.rect.x - 1, self.rect.y, 1,
                                          self.rect.h - self.max_v)
        self.right_side.rect = pygame.Rect(self.rect.right, self.rect.y, 1,
                                           self.rect.h - self.max_v)

    def die(self):
        self.smert = max(1, self.smert)
