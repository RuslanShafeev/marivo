import pygame
from Utilities import *
from Map import *


class Goomba(pygame.sprite.Sprite):
    image = cut_sheet(load_image("goomba.png"), 3, 1)
    image_ug = cut_sheet(load_image("goomba_ug.png"), 3, 1)

    def __init__(self, x, y, ug):
        super().__init__(all_sprites, enemies_group)
        self.smert = 0
        self.SMERT_TIME = 5
        self.frames = Goomba.image if not ug else Goomba.image_ug
        self.state = 0
        self.dir = 1
        self.image = self.frames[0][self.state]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.a = 0.5
        self.step_x = 1
        self.frame_time = 0

        self.create_sides()

    def update(self):
        if self.smert > 0:
            self.image = self.frames[0][2]
            self.smert += 1
            if self.smert == self.SMERT_TIME:
                self.kill()
            return
        self.frame_time += 1
        if self.frame_time == 20:
            self.state ^= 1
            self.image = self.frames[0][self.state]
            self.frame_time = 0
        self.rect.y += self.a * 2
        self.rect.x += self.dir * self.step_x

        self.check_collisions()
        self.sides_group.draw(screen)

    def check_collisions(self):
        self.update_sides()

        colided_tile = pygame.sprite.spritecollideany(self.left_side, tiles_group)
        if colided_tile:
            self.rect.x = colided_tile.rect.right
            self.dir *= -1
            self.update_sides()

        colided_tile = pygame.sprite.spritecollideany(self.right_side, tiles_group)
        if colided_tile:
            self.rect.right = colided_tile.rect.x
            self.dir *= -1
            self.update_sides()

        colided_tile = pygame.sprite.spritecollideany(self.down_side, tiles_group)
        if colided_tile:
            self.rect.bottom = colided_tile.rect.y
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
        self.left_side.image = pygame.Surface((1, self.rect.h - 2))
        self.left_side.image.fill((0, 255, 0))
        self.right_side.image = pygame.Surface((1, self.rect.h - 2))
        self.right_side.image.fill((0, 255, 0))

    def update_sides(self):
        self.top_side.rect = pygame.Rect(self.rect.x, self.rect.y - 1,
                                         self.rect.w, 1)
        self.down_side.rect = pygame.Rect(self.rect.x, self.rect.bottom, self.rect.w, 1)

        self.left_side.rect = pygame.Rect(self.rect.x - 1, self.rect.y, 1,
                                          self.rect.h - 1)
        self.right_side.rect = pygame.Rect(self.rect.right, self.rect.y, 1,
                                           self.rect.h - 1)

    def die(self):
        if self.smert > 0:
            return
        self.smert = 1