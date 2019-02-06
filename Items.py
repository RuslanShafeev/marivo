import pygame
from Utilities import *
from BaseCharacter import BaseCharacter


class MushroomBase(BaseCharacter):
    def __init__(self, x, y):
        super().__init__(x, y, all_sprites, items_group)
        self.vx = 5
        self.uprise = self.rect.y - self.rect.h + self.rect.h // 3
        self.create_sides()

    def update(self):
        if self.uprise is not None and self.rect.y > self.uprise:
            self.rect.y -= 1
            if self.rect.y == self.uprise:
                self.uprise = None
            return
        self.update_coords()
        self.check_player_collisions()

        vx = self.vx
        self.check_tile_collisions()
        if vx != self.vx:
            self.image = pygame.transform.flip(self.image, True, False)

        self.sides_group.draw(screen)

    def create_top_side(self):
        pass

    def update_top_side(self):
        pass


class MushroomSizeUp(MushroomBase):
    def __init__(self, x, y, world):
        self.image = BaseCharacter.ITEMS[world][0]
        super().__init__(x, y)

    def check_player_collisions(self):
        collided = pygame.sprite.spritecollideany(self, players_group)
        if collided:
            collided.set_state('big')
            print('+1000 Score')
            self.kill()


class MushroomLiveUp(MushroomBase):
    def __init__(self, x, y, world):
        self.image = BaseCharacter.ITEMS[world][1]
        super().__init__(x, y)

    def check_player_collisions(self):
        collided = pygame.sprite.spritecollideany(self, players_group)
        if collided:
            print('+1 live')
            self.kill()


class MushroomDeadly(MushroomBase):
    def __init__(self, x, y, world):
        self.image = BaseCharacter.ITEMS[world][2]
        super().__init__(x, y)

    def check_player_collisions(self):
        collided = pygame.sprite.spritecollideany(self, players_group)
        if collided:
            collided.set_state('small')
            collided.set_state('died')
            print('-1 live')
            self.kill()


class FireFlower(pygame.sprite.Sprite):
    def __init__(self, x, y, world):
        super().__init__(all_sprites, items_group)

        self.cur_frame = 0
        self.frames = BaseCharacter.ITEMS[world][3:7]
        self.image = self.frames[self.cur_frame]

        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.vy = 0
        self.max_v = 10
        self.uprise = self.rect.y - self.rect.h + self.rect.h // 3
        self.create_sides()

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % 60
        self.image = self.frames[self.cur_frame // 5 % 4]

        if self.uprise is not None and self.rect.y > self.uprise:
            self.rect.y -= 1
            if self.rect.y == self.uprise:
                self.uprise = None
            return

        self.vy += GRAVITY
        self.vy = max(min(self.vy, self.max_v), -self.max_v)
        self.rect.y += self.vy

        self.check_tile_collision()
        self.check_player_collisions()
        self.sides_group.draw(screen)

    def check_player_collisions(self):
        collided = pygame.sprite.spritecollideany(self, players_group)
        if collided:
            collided.set_state('fire', 'big')
            print('firemario')
            self.kill()

    def check_tile_collision(self):
        self.update_sides()
        colided_tile = pygame.sprite.spritecollideany(self.down_side, tiles_group)
        if colided_tile:
            self.rect.bottom = colided_tile.rect.y
            self.vy = min(0, self.vy)
            self.update_sides()

    def create_sides(self):
        self.sides_group = pygame.sprite.Group()
        self.down_side = pygame.sprite.Sprite(self.sides_group)
        self.update_sides()

        self.down_side.image = pygame.Surface((self.rect.w, 1))
        self.down_side.image.fill((0, 255, 0))

    def update_sides(self):
        self.down_side.rect = pygame.Rect(self.rect.x, self.rect.bottom, self.rect.w, 1)
