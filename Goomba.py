import pygame
from Utilities import cut_sheet, load_image, all_sprites, enemies_group, screen, hud
from PointsUp import PointsUp
from BaseCharacter import BaseCharacter


class Goomba(BaseCharacter):
    """Класс Гумбы (враждебный ходячий гриб)"""

    # Здесь происходит загрузка изображений Гумбы для разных миров
    IMAGES = {name: surf for name, surf in
              zip(['normal', 'underground', 'castle', 'underwater'],
                  cut_sheet(load_image("Goomba.png"), 3, 4))}

    def __init__(self, x, y, world):
        self.SMERT_TIME = 5  # Общее время отображения картинки расплющенного Гумбы в кадрах
        self.smert = 0  # Счетчик, показывающий сколько прошло кадров с момента смерти
        # Когда self.smert станет равен self.SMERT_TIME, Гумба будет удален

        self.cur_frame = 0  # Счетчик кадров

        self.frames = Goomba.IMAGES[world]  # Все изображения Гумбы для этого мира
        # 0 и 1 картинка - шаги, 2 - смерть
        self.image = self.frames[self.cur_frame]

        super().__init__(x, y, all_sprites, enemies_group)
        self.vx = -1  # Скорость в пикселях на кадр

    def update(self):
        # Блок кода, отвечающий за задержку для показа соотвествующей картинки перед смертью
        if self.smert:
            self.smert += 1
            if self.smert == self.SMERT_TIME:
                self.kill()
            return

        self.cur_frame = (self.cur_frame + 1) % 60  # Обновление счетчика кадров
        self.image = self.frames[self.cur_frame // 15 % 2]  # Каждые 15 кадров меняем картинку,
        # тем самым создается анимация шагов

        self.update_coords()

        self.check_tile_collisions()
        self.check_enemies_collisions()
        self.sides_group.draw(screen)  # Отрисовка коллизий

    def die(self, rate):
        """rate - множитель очков, выдающихся при убийстве Гумбы. Позволяет делать комбо"""
        self.image = self.frames[2]

        self.smert = max(1, self.smert)  # Запуск счетчика смерти. max нужен,
        # чтобы счетчик не сбрасывался при возможных повторных вызовах метода
        PointsUp(*self.rect.topleft, 200 * rate)  # Создаем высвечивающиеся очки
        hud.add_score(200 * rate)  # Добавляем счет в худ

    def fast_die(self):
        """Метод нужен для убийства черепахой, огненным шаром, движущимся блоком.
        Здесь не особо полезен, просто предоставляет такой же интерфейс, как у Купы"""
        self.die(0.5)
