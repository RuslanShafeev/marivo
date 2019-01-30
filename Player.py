import pygame
from Utilities import *
from Map import *
from Goomba import Goomba


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, world):
        super().__init__(players_group)

        self.vx = 0
        self.vy = 0
        self.a = 0.5
        self.max_v = 10

        self.world = world
        self.mario_state = 'big'
        self.invincibility = 0   # Время неуязвимости в кадрах

        self.cur_frame = 0
        self.MARIO_IMAGES = self.load_images()
        self.load_frames(x, y)

        self.max_jumps = 15
        self.cur_jump = 0

    def load_images(self):
        images = {}
        for name, s_surf, b_surf in zip(['normal', 'fire', 'luigi', 'star_1', 'star_2', 'star_3',
                                         'underground_1', 'underground_2', 'castle',
                                         'underwater_1', 'underwater_2'],
                                        cut_sheet(load_image('Mario.png'), 14, 11),
                                        cut_sheet(load_image('Big_Mario.png'), 19, 11)):
            images[name] = {'small': s_surf, 'big': b_surf}
        return images

    def load_frames(self, x, y):
        self.frames = self.MARIO_IMAGES[self.world][self.mario_state]
        self.l_frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]
        self.r_frames = self.frames

        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.create_sides()

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % 60
        self.vy += self.a * 2

        self.invincibility = max(0, self.invincibility - 1)
        self.vx = max(min(self.vx, self.max_v), -self.max_v)
        self.vy = max(min(self.vy, self.max_v), -self.max_v)
        self.rect = self.rect.move(self.vx, self.vy)

        if self.mario_state == 'died':
            self.image = self.frames[5]
            self.jump()
            return

        self.check_collisions()
        self.sides_group.draw(screen)

    def check_collisions(self):
        self.update_sides()
        self.check_tile_collisions()
        self.check_enemies_collisions()

    def check_tile_collisions(self):
        colided_tile = pygame.sprite.spritecollideany(self.left_side, tiles_group)
        if colided_tile:
            self.rect.x = colided_tile.rect.right
            self.vx = max(0, self.vx)
            self.update_sides()

        colided_tile = pygame.sprite.spritecollideany(self.right_side, tiles_group)
        if colided_tile:
            self.rect.right = colided_tile.rect.x
            self.vx = min(0, self.vx)
            self.update_sides()

        colided_tile = pygame.sprite.spritecollideany(self.down_side, tiles_group)
        if colided_tile:
            self.rect.bottom = colided_tile.rect.y
            self.vy = min(0, self.vy)
            self.update_sides()
            self.cur_jump = 0
        else:
            self.image = self.frames[4]

        colided_tile = pygame.sprite.spritecollideany(self.top_side, tiles_group)
        if colided_tile:
            self.cur_jump = self.max_jumps
            colided_tile.kill()

            self.rect.y = colided_tile.rect.bottom
            self.vy = max(0, self.vy)
            self.update_sides()

    def check_enemies_collisions(self):
        for side in [self.left_side, self.right_side]:
            colided_enemy = pygame.sprite.spritecollideany(side, enemies_group)
            if colided_enemy:
                if self.mario_state == 'big':
                    self.mario_state = 'small'
                    self.cur_frame = 0
                    self.load_frames(self.rect.x, self.rect.bottom - self.rect.h // 2)
                    self.invincibility = 180
                elif self.mario_state == 'small' and not self.invincibility:
                    self.mario_state = 'died'
                    self.jump()
                    print("mario, vi sdohli")
                return

        colided_enemy = pygame.sprite.spritecollideany(self.down_side, enemies_group)
        if colided_enemy and self.vy > 0:
            self.rect.bottom = colided_enemy.rect.y
            self.vy = min(0, self.vy)
            self.update_sides()
            self.cur_jump = 0
            if isinstance(colided_enemy, Goomba):
                colided_enemy.die()

    def jump(self):
        if self.cur_jump < self.max_jumps:
            self.vy = -self.max_v
            self.cur_jump += 1

    def right(self):
        if self.frames is not self.r_frames:
            self.frames = self.r_frames

        if self.vx < 0:
            self.image = self.frames[3]
        elif self.vx:
            self.image = self.frames[self.cur_frame // 5 % 3]
        else:
            self.image = self.frames[6]
        self.vx += self.a

    def left(self):
        if self.frames is not self.l_frames:
            self.frames = self.l_frames
        if self.vx > 0:
            self.image = self.frames[3]
        elif self.vx:
            self.image = self.frames[self.cur_frame // 5 % 3]
        else:
            self.image = self.frames[6]
        self.vx -= self.a

    def process_events(self, events_list):
        any_key_pressed = False

        for event in events_list:
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and pygame.sprite.spritecollideany(self.down_side,
                                                                               tiles_group):
                    self.jump()
                    any_key_pressed = True

        if self.mario_state == 'died':
            return

        if self.cur_jump and not any_key_pressed:
            if pygame.key.get_pressed()[pygame.K_UP]:
                self.jump()
                any_key_pressed = True
            else:
                self.cur_jump = self.max_jumps

        for key, func in [(pygame.K_RIGHT, self.right), (pygame.K_LEFT, self.left)]:
            if pygame.key.get_pressed()[key]:
                func()
                any_key_pressed = True

        if not any_key_pressed:
            self.vx -= self.vx // max(abs(self.vx), 1) * self.a
            self.image = self.frames[6]

    def create_sides(self):
        self.sides_group = pygame.sprite.Group()
        self.top_side = pygame.sprite.Sprite(self.sides_group)
        self.down_side = pygame.sprite.Sprite(self.sides_group)
        self.left_side = pygame.sprite.Sprite(self.sides_group)
        self.right_side = pygame.sprite.Sprite(self.sides_group)
        self.update_sides()

        # Код ниже рисует зеленые линии вокруг Марио для дебага. Удалю, когда пойму, что коллизии работают корректно
        self.top_side.image = pygame.Surface((self.rect.w - self.max_v * 2, 1))
        self.top_side.image.fill((0, 255, 0))
        self.down_side.image = pygame.Surface((self.rect.w, 1))
        self.down_side.image.fill((0, 255, 0))
        self.left_side.image = pygame.Surface((1, self.rect.h - self.max_v * 2))
        self.left_side.image.fill((0, 255, 0))
        self.right_side.image = pygame.Surface((1, self.rect.h - self.max_v * 2))
        self.right_side.image.fill((0, 255, 0))

    def update_sides(self):
        self.top_side.rect = pygame.Rect(self.rect.x + self.max_v, self.rect.y - 1,
                                         self.rect.w - self.max_v * 2, 1)
        self.down_side.rect = pygame.Rect(self.rect.x, self.rect.bottom, self.rect.w, 1)

        self.left_side.rect = pygame.Rect(self.rect.x - 1, self.rect.y + self.max_v, 1,
                                          self.rect.h - self.max_v * 2)
        self.right_side.rect = pygame.Rect(self.rect.right, self.rect.y + self.max_v, 1,
                                           self.rect.h - self.max_v * 2)
