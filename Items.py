import pygame
from Utilities import *
from BaseCharacter import BaseCharacter
from PointsUp import PointsUp


class ItemBase(BaseCharacter):
    ITEMS = {name: surf for name, surf in
             zip(['normal', 'underground', 'castle', 'underwater'],
                 cut_sheet(load_image("Items.png"), 19, 4))}

    def __init__(self, x, y):
        super().__init__(x, y, all_sprites, items_group)
        self.vx = 5
        self.uprise = self.rect.y - self.rect.h + self.rect.h // 3
        self.create_sides()

    def move(self):
        if self.uprise is not None and self.rect.y > self.uprise:
            self.rect.y -= 1
            if self.rect.y == self.uprise:
                self.uprise = None
            return True

    def update(self):
        if self.move():
            return
        self.update_coords()
        self.check_player_collisions()

        vx = self.vx
        self.check_tile_collisions()
        if vx != self.vx:
            self.image = pygame.transform.flip(self.image, True, False)

        self.sides_group.draw(screen)

    def show_points(self, collided, points):
        scores.append(PointsUp(collided.rect.left, collided.rect.top, points, scores))


class MushroomSizeUp(ItemBase):
    def __init__(self, x, y, world):
        self.image = ItemBase.ITEMS[world][0]
        super().__init__(x, y)

    def check_player_collisions(self):
        collided = pygame.sprite.spritecollideany(self, players_group)
        if collided:
            collided.set_state('big')
            print('+1000 Score')
            PointsUp(*collided.rect.topleft, 1000)
            hud.add_score(1000)
            self.kill()

    def create_top_side(self):
        pass

    def update_top_side(self):
        pass


class MushroomLiveUp(ItemBase):
    def __init__(self, x, y, world):
        self.image = ItemBase.ITEMS[world][1]
        super().__init__(x, y)

    def check_player_collisions(self):
        collided = pygame.sprite.spritecollideany(self, players_group)
        if collided:
            print('+1 live')
            hud.add_lives(1)
            self.kill()

    def create_top_side(self):
        pass

    def update_top_side(self):
        pass


class MushroomDeadly(ItemBase):
    def __init__(self, x, y, world):
        self.image = ItemBase.ITEMS[world][2]
        super().__init__(x, y)

    def check_player_collisions(self):
        collided = pygame.sprite.spritecollideany(self, players_group)
        if collided:
            collided.die()
            self.kill()

    def create_top_side(self):
        pass

    def update_top_side(self):
        pass


class FireFlower(ItemBase):
    def __init__(self, x, y, world):
        self.cur_frame = 0
        self.frames = ItemBase.ITEMS[world][3:7]
        self.image = self.frames[self.cur_frame]
        super().__init__(x, y)
        self.vx = 0

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % 60
        self.image = self.frames[self.cur_frame // 5 % 4]
        super().update()

    def check_player_collisions(self):
        collided = pygame.sprite.spritecollideany(self, players_group)
        if collided:
            collided.set_state('big', 'fire')
            self.kill()

    def check_tile_collisions(self):
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


class Star(ItemBase):
    def __init__(self, x, y, world):
        self.cur_frame = 0
        self.frames = ItemBase.ITEMS[world][7:11]
        self.image = self.frames[self.cur_frame]
        super().__init__(x, y)

        self.max_jumps = 8
        self.cur_jump = 0

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % 60
        self.image = self.frames[self.cur_frame // 5 % 4]
        if self.cur_jump < self.max_jumps:
            self.vy = - self.max_vy
            self.cur_jump += 1
        super().update()
        if pygame.sprite.spritecollideany(self.down_side, tiles_group):
            self.cur_jump = 0

    def check_player_collisions(self):
        collided = pygame.sprite.spritecollideany(self, players_group)
        if collided:
            collided.become_invincible(600, True)
            self.kill()

    def check_tile_collisions(self):
        super().check_tile_collisions()
        colided_tile = pygame.sprite.spritecollideany(self.top_side, tiles_group)
        if colided_tile:
            self.cur_jump = self.max_jumps
            self.rect.y = colided_tile.rect.bottom
            self.vy = max(0, self.vy)
            self.update_sides()


class CoinStatic(pygame.sprite.Sprite):
    def __init__(self, x, y, world):
        self.frames = ItemBase.ITEMS[world][11:15]
        self._load_image(x, y)

    def _load_image(self, x, y):
        super().__init__(all_sprites, items_group)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % 60
        self.image = self.frames[self.cur_frame // 5 % 4]
        self.check_player_collisions()

    def check_player_collisions(self):
        collided = pygame.sprite.spritecollideany(self, players_group)
        if collided:
            print('+1 coins')
            print('+200 score')
            hud.add_score(200)
            hud.add_coins(1)
            self.kill()


class Coin(CoinStatic):
    def __init__(self, x, y, world):
        self.frames = ItemBase.ITEMS[world][15:19]
        self._load_image(x, y)
        self.start_y = self.rect.y - self.rect.h
        self.end_y = self.start_y - self.rect.h * 2

        print('+1 coins')
        print('+200 score')
        hud.add_score(200)
        hud.add_coins(1)

    def update(self):
        super().update()
        if self.end_y is not None and self.rect.y > self.end_y:
            self.rect.y -= 7
            if self.rect.y <= self.end_y:
                self.end_y = None
        elif self.rect.y < self.start_y:
            self.rect.y += 7
            if self.rect.y >= self.start_y:
                self.kill()

    def check_player_collisions(self):
        pass


class Fire(BaseCharacter):
    IMAGES = cut_sheet(load_image("fire.png"), 4, 1)[0]
    FLYING = [col for row in cut_sheet(IMAGES[0], 2, 2) for col in row]
    EXPLODE = IMAGES[1:]

    def __init__(self, x, y, direction):
        self.cur_frame = 0
        self.image = Fire.FLYING[self.cur_frame]
        super().__init__(x, y, all_sprites, items_group)
        self.vx = 5 * direction

        self.explosion = False
        self.explosion_time = 0
        self.explosion_end = 17

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % 60

        if self.explosion:
            self.image = Fire.EXPLODE[self.explosion_time // 6]
            self.explosion_time += 1
            if self.explosion_time == self.explosion_end:
                self.kill()
            return

        self.image = Fire.FLYING[self.cur_frame // 15 % 4]
        self.update_coords()
        self.rect.x += self.vx
        self.check_tile_collisions()
        self.check_enemies_collisions()

        self.sides_group.draw(screen)

    def check_tile_collisions(self):
        self.update_sides()
        for side in [self.left_side, self.right_side]:
            colided_tile = pygame.sprite.spritecollideany(side, tiles_group)
            if colided_tile:
                self.vx = 0
                self.explosion = True
                self.update_sides()
                return

        colided_tile = pygame.sprite.spritecollideany(self.down_side, tiles_group)
        if colided_tile:
            self.rect.bottom = colided_tile.rect.y
            self.vy = -self.max_vy
            self.update_sides()

        colided_tile = pygame.sprite.spritecollideany(self.top_side, tiles_group)
        if colided_tile:
            self.rect.y = colided_tile.rect.bottom
            self.vy = self.max_vy
            self.update_sides()

    def check_enemies_collisions(self):
        collided_enemy = pygame.sprite.spritecollideany(self, enemies_group)
        if collided_enemy:
            collided_enemy.fast_die()
            self.explosion = True
