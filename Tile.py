import pygame
from Utilities import *
from Items import *
import random


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, dx, dy, image):
        super().__init__(all_sprites, particles_group)
        self.image = pygame.transform.rotate(
            pygame.transform.scale(image, (image.get_width() // 2, image.get_height() // 2)),
            random.randint(30, 60))

        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if self.rect.y > HEIGHT:
            self.kill()


class TilesBase(pygame.sprite.Sprite):
    ITEMS = {'MushroomSizeUp': MushroomSizeUp, 'MushroomLiveUp': MushroomLiveUp,
             'MushroomDeadly': MushroomDeadly, 'FireFlower': FireFlower, 'Star': Star, 'Coin': Coin}
    IMAGES = {name: surf for name, surf in
              zip(['normal', 'underground', 'castle', 'underwater'],
                  cut_sheet(load_image("Tile.png"), 11, 4))}

    def __init__(self, x, y):
        super().__init__(all_sprites, tiles_group)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move((x - 1) * PPM, y * PPM)

    def interact(self, mario_state):
        pass

    def create_particles(self):
        Particle(self.rect.topleft, -5, 0, self.image)
        Particle(self.rect.midtop, 5, 0, self.image)
        Particle(self.rect.midleft, -5, 5, self.image)
        Particle(self.rect.center, 5, 5, self.image)

    def kill_enemies(self):
        [enemy.fast_die() for enemy in pygame.sprite.spritecollide(self, enemies_group, False, self.check_enemy_collide)]

    def check_enemy_collide(self, tile, enemy):
        return pygame.sprite.collide_rect(tile, enemy.down_side)


class Floor(TilesBase):
    def __init__(self, x, y, world):
        self.image = TilesBase.IMAGES[world][0]
        super().__init__(x, y)


class BrickPlain(TilesBase):
    def __init__(self, x, y, world):
        self.image = TilesBase.IMAGES[world][2]
        super().__init__(x, y)

    def interact(self, mario_state):
        self.kill_enemies()
        self.create_particles()
        self.kill()


class CastleBlock(TilesBase):
    def __init__(self, x, y, world):
        self.image = TilesBase.IMAGES[world][3]
        super().__init__(x, y)


class CubbleStone(TilesBase):
    def __init__(self, x, y, world):
        self.image = TilesBase.IMAGES[world][4]
        super().__init__(x, y)


class PavingStone(TilesBase):
    def __init__(self, x, y, world):
        self.image = TilesBase.IMAGES[world][5]
        super().__init__(x, y)


class Brick(TilesBase):
    def __init__(self, x, y, world, item=None):
        self.world = world
        self.image = TilesBase.IMAGES[world][1]
        self.stone_image = TilesBase.IMAGES[world][9]
        super().__init__(x, y)

        self.items = ([item] if item else []) * (random.randint(5, 10) if item == 'Coin' else 1)
        self.moving = False
        self.start_y = self.rect.y
        self.end_y = self.start_y - 14

    def interact(self, mario_state):
        if self.rect.y == self.start_y and self.image is not self.stone_image:
            self.kill_enemies()
            if self.items:
                item_obj = TilesBase.ITEMS[self.items.pop()]
                if item_obj is FireFlower and mario_state == 'small':
                    item_obj = MushroomSizeUp
                item_obj(self.rect.x, self.end_y, self.world)
                if not self.items:
                    self.image = self.stone_image
                self.moving = True
            elif mario_state == 'small':
                self.moving = True
            else:
                self.create_particles()
                self.kill()

    def update(self):
        self.move()

    def move(self):
        if self.moving:
            if self.rect.y > self.end_y:
                self.rect.y -= 3
            else:
                self.moving = False
        elif self.rect.y < self.start_y:
            self.rect.y += 3


class InvincibleTile(TilesBase):
    def __init__(self, x, y, world, item):
        self.x, self.y = x, y
        self.world = world
        self.item = item
        self.used = False
        self.image = TilesBase.IMAGES[world][10]
        super().__init__(x, y)

    def interact(self, mario_state):
        if self.used:
            return
        item_obj = TilesBase.ITEMS[self.item]
        if item_obj is FireFlower and mario_state == 'small':
            item_obj = MushroomSizeUp
        item_obj(self.rect.x, self.rect.y - 14, self.world)
        self.image = TilesBase.IMAGES[self.world][9]
        self.used = True


class Quest(TilesBase):
    def __init__(self, x, y, world, item):
        self.world = world
        self.frames = TilesBase.IMAGES[world][6:10]
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        super().__init__(x, y)

        self.item = item
        self.moving = False
        self.start_y = self.rect.y
        self.end_y = self.start_y - self.rect.h // 3

    def update(self):
        if self.image is not self.frames[3]:
            self.cur_frame = (self.cur_frame + 1) % 60
            self.image = self.frames[self.cur_frame // 10 % 3]
            self.move()

    def interact(self, mario_state):
        self.kill_enemies()
        if self.item:
            item_obj = TilesBase.ITEMS[self.item]
            if item_obj is FireFlower and mario_state == 'small':
                item_obj = MushroomSizeUp
            item_obj(self.rect.x, self.end_y, self.world)
            self.item = None
            self.moving = True

    def move(self):
        if self.moving:
            if self.rect.y > self.end_y:
                self.rect.y -= 3
            else:
                self.moving = False
        elif self.rect.y < self.start_y:
            self.rect.y += 3
            if self.rect.y == self.start_y:
                self.image = self.frames[3]

class Stone(TilesBase):
    def __init__(self, x, y, world):
        self.image = TilesBase.IMAGES[world][9]
        super().__init__(x, y)


class Decor(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__(all_sprites, decor_group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect = self.rect.move((x - 1) * PPM, y * PPM)


class GrassHill(Decor):
    image = load_image("grass_hill.png")

    def __init__(self, x, y, height):
        super().__init__(x, y - height + 1, GrassHill.image)


class Grass(Decor):
    image = load_image("grass.png")

    def __init__(self, x, y):
        super().__init__(x, y, Grass.image)


class Cloud(Decor):
    image = load_image("cloud.png")

    def __init__(self, x, y):
        super().__init__(x, y, Cloud.image)