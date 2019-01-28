import pygame
import os
import sys


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


pygame.init()
SIZE = WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode(SIZE)

all_sprites = pygame.sprite.Group()
players_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
