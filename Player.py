import pygame
from Utilities import *
from Map import *
from Goomba import Goomba
from BaseCharacter import *
from Castle import Castle
from FlagPole import *
from Items import Fire


class Player(Character):
    def __init__(self, x, y, world):
        self.world = world
        self.type = self.world
        self.state = 'big'
        self.MARIO_IMAGES = self.load_images()
        self.alpha_surface = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.load_frames()
        self.max_vx = 5
        super().__init__(x, y, players_group)

        self.vx = 0
        self.a = 0.5
        self.died = False
        self.killing = False
        self.killing_rate = 1
        self.invincibility = 0  # Время неуязвимости в кадрах
        self.blinking = 0
        self.blinking_freq = 30

        self.max_jumps = 17
        self.cur_jump = 0

        self.flagpoled = -1
        self.end_speed = 4

    def load_images(self):
        images = {}
        for name, s_surf, b_surf in zip(['normal', 'fire', 'luigi', 'star_1', 'star_2', 'star_3',
                                         'underground_1', 'underground_2', 'castle',
                                         'underwater_1', 'underwater_2'],
                                        cut_sheet(load_image('Mario.png'), 14, 11),
                                        cut_sheet(load_image('Big_Mario.png'), 19, 11)):
            images[name] = {'small': s_surf, 'big': b_surf}
        return images

    def load_frames(self):
        self.cur_frame = 0
        self.frames = self.MARIO_IMAGES[self.type][self.state]
        self.l_frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]
        self.r_frames = self.frames
        self.image = self.frames[self.cur_frame]

    def update_frames(self):
        bottomleft = self.rect.bottomleft
        self.load_frames()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = bottomleft
        self.create_sides()

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % 60
        self.update_invincibility()
        self.vx = max(min(self.vx, self.max_vx), -self.max_vx)
        if self.flagpoled == 1:
            if self.rect.x >= Map.map.castle.get_centre():
                self.kill()
            self.rect.x += self.end_speed
            self.cur_jump = self.max_jumps
            self.walking()
        self.update_coords()

        if self.flagpoled == 0 and self.rect.y >= PPM * 10:
            self.flagpoled = 1

        if self.died:
            self.image = self.frames[5]
            self.jump()
            return

        self.check_tile_collisions()
        self.check_enemies_collisions()
        self.check_flagpole_collision()

        self.update_blincking()

        self.sides_group.draw(screen)

    def update_invincibility(self):
        if self.invincibility:
            self.invincibility -= 1
            if not self.invincibility:
                self.killing = False

    def update_blincking(self):
        if self.blinking:
            self.blinking -= 1
            if self.cur_frame // (100 / self.blinking_freq) % 2:
                self.image = self.alpha_surface

    def check_tile_collisions(self):
        self.update_sides()
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
            self.killing_rate = 1
        else:
            self.image = self.frames[4]

        colided_tile = pygame.sprite.spritecollideany(self.top_side, tiles_group)
        if colided_tile:
            self.cur_jump = self.max_jumps
            colided_tile.interact(self.state)

            self.rect.y = colided_tile.rect.bottom
            self.vy = max(0, self.vy)
            self.update_sides()

    def check_enemies_collisions(self):
        self.update_sides()
        if self.killing:
            colided_enemies = pygame.sprite.spritecollide(self, enemies_group, False)
            [enemy.die(len(colided_enemies) // 2) for enemy in colided_enemies]
            return
        for side in [self.left_side, self.right_side]:
            colided_enemy = pygame.sprite.spritecollideany(side, enemies_group)
            if colided_enemy:
                if self.set_state(self.world, 'small'):
                    self.become_invincible(120)
                elif not self.invincibility:
                    self.die()
                return

        colided_enemies = pygame.sprite.spritecollide(self.down_side, enemies_group, False)
        if colided_enemies and self.vy > 0:
            self.rect.bottom = colided_enemies[0].rect.y
            self.vy = min(0, self.vy)
            self.update_sides()
            self.cur_jump = 0
            self.jump()
            self.killing_rate = max(self.killing_rate, len(colided_enemies) ** 2)
            [enemy.die(self.killing_rate) for enemy in colided_enemies]
            self.killing_rate += 1

    def check_flagpole_collision(self):
        self.update_sides()
        if self.flagpoled > -1:
            return
        colided_flagpole = pygame.sprite.spritecollideany(self.right_side, castle_group)
        if colided_flagpole:
            if isinstance(colided_flagpole, FlagPole):
                self.flagpoled = 0
                self.vx = 0
                self.rect.x = colided_flagpole.rect.x - PPM // 2

    def jump(self):
        if self.cur_jump < self.max_jumps:
            self.vy = -self.max_vy
            self.cur_jump += 1

    def right(self):
        if self.frames is not self.r_frames:
            self.frames = self.r_frames

        if self.vx < 0:
            self.image = self.frames[3]
        elif self.vx:
            self.walking()
        else:
            self.image = self.frames[6]
        self.vx += self.a

    def left(self):
        if self.frames is not self.l_frames:
            self.frames = self.l_frames
        if self.vx > 0:
            self.image = self.frames[3]
        elif self.vx:
            self.walking()
        else:
            self.image = self.frames[6]
        self.vx -= self.a

    def walking(self):
        self.image = self.frames[self.cur_frame * abs(self.max_vx) // 50 % 3]

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

                elif event.key == pygame.K_x and self.type == 'fire':
                    Fire(*self.rect.center, 1 if self.frames is self.r_frames else -1)


        if self.died or self.flagpoled >= 0:
            return

        self.max_vx = 10 if pygame.key.get_pressed()[pygame.K_LSHIFT] else 5

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
            if abs(self.a) <= abs(self.vx):
                self.vx -= 1 if self.vx > 0 else -1 * self.a
                self.walking()
            else:
                self.vx = 0
                self.image = self.frames[6]

    def create_top_side(self):
        self.top_side = pygame.sprite.Sprite(self.sides_group)
        self.top_side.image = pygame.Surface((self.rect.w // 2, 1))
        self.top_side.image.fill((0, 255, 0))

    def update_top_side(self):
        self.top_side.rect = pygame.Rect(self.rect.x + self.rect.w // 4, self.rect.y - 1,
                                         self.rect.w // 2, 1)

    def set_state(self, new_type, new_state):
        if self.state != new_state or self.type != new_type:
            self.type, self.state = new_type, new_state
            self.update_frames()
            self.blinking = 120
            self.blinking_freq = 30
            return True

    def die(self):
        self.vx = 0
        self.set_state(self.world, 'small')
        self.died = True
        self.cur_jump = 0
        self.jump()
        hud.add_lives(-1)

    def become_invincible(self, time, killing=False):
        self.killing = killing
        self.invincibility = time
        if killing:
            self.blinking = time
            self.blinking_freq = 10