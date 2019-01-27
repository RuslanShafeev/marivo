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


pygame.init()
SIZE = WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode(SIZE)

all_sprites = pygame.sprite.Group()
players_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()


class Player(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites, players_group)
        self.right_frames = []
        self.cut_sheet(sheet, columns, rows)
        self.left_frames = [pygame.transform.flip(frame, True, False) for frame in
                            self.right_frames]
        self.frames = self.right_frames

        self.cur_frame = 0


        self.jumping = False
        self.max_jumps = 15
        self.cur_jump = 0

        self.image = self.frames[self.cur_frame]

        self.rect = self.rect.move(x, y)

        self.vx = 0
        self.vy = 0
        self.a = 0.5
        self.max_v = 10

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.right_frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % 60
        self.vy += self.a

        if pygame.sprite.spritecollideany(self, tiles_group):
            self.vy = min(0, self.vy)
            self.cur_jump = 0
        else:
            self.image = self.frames[4]

        self.vx = max(min(self.vx, self.max_v), -self.max_v)
        self.vy = max(min(self.vy, self.max_v), -self.max_v)

        self.rect = self.rect.move(self.vx, self.vy)

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
        else:
            self.image = self.frames[self.cur_frame // 5 % 3]
        self.vx += self.a

    def left(self):
        if self.frames is not self.left_frames:
            self.frames = self.left_frames
        if self.vx > 0:
            self.image = self.frames[3]
        else:
            self.image = self.frames[self.cur_frame // 5 % 3]
        self.vx -= self.a

    def process_events(self, events_list):
        any_key_pressed = False

        for event in events_list:
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and pygame.sprite.spritecollideany(self, tiles_group):
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


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__(all_sprites, tiles_group)

        self.image = pygame.Surface((100, 100))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)


time = pygame.time.Clock()

player = Player(load_image('mario_bros.png'), 19, 1, 100, 100)
Tile(0, 600)
Tile(100, 600)
Tile(200, 600)
Tile(300, 600)
Tile(400, 600)

while True:
    player.process_events(pygame.event.get())
    screen.fill(pygame.Color('Blue'))
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    time.tick(60)
