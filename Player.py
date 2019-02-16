import pygame
from Utilities import *
import Utilities
from BaseCharacter import Character
from FlagPole import *
from Items import Fire
from PointsUp import PointsUp
import Map


class Player(Character):
    """Собственно, сам Марио. Имеет множество состояний, анимаций, инерцию, занимается проверками на
    столкновения с врагами, блоками, замком"""

    def __init__(self, x, y, state, type, world):
        self.world = world  # Используется при откате типа игрока
        self.type = type  # Тип игрока. может быть normal, fire, luigi...
        self.state = state  # состояние игрока. Может быть small, big
        self.MARIO_IMAGES = self.load_images()  # Константа хранит все изображения Марио

        # Прозрачный пиксель. Используется в режиме мерцания
        self.alpha_surface = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.load_frames()
        self.max_vx = 5  # Максимальная горизонтальная скорость в пикселях на кадр
        super().__init__(x, y, players_group)

        self.vx = 0  # Горизонтальная скорость в пикселях на кадр
        self.a = 0.5  # Горизонтальное ускорение
        self.died = False
        self.killing = False  # Может ли Марио убивать врагов во время неуязвимости
        self.killing_rate = 1  # Множитель очков при убийстве врагов
        self.invincibility = 0  # Время неуязвимости в кадрах
        self.blinking = 0  # Оставшееся время мерцания
        self.blinking_freq = 30  # Коэффициент частоты мерцания

        # Количество кадров, когда у Марио будет максимальная отрицательная вертикальная скорость
        self.max_jumps = 17  # определяет максимальную высоту прыжка.
        self.cur_jump = 0  # Переменная-счетчик этих кадров. Определяет кол-во совершенных прыжков

        self.flagpoled = -1  # Положение Марио относительно флагштока
        self.end_speed = 4  # Горизонтальная скорость прогулки Марио от флагштока к замку

    def load_images(self):
        """Метод загрузки всех изображений и распределения их по категориям"""
        images = {}
        for name, s_surf, b_surf in zip(['normal', 'fire', 'luigi', 'star_1', 'star_2', 'star_3',
                                         'underground_1', 'underground_2', 'castle',
                                         'underwater_1', 'underwater_2'],
                                        cut_sheet(load_image('Mario.png'), 14, 11),
                                        cut_sheet(load_image('Big_Mario.png'), 19, 11)):
            images[name] = {'small': s_surf, 'big': b_surf}
        return images

    def load_frames(self):
        """Загрузка кадров для данного состояния и типа Марио и создание зеркальных кадров для
        другого направления"""
        self.cur_frame = 0  # Счетчик кадров
        self.frames = self.MARIO_IMAGES[self.type][self.state]
        self.l_frames = [pygame.transform.flip(frame, True, False) for frame in self.frames]
        self.r_frames = self.frames
        self.image = self.frames[self.cur_frame]

    def update_frames(self):
        """Метод позволяет переключаться на разные по высоте изображения Марио без изменения его
        положения, пересоздает коллизии"""
        bottomleft = self.rect.bottomleft
        self.load_frames()
        self.rect = self.image.get_rect()
        self.rect.bottomleft = bottomleft
        self.create_sides()

    def update(self):
        if self.rect.y > HEIGHT * 2:
            # Если Марио упал за пределы карты, в том числе из-за отключения коллизий после смерти
            Map.load_level(Map.cur, Utilities, resetscore=True)  # перезагруажем уровень
            hud.add_lives(-1)  # Отнимаем одну жизнь
        self.cur_frame = (self.cur_frame + 1) % 60  # Обновление счетчика кадров
        self.update_invincibility()  # Обновление счетчика неуязвимости
        self.vx = max(min(self.vx, self.max_vx), -self.max_vx)  # Ограничение горизонт. скорости

        self.update_flagpoled()  # Проигрывание анимаций в конце уровня
        self.update_coords()

        if self.died:  # Анимация смерти и отключение коллизий
            self.image = self.frames[5]
            self.jump()
            return

        # Взаимодействия с тайлами, врагами, флагштоком
        self.check_tile_collisions()
        self.check_enemies_collisions()
        self.check_flagpole_collision()

        self.update_blincking()  # Анимация мерцания

        self.sides_group.draw(screen)  # Отрисовка коллизий

    def update_flagpoled(self):
        """Анимации в конце уровня"""
        if self.flagpoled == 1:  # Прогулка от флажка до замка
            if self.rect.x >= Map.map.castle.get_centre():
                self.kill()  # Вход в дверь замка
            self.rect.x += self.end_speed
            self.cur_jump = self.max_jumps
            self.walking()

        if self.flagpoled == 0 and self.rect.y >= PPM * 10:  # Спуск по флагштоку
            self.flagpoled = 1
            hud.start_count()  # Запуск подсчета времени в hud

    def update_invincibility(self):
        """Отсчет времени до конца неуязвимости"""
        if self.invincibility:
            self.invincibility -= 1
            if not self.invincibility:
                self.killing = False

    def update_blincking(self):
        """Создание и отключение анимации мерцания"""
        if self.blinking:
            self.blinking -= 1
            if self.cur_frame // (100 / self.blinking_freq) % 2:
                self.image = self.alpha_surface

    def check_tile_collisions(self):
        """Тут нет копипаста, новые координаты присваиваются для разных сторон по-разному,
        действия при столкновении тоже разные"""
        self.update_sides()  # Обновляем коллизии, т.к. с момента прошлого вызова метода положение
        # Марио, скорее всего, поменялось.
        colided_tile = pygame.sprite.spritecollideany(self.left_side, tiles_group)
        if colided_tile:
            # т.к. проверки на столконвения происходят ограниченное кол-во раз в секунду, то между
            # ними Марио может слегка вылететь за текстуры, строка ниже возвращает его назад
            self.rect.x = colided_tile.rect.right
            self.vx = max(0, self.vx)  # При столкновении слева больше нельзя налево
            self.update_sides()  # Обновляем коллизии после изменения положения объекта

        colided_tile = pygame.sprite.spritecollideany(self.right_side, tiles_group)
        if colided_tile:
            self.rect.right = colided_tile.rect.x  # Возвращаем Марио на границу с тайлом
            self.vx = min(0, self.vx)  # При столкновении справа больше нельзя направо
            self.update_sides()  # Обновляем коллизии после изменения положения объекта

        colided_tile = pygame.sprite.spritecollideany(self.down_side, tiles_group)
        if colided_tile:
            self.rect.bottom = colided_tile.rect.y  # Возвращаем Марио на границу с тайлом
            self.vy = min(0, self.vy)  # При столкновении снизу больше нельзя вниз
            self.update_sides()  # Обновляем коллизии после изменения положения объекта
            self.cur_jump = 0  # Если Марио стоит на чем-то, то может заново прыгнуть
            self.killing_rate = 1  # Марио стоит на тайле, а не на враге. Комбо сбрасывается
        else:
            self.image = self.frames[4]  # если Марио не стоит на чем-то, ставим картинку летящего

        colided_tile = pygame.sprite.spritecollideany(self.top_side, tiles_group)
        if colided_tile:
            self.cur_jump = self.max_jumps  # Нельзя прыгтнуть выше, если вверху что-то есть.
            if self.vy < 0:  # Удар головой об блок активирует его
                colided_tile.interact(self.state)

            self.rect.y = colided_tile.rect.bottom  # Возвращаем Марио на границу с тайлом
            self.vy = max(0, self.vy)  # При столкновении сверху больше нельзя вверх
            self.update_sides()  # Обновляем коллизии после изменения положения объекта

    def check_enemies_collisions(self):
        self.update_sides()  # Обновляем коллизии, т.к. с момента прошлого вызова метода положение
        # Марио, скорее всего, поменялось.
        if self.killing:  # Если включен killing, то убиваем мгновенно и без разбора
            colided_enemies = pygame.sprite.spritecollide(self, enemies_group, False)
            [enemy.fast_die() for enemy in colided_enemies]
            return

        # Если враг задел боковую сторону...
        for side in [self.left_side, self.right_side]:
            colided_enemy = pygame.sprite.spritecollideany(side, enemies_group)
            if colided_enemy:
                # ...уменьшаемся и становимся неуязвимыми на 120 кадров...
                if self.set_state('small', self.world):
                    self.become_invincible(120)
                elif not self.invincibility:
                    self.die()  # ... или умираем
                return

        colided_enemies = pygame.sprite.spritecollide(self.down_side, enemies_group, False)
        if colided_enemies and self.vy > 0:
            # При приземлении на голову врага
            self.rect.bottom = colided_enemies[0].rect.y  # Возвращаем Марио на границу с врагом
            self.vy = min(0, self.vy)  # Не падаем
            self.update_sides()  # Обновляем коллизии после изменения положения объекта
            self.cur_jump = 0  # Если Марио стоит на чем-то, то может заново прыгнуть
            self.jump()  # Отпрыгиваем от врага

            # Считаем комбо и убиваем врагов
            self.killing_rate = max(self.killing_rate, len(colided_enemies) ** 2)
            [enemy.die(self.killing_rate) for enemy in colided_enemies]
            self.killing_rate += 1

    def check_flagpole_collision(self):
        """Вычисление положения Марио относительно флагштока и взаимодействие с ним"""
        self.update_sides()
        if self.flagpoled > -1:
            return
        colided_flagpole = pygame.sprite.spritecollideany(self.right_side, castle_group)
        if colided_flagpole and self.rect.x + self.rect.w > colided_flagpole.rect.x + PPM // 4:
            if isinstance(colided_flagpole, FlagPole):
                colided_flagpole.start()
                self.flagpoled = 0
                self.vx = 0
                points = 5000 if self.rect.y < 2 * PPM else 400
                points_coords = (self.rect.x + 2 * PPM, self.rect.y + 1.5 * PPM)
                PointsUp(*points_coords, points)
                hud.add_score(points)
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
        """Обработка клавиш и ивентов"""
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
            # Игнорируем нажатые клавиши после смерти или пересечения флажка
            return

        self.max_vx = 10 if pygame.key.get_pressed()[pygame.K_LSHIFT] else 5

        if self.cur_jump and not any_key_pressed:
            if pygame.key.get_pressed()[pygame.K_UP]:
                self.jump()
                any_key_pressed = True
            else:
                self.cur_jump = self.max_jumps  # Предотвращение "двойного прыжка"

        for key, func in [(pygame.K_RIGHT, self.right), (pygame.K_LEFT, self.left)]:
            if pygame.key.get_pressed()[key]:
                func()
                any_key_pressed = True

        if not any_key_pressed:
            if abs(self.a) <= abs(self.vx):  # Инерция и торможение
                self.vx -= 1 if self.vx > 0 else -1 * self.a
                self.walking()
            else:
                self.vx = 0
                self.image = self.frames[6]  # idle анимация

    def create_top_side(self):
        """Верхняя коллизия не должна быть слишком широкой, иначе сложно активировать нужный тайл"""
        self.top_side = pygame.sprite.Sprite(self.sides_group)
        self.top_side.image = pygame.Surface((self.rect.w // 2, 1))
        self.top_side.image.fill((0, 255, 0))

    def update_top_side(self):
        """Верхняя коллизия не должна быть слишком широкой, иначе сложно активировать нужный тайл"""
        self.top_side.rect = pygame.Rect(self.rect.x + self.rect.w // 4, self.rect.y,
                                         self.rect.w // 2, 1)

    def set_state(self, new_state, new_type=None):
        """Смена состояний и обновление изображений Марио, включение мерциния"""
        if not new_type:
            new_type = self.type
        if self.state != new_state or self.type != new_type:
            self.type, self.state = new_type, new_state
            Map.player_state = self.state
            Map.player_type = self.type
            self.update_frames()
            if not self.blinking:
                self.blinking = 120
                self.blinking_freq = 30
            return True

    def die(self):
        self.vx = 0
        self.set_state('small', self.world)
        self.died = True
        self.cur_jump = 0
        self.jump()
        hud.add_lives(-1)

    def become_invincible(self, time, killing=False):
        """Включение неуязвимости"""
        self.killing = killing
        self.invincibility = time
        if killing:
            self.blinking = time
            self.blinking_freq = 10

    def get_flagpoled(self):
        return self.flagpoled == 1
