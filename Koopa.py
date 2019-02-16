import pygame
from Utilities import cut_sheet, load_image, all_sprites, enemies_group, tiles_group, screen, \
    hud, PPM
from BaseCharacter import BaseCharacter
from PointsUp import PointsUp
import Map


class Koopa(BaseCharacter):
    """Класс Купы (враждебной черепахи). Может скрываться в панцирь, кататься по уровню, убивая
    других врагов и игрока"""

    # Загрузка всех изображений и распределение их на группы.
    # Изображение скрытой в панцирь Купы приходится грузить отдельно, т.к. оно имеет другую высоту
    IMAGES = {name: (surf1 + surf2) for name, surf1, surf2 in
              zip(['normal', 'underground', 'castle', 'underwater'],
                  cut_sheet(load_image("Koopa.png"), 4, 4),
                  cut_sheet(load_image("Koopa_hidden.png"), 2, 4))}

    L_KOOPA = {key: images[:2] + images[4:6] for
               key, images in IMAGES.items()}

    # Зеркальные изображения для другого направления движения
    R_KOOPA = {key: [pygame.transform.flip(frame, True, False) for frame in images]
               for key, images in L_KOOPA.items()}

    def __init__(self, x, y, world):
        self.world = world
        self.smert = 0  # Счетчик кадров прошедших после того, как игрок наступил на Купу

        self.REVIVAL_TIME = 60 * 6  # Время появление лапок Купы из панциря в кадрах

        self.SMERT_TIME = 60 * 8  # Время выхода Купы из панциря в кадрах
        self.cur_frame = 0  # Счетчик кадров

        self._load_frames()
        self.image = self.frames[self.cur_frame]
        super().__init__(x, y, all_sprites, enemies_group)
        self.vx = -2  # Скорость в пикселях на кард
        self.value = 400  # Количество очков за убийство

    def _load_frames(self):
        """Внутренний метод загрузки кадров"""

        # Все кадры купы для этого мира
        self.l_frames = Koopa.L_KOOPA[self.world]
        self.r_frames = Koopa.R_KOOPA[self.world]
        self.frames = self.l_frames

    def load_image(self, index):
        """Метод загрузки изображений с сохранением координат после изменения высоты изображения"""
        topleft = self.rect.topleft
        self.image = self.frames[index]
        self.rect = self.image.get_rect()
        self.rect.topleft = topleft
        self.update_sides()

    def update(self):
        self.update_coords()
        self.check_tile_collisions()

        # Выбор кадров в зависимости от направления движения
        self.frames = self.l_frames if self.vx < 0 else self.r_frames
        self.check_enemies_collisions()
        self.sides_group.draw(screen)  # Отрисовка колизий

        if self.smert:  # Анимации скрытой Купы, скрытой Купы с лапками, выхода Купы из панциря
            if not self.vx:
                self.smert += 1
                if self.smert == self.REVIVAL_TIME:
                    # скрытая Купа с лапками
                    self.image = self.frames[3]
                elif self.smert == self.SMERT_TIME:
                    self.load_image(self.cur_frame // 15 % 2)
                    # обычная шагающая Купа
                    self.smert = 0
                    self.vx = -2
        else:
            self.cur_frame = (self.cur_frame + 1) % 60  # Обновление счетчика кадров
            self.image = self.frames[self.cur_frame // 15 % 2]  # Каждый 15 кадр обновляем картинку,
            # тем самым создается анимация шагов

    def die(self, rate):
        """rate - множитель очков, выдающихся при убийстве Купы. Позволяет делать комбо"""
        if not self.smert:
            # Спрятаться в панцирь и остановиться
            self.load_image(2)
            self.smert = 1
            self.vx = 0
        else:
            if not self.vx:
                # Выбор направления движения катающейся в панцире Купы
                right = (self.rect.x + self.rect.w // 2) > (
                        Map.player.rect.x + Map.player.rect.w // 2)
                self.vx = 10 if right else (-10)
            else:
                # Окончательное убийство Купы
                PointsUp(*self.rect.topleft, self.value * rate)
                hud.add_score(self.value * rate)
                self.kill()

    def fast_die(self):
        """Метод нужен для убийства черепахой, огненным шаром, движущимся блоком."""
        PointsUp(*self.rect.topleft, self.value // 2)
        hud.add_score(self.value // 2)
        self.kill()

    def check_enemies_collisions(self):
        if self.smert and self.vx:
            # Убийство врагов ездящей Купой
            [enemy.die(2) if enemy is not self else None for enemy in
             pygame.sprite.spritecollide(self, enemies_group, False)]
        else:
            # В обычном состоянии Купа меняет направление при столкновении с врагом
            super().check_enemies_collisions()


class JumpingKoopa(Koopa):
    """Класс Прыгающей Купы (враждебной черепахи). После того, как игрок наступает, превращается в
    обычную Купу. Может прыгать, имеет пониженную гравитацию из-за крыльев"""
    L_FLYING_KOOPA = {key: images[2:6] for key, images in Koopa.IMAGES.items()}

    # Зеркальные изображения для другого направления движения
    R_FLYING_KOOPA = {key: [pygame.transform.flip(frame, True, False) for frame in images]
                      for key, images in L_FLYING_KOOPA.items()}

    def __init__(self, x, y, world):
        super().__init__(x, y, world)
        # Количество кадров, когда у Купы будет максимальная отрицательная вертикальная скорость
        self.max_jumps = 25  # определяет максимальную высоту прыжка.
        self.cur_jump = 0  # Переменная-счетчик этих кадров. Определяет кол-во совершенных прыжков

        self.gravity = 0.7  # Ускорение свободного падения
        self.max_vy = 5  # Максимальная вертикальная скорость в пикселях на кадр

    def _load_frames(self):
        """Внутренний метод загрузки кадров"""

        # Все кадры купы для этого мира
        self.l_frames = JumpingKoopa.L_FLYING_KOOPA[self.world]
        self.r_frames = JumpingKoopa.R_FLYING_KOOPA[self.world]
        self.frames = self.l_frames

    def update(self):
        super().update()
        if pygame.sprite.spritecollideany(self.down_side, tiles_group):
            self.cur_jump = 0  # Обнуляем кол-во совершенных прыжков, если Купа касается земли
        if self.cur_jump < self.max_jumps:
            # Блок кода, совершающий прыжки
            self.cur_jump += 1
            self.vy = -self.max_vy

    def die(self, rate):
        """При убийстве прыгающей Купы создается обычная в панцире"""
        Koopa(self.rect.x / PPM + 1, self.rect.y / PPM, self.world).die(rate)
        self.kill()

    def check_tile_collisions(self):
        """Расширяем родительский метод check_tile_collisions. Купа может прыгать, поэтому ей
        нужна верхняя коллизия"""
        super().check_tile_collisions()
        colided_tile = pygame.sprite.spritecollideany(self.top_side, tiles_group)
        if colided_tile:  # Если Купа сталкивается с блоком вверху
            self.cur_jump = self.max_jumps  # то не может больше прыгать
            self.rect.y = colided_tile.rect.bottom  # Вытаскиваем из-за текстур
            self.vy = max(0, self.vy)  # Может лететь только вниз
            self.update_sides()
