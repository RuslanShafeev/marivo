import pygame
import os
import sys
from collections import OrderedDict


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    image_rect = image.get_rect()
    return pygame.transform.scale(image, (image_rect.w * 3, image_rect.h * 3))


def cut_sheet(sheet, columns, rows):
    frames = []
    width, height = sheet.get_width() // columns, sheet.get_height() // rows
    for row in range(rows):
        frames_line = []
        for col in range(columns):
            frame_location = (width * col, height * row)
            frames_line.append(sheet.subsurface(pygame.Rect(frame_location, (width, height))))
        frames.append(frames_line)
    return frames


class Hud:
    FONT = "data/SuperMario256.ttf"

    def __init__(self):
        self.font = pygame.font.Font(Hud.FONT, 40)

        self.info = OrderedDict([("SCORE", 0), ("TIME", 400), ("WORLD", "1-1"), ("COINS", 0),
                                 ("LIVES", 3)])
        self.first_line = [(key, self.font.render(key, 1, pygame.Color('White'))) for key in
                           self.info.keys()]
        self.first_line_width = sum([item[1].get_width() for item in self.first_line])
        self.h_indent = (WIDTH - self.first_line_width) // (len(self.first_line) + 1)
        self.v_indent = 10
        self.last_frame = FPS - 1
        self.cur_frame = 0
        self.count = False

    def update(self):
        if self.count:
            if self.info['TIME']:
                self.info['TIME'] -= 1
                self.info['SCORE'] += 50
            else:
                self.count = False
        else:
            self.cur_frame = (self.cur_frame + 1) % 60
            if self.cur_frame == self.last_frame and self.info['TIME']:
                self.info['TIME'] -= 1

    def draw(self, screen):
        x = self.h_indent
        for key, key_surf in self.first_line:
            screen.blit(key_surf, (x, self.v_indent))
            val_surf = self.font.render(str(self.info[key]), 1, pygame.Color('White'))
            screen.blit(val_surf, (x + (key_surf.get_width() - val_surf.get_width()) // 2,
                                   self.v_indent + key_surf.get_height()))
            x += self.h_indent + key_surf.get_width()

    def start_count(self):
        self.count = True

    def add_score(self, score):
        self.info["SCORE"] += int(score)

    def set_score(self, score):
        self.info["SCORE"] = int(score)

    def set_world(self, world):
        self.info["WORLD"] = str(world)

    def add_coins(self, coins):
        self.info["COINS"] += int(coins)

    def set_coins(self, coins):
        self.info["COINS"] = int(coins)

    def add_lives(self, lives):
        self.info["LIVES"] += int(lives)

    def set_lives(self, lives):
        self.info["LIVES"] = int(lives)


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        if obj.rect.right < 0:
            obj.kill()

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = min(0, -(target.rect.x + target.rect.w // 2 - WIDTH // 2))
        target.rect.x += self.dx
        if target.rect.x <= 0:
            target.rect.x = 0
            target.vx = max(0, target.vx)


pygame.init()
PPM = 48
FPS = 60
SIZE = WIDTH, HEIGHT = 32 * PPM, 15 * PPM
GRAVITY = 1
screen = pygame.display.set_mode(SIZE)
world = 'normal'

camera = Camera()
hud = Hud()

all_sprites = pygame.sprite.Group()
decor_group = pygame.sprite.Group()
players_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
castle_group = pygame.sprite.Group()
items_group = pygame.sprite.Group()
particles_group = pygame.sprite.Group()