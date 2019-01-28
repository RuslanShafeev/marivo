import pygame
from Utilities import *
from Map import *


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, players_group)

        self.frames = cut_sheet(load_image('mario_bros.png'), 19, 1)[0]
        self.left_frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]
        self.right_frames = self.frames

        self.cur_frame = 0

        self.jumping = False
        self.max_jumps = 15
        self.cur_jump = 0

        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()

        self.rect = self.rect.move(x, y)

        self.vx = 0
        self.vy = 0
        self.a = 0.5
        self.max_v = 10

        self.create_sides()

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % 60
        self.vy += self.a * 2

        self.vx = max(min(self.vx, self.max_v), -self.max_v)
        self.vy = max(min(self.vy, self.max_v), -self.max_v)

        self.rect = self.rect.move(self.vx, self.vy)

        if pygame.sprite.spritecollideany(self.down_side, tiles_group):
            self.cur_jump = 0
        else:
            self.image = self.frames[4]

        self.prevent_falling()
        if pygame.sprite.spritecollide(self.top_side, tiles_group, True):
            self.jumping = False
        self.sides_group.draw(screen)

    def prevent_falling(self):
        self.update_sides()
        for side, x, y in [(self.down_side, 0, 1), (self.top_side, 0, -1), (self.left_side, -1, 0),
                           (self.right_side, 1, 0)]:
            if pygame.sprite.spritecollideany(side, tiles_group):
                while pygame.sprite.spritecollideany(side, tiles_group):
                    self.rect.x -= x
                    self.rect.y -= y
                    self.update_sides()
                self.rect.x += x
                self.rect.y += y
                self.update_sides()
                if x != 0:
                    self.vx = x // abs(x) * min(x // abs(x) * self.vx, 0)
                if y != 0:
                    self.vy = y // abs(y) * min(y // abs(y) * self.vy, 0)

    def jump(self):
        if self.cur_jump < self.max_jumps:
            self.jumping = True
            self.vy = -self.max_v
            self.cur_jump += 1
        else:
            self.jumping = False

    def right(self):
        if self.frames is not self.right_frames:
            self.frames = self.right_frames

        if self.vx < 0:
            self.image = self.frames[3]
        elif self.vx:
            self.image = self.frames[self.cur_frame // 5 % 3]
        else:
            self.image = self.frames[6]
        self.vx += self.a

    def left(self):
        if self.frames is not self.left_frames:
            self.frames = self.left_frames
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

        if self.jumping and not any_key_pressed:
            if pygame.key.get_pressed()[pygame.K_UP]:
                self.jump()
                any_key_pressed = True
            else:
                self.jumping = False


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
        self.down_side.image = pygame.Surface((self.rect.w - self.max_v * 2, 1))
        self.down_side.image.fill((0, 255, 0))
        self.left_side.image = pygame.Surface((1, self.rect.h - self.max_v * 2))
        self.left_side.image.fill((0, 255, 0))
        self.right_side.image = pygame.Surface((1, self.rect.h - self.max_v * 2))
        self.right_side.image.fill((0, 255, 0))

    def update_sides(self):
        self.top_side.rect = pygame.Rect(self.rect.x + self.max_v, self.rect.y - 1,
                                         self.rect.w - self.max_v * 2, 1)
        self.down_side.rect = pygame.Rect(self.rect.x + self.max_v, self.rect.bottom,
                                          self.rect.w - self.max_v * 2, 1)
        self.left_side.rect = pygame.Rect(self.rect.x - 1, self.rect.y + self.max_v, 1,
                                          self.rect.h - self.max_v * 2)
        self.right_side.rect = pygame.Rect(self.rect.right, self.rect.y + self.max_v, 1,
                                           self.rect.h - self.max_v * 2)
