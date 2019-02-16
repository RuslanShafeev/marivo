import pygame
from Utilities import cut_sheet, load_image, all_sprites, items_group, players_group, \
    enemies_group, tiles_group, hud, screen, PPM
from BaseCharacter import BaseCharacter
from PointsUp import PointsUp


class ItemBase(BaseCharacter):
    """Базовый класс для различных бонусов. Бонусы никак не взаимодействуют с врагами."""

    # Загрузка всех изображений и распределение их на группы
    ITEMS = {name: surf for name, surf in
             zip(['normal', 'underground', 'castle', 'underwater'],
                 cut_sheet(load_image("Items.png"), 19, 4))}

    def __init__(self, x, y):
        super().__init__(x, y, all_sprites, items_group)
        self.vx = 5  # Скорость в пикселях на кадр

        # Высота, до котор. нужно поднятся бонусу при появлении из блока, прежде чем начать движение
        self.uprise = self.rect.y - self.rect.h + self.rect.h // 3
        self.create_sides()

    def move(self):
        """Метод, отвечающий анимацию появления бонуса из блока"""
        if self.uprise is not None and self.rect.y > self.uprise:
            self.rect.y -= 1
            if self.rect.y == self.uprise:
                self.uprise = None
            return True

    def update(self):
        # Если бонус еще не до конца появился, то не обновляем координаты в зависимости от скорости
        if self.move():
            return
        self.update_coords()
        self.check_player_collisions()

        vx = self.vx  # Старое направление
        self.check_tile_collisions()
        if vx != self.vx:  # При изменении направления отражаем картинку
            self.image = pygame.transform.flip(self.image, True, False)

        self.sides_group.draw(screen)  # Отрисовка коллизий


class MushroomSizeUp(ItemBase):
    """Класс гриба, превращающего обычного Марио в Супер Марио"""

    def __init__(self, x, y, world):
        self.image = ItemBase.ITEMS[world][0]
        super().__init__(x, y)

    def check_player_collisions(self):
        """Метод проверяет, подобрал ли игрок бонус, превращает игрока в Супер Марио,
        дает 1000 очков"""
        collided = pygame.sprite.spritecollideany(self, players_group)
        if collided:
            collided.set_state('big')
            PointsUp(*collided.rect.topleft, 1000)
            hud.add_score(1000)
            self.kill()

    def create_top_side(self):
        """Верхняя коллизия не нужна, т.к. гриб не умеет прыгать и не убивается прыжком сверху"""
        pass

    def update_top_side(self):
        """Верхняя коллизия не нужна, т.к. гриб не умеет прыгать и не убивается прыжком сверху"""
        pass


class MushroomLiveUp(ItemBase):
    """Класс гриба, дающего бонусную жизнь"""

    def __init__(self, x, y, world):
        self.image = ItemBase.ITEMS[world][1]
        super().__init__(x, y)

    def check_player_collisions(self):
        """Метод проверяет, подобрал ли игрок бонус, дает 1 жизнь"""
        collided = pygame.sprite.spritecollideany(self, players_group)
        if collided:
            hud.add_lives(1)
            self.kill()

    def create_top_side(self):
        """Верхняя коллизия не нужна, т.к. гриб не умеет прыгать и не убивается прыжком сверху"""
        pass

    def update_top_side(self):
        """Верхняя коллизия не нужна, т.к. гриб не умеет прыгать и не убивается прыжком сверху"""
        pass


class MushroomDeadly(ItemBase):
    """Класс гриба, убивающего Марио"""

    def __init__(self, x, y, world):
        self.image = ItemBase.ITEMS[world][2]
        super().__init__(x, y)

    def check_player_collisions(self):
        """Метод проверяет, подобрал ли игрок бонус, убивает Марио"""
        collided = pygame.sprite.spritecollideany(self, players_group)
        if collided:
            collided.die()
            self.kill()

    def create_top_side(self):
        """Верхняя коллизия не нужна, т.к. гриб не умеет прыгать и не убивается прыжком сверху"""
        pass

    def update_top_side(self):
        """Верхняя коллизия не нужна, т.к. гриб не умеет прыгать и не убивается прыжком сверху"""
        pass


class FireFlower(ItemBase):
    """Класс цветка, превращающего Марио в Огненного Марио"""

    def __init__(self, x, y, world):
        self.cur_frame = 0  # Счетчик кадров
        self.frames = ItemBase.ITEMS[world][3:7]  # Все кадры мерцающего цветка для этого мира
        self.image = self.frames[self.cur_frame]
        super().__init__(x, y)
        self.vx = 0

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % 60  # Обновляем счетчик кадров
        self.image = self.frames[self.cur_frame // 5 % 4]  # Каждые 5 кадров меняем картинку
        # тем самым создаем мерцание
        super().update()

    def check_player_collisions(self):
        """Метод проверяет, подобрал ли игрок бонус, превращает Марио в Огненного,
        дает 1000 очков"""
        collided = pygame.sprite.spritecollideany(self, players_group)
        if collided:
            collided.set_state('big', 'fire')
            PointsUp(*collided.rect.topleft, 1000)
            hud.add_score(1000)
            self.kill()

    def check_tile_collisions(self):
        """Переопределяем родительский check_tile_collisions, т.к. цветочку нужна только
        нижняя коллизия (на цветок действует гравитация)"""
        self.update_sides()
        colided_tile = pygame.sprite.spritecollideany(self.down_side, tiles_group)
        if colided_tile:
            self.rect.bottom = colided_tile.rect.y
            self.vy = min(0, self.vy)
            self.update_sides()

    def create_sides(self):
        """Переопределяем родительский create_sides, т.к. цветочку нужна только
        нижняя коллизия (на цветок действует гравитация)"""
        self.sides_group = pygame.sprite.Group()
        self.down_side = pygame.sprite.Sprite(self.sides_group)
        self.update_sides()

        self.down_side.image = pygame.Surface((self.rect.w, 1))
        self.down_side.image.fill((0, 255, 0))

    def update_sides(self):
        """Переопределяем родительский update_sides, т.к. цветочку нужна только
        нижняя коллизия (на цветок действует гравитация)"""
        self.down_side.rect = pygame.Rect(self.rect.x, self.rect.bottom, self.rect.w, 1)


class Star(ItemBase):
    """Класс звездочки, дающей игроку бессмертие"""

    def __init__(self, x, y, world):
        self.cur_frame = 0
        self.frames = ItemBase.ITEMS[world][7:11]
        self.image = self.frames[self.cur_frame]
        super().__init__(x, y)

        # Количество кадров, когда у звезды будет максимальная отрицательная вертикальная скорость
        self.max_jumps = 8  # определяет максимальную высоту прыжка.
        self.cur_jump = 0  # Переменная-счетчик этих кадров. Определяет кол-во совершенных прыжков
        self.invincibility_time = 600  # Время неуязвимости в кадрах

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % 60  # Обновление счетчика кадров
        self.image = self.frames[self.cur_frame // 5 % 4]  # Каждые 5 кадров меняем изображение,
        # тем самым создаем мерцание

        if self.cur_jump < self.max_jumps:  # Блок кода, совершающий прыжки
            self.vy = - self.max_vy
            self.cur_jump += 1
        super().update()
        if pygame.sprite.spritecollideany(self.down_side, tiles_group):
            self.cur_jump = 0  # Обнуляем кол-во совершенных прыжков, если звезда касается земли

    def check_player_collisions(self):
        """Метод проверяет, подобрал ли игрок бонус, делает Марио неуязвимым на
        определенное время"""
        collided = pygame.sprite.spritecollideany(self, players_group)
        if collided:
            collided.become_invincible(self.invincibility_time, True)
            self.kill()

    def check_tile_collisions(self):
        """Расширяем родительский метод check_tile_collisions. Звезда может прыгать, поэтому ей
        нужна верхняя коллизия"""
        super().check_tile_collisions()
        colided_tile = pygame.sprite.spritecollideany(self.top_side, tiles_group)
        if colided_tile:  # Если звезда сталкивается с блоком вверху
            self.cur_jump = self.max_jumps  # то не может больше прыгать
            self.rect.y = colided_tile.rect.bottom  # Вытаскиваем из-за текстур
            self.vy = max(0, self.vy)  # Может лететь только вниз
            self.update_sides()


class CoinStatic(pygame.sprite.Sprite):
    """Класс статичной подбираемой монетки. Не наследуется от ItemBase, т.к. нет коллизий,
    скорости, не может появляется из блока"""

    def __init__(self, x, y, world):
        self.frames = ItemBase.ITEMS[world][11:15]  # Все кадры мерцающей монетки для этого мира
        self._load_image(x, y)

    def _load_image(self, x, y):
        """Внутренний метод для загрузки изображений"""
        super().__init__(all_sprites, items_group)
        self.cur_frame = 0  # Счетчик кадров
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move((x - 1) * PPM, y * PPM)

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % 60  # Обновление счетчика кадров
        self.image = self.frames[self.cur_frame // 5 % 4]  # Каждые 5 кадров меняем картинку
        # тем самым создаем мерцание
        self.check_player_collisions()

    def check_player_collisions(self):
        """Метод проверяет, подобрал ли игрок бонус, добавляет монету в худ, дает 200 очков"""
        collided = pygame.sprite.spritecollideany(self, players_group)
        if collided:
            hud.add_score(200)
            hud.add_coins(1)
            self.kill()


class Coin(CoinStatic):
    """Класс вылетающей из блока монеты"""

    def __init__(self, x, y, world):
        self.frames = ItemBase.ITEMS[world][15:19]  # Все кадры вращающейся монетки для этого мира
        self._load_image(x, y)
        self.start_y = self.rect.y - self.rect.h  # Нижняя точка полета монеты
        self.end_y = self.start_y - self.rect.h * 2  # Верхняя точка полета монеты
        self.vx = 7  # Вертикальная скорость в пикселях на кадр

        # При появлении монета добавляет игроку
        hud.add_score(200)  # 200 очков
        hud.add_coins(1)  # +1 coin

    def update(self):
        """Полет монеты между верхней и нижней точкой, анимация вращения монеты"""
        super().update()
        if self.end_y is not None and self.rect.y > self.end_y:
            self.rect.y -= self.vx
            if self.rect.y <= self.end_y:
                self.end_y = None
        elif self.rect.y < self.start_y:
            self.rect.y += self.vx
            if self.rect.y >= self.start_y:
                self.kill()

    def check_player_collisions(self):
        """Игрок не может взаимодействовать с монетой"""
        pass


class Fire(BaseCharacter):
    """Класс фаерболов, выпусаемых Огненным Марио. Убивают врагов одним выстрелом, взрываются
    при контакте с боком блока, отскакивают от верха, не взаимодействуют с игроком"""
    IMAGES = cut_sheet(load_image("fire.png"), 4, 1)[0]  # Загрузка всех изображений фаербола

    # Первое разбивается на 4 маленьких
    FLYING = [col for row in cut_sheet(IMAGES[0], 2, 2) for col in row]
    EXPLODE = IMAGES[1:]

    def __init__(self, x, y, direction):
        """direction зависит от Направления марио"""
        self.cur_frame = 0  # Счетчик кадров
        self.image = Fire.FLYING[self.cur_frame]
        super().__init__(x, y, all_sprites, items_group)
        self.vx = 5 * direction  # Горизонтальная скорость в пикселях на кадр

        self.explosion = False  # Если True воспроизводится анимация взрыва
        self.explosion_time = 0  # Счетчик кадров анимации взрыва
        self.explosion_end = 17  # Общее время анимации взрыва в кадрах

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % 60  # Обновление счетчика кадров

        if self.explosion:  # Воспроизведение анимации взрыва
            self.image = Fire.EXPLODE[self.explosion_time // 6]
            self.explosion_time += 1
            if self.explosion_time == self.explosion_end:
                self.kill()
            return

        self.image = Fire.FLYING[self.cur_frame // 15 % 4]  # Каждые 15 кадров обновляем изборажение
        # тем самым достигается анимация вращения в полете

        self.update_coords()  # Обновляем y координату
        self.rect.x += self.vx  # Обновляем x координату
        self.check_tile_collisions()
        self.check_enemies_collisions()

        self.sides_group.draw(screen)  # Отрисовка коллизий

    def check_tile_collisions(self):
        """Изменение направления движения при столкновении с блоком либо запуск взрыва.
        Переопределяет родительский метод check_tile_collisions, т.к. фаербол имеет уникальное
        поведение"""
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
        """Быстрое убийство врага при соприкосновении"""
        collided_enemy = pygame.sprite.spritecollideany(self, enemies_group)
        if collided_enemy:
            collided_enemy.fast_die()
            self.explosion = True
