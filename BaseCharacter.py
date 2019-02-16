import pygame
from Utilities import GRAVITY, WIDTH, PPM, tiles_group, enemies_group


class BaseCharacter(pygame.sprite.Sprite):
    """Базовый класс для одушевленных объектов. Отвечает за гравитацию и ограничение вертикальной
    скорости; подготавливает, обновляет и проверяет коллизии"""

    def __init__(self, x, y, *groups):
        """init следует вызывать только после присваивания self.image в дочернем классе.
        Метод занимается созданием rect для self.image и хранит переменные-настройки класса"""
        super().__init__(*groups)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move((x - 1) * PPM, y * PPM)  # Перевод из блоков в пиксели
        self.max_vy = 10  # Максимальная вертикальная скорость
        self.vy = 0  # Вертикальная скорость
        self.create_sides()  # Создание коллизий
        self.gravity = GRAVITY  # Ускорение свободного падения
        self.on_screen = False  # Объект начинает двигаться, только после появления на экране

    def update_coords(self):
        if self.on_screen:  # Координаты изменяются, только если объект хоть раз появился на экране
            self.vy += self.gravity
            self.vy = max(min(self.vy, self.max_vy), -self.max_vy)  # Ограничение макс. скорости
            self.rect = self.rect.move(self.vx, self.vy)
        elif 0 <= self.rect.x <= WIDTH:  # если камера перемещает координату x на экран, то начинаем
            #  двигаться. На y проверка не нужна, т.к. если объект выпадет, то будет удален камерой,
            #  а если будет слишком высоко, то либо рано или поздно вернется, или будет удален
            self.on_screen = True  # камерой при выходе за левую границу

    def check_tile_collisions(self):
        """Метод проверяет столкновение NPC с тайлами"""
        self.check_any_collisions(tiles_group)

    def check_enemies_collisions(self):
        """Метод проверяет столкновение NPC с врагами"""
        self.check_any_collisions(enemies_group)

    def check_any_collisions(self, group):
        """Метод, отвечающий за взаимодействие левой, правой и нижней коллизий NPC с группами
        спрайтов. Многим наследникам не нужна верхняя коллизия. Объекты, которым она все же нужна,
        могут переопределить или расширить этот метод"""
        self.update_sides()  # Обновляем коллизии, т.к. с момента прошлого вызова метода положение
        # объекта, скорее всего, поменялось.
        colided_tile = pygame.sprite.spritecollideany(self.left_side, group)
        if colided_tile:
            # т.к. проверки на столконвения происходят ограниченное кол-во раз в секунду, то между
            # ними объект может слегка вылететь за текстуры, строка ниже возвращает его назад
            self.rect.x = colided_tile.rect.right
            self.vx = -self.vx  # Этот метод используется для NPC, которые всегда движутся
            # с постоянной скоростью, достаточно поменять только направление движения
            self.update_sides()  # Обновляем коллизии после изменения положения объекта

        colided_tile = pygame.sprite.spritecollideany(self.right_side, group)
        if colided_tile:
            # Это не копипаст, новые координаты присваиваются для разных сторон по-разному
            self.rect.right = colided_tile.rect.x
            self.vx = -self.vx
            self.update_sides()

        colided_tile = pygame.sprite.spritecollideany(self.down_side, group)
        if colided_tile:
            self.rect.bottom = colided_tile.rect.y
            self.vy = min(0, self.vy)  # Если NPC приземлился, то больше не может двигаться вниз
            self.update_sides()

    def create_top_side(self):
        # Наследники класса, которым не нужна верхняя коллизия, дожны заменить этот метод на pass
        self.top_side = pygame.sprite.Sprite(self.sides_group)
        self.top_side.image = pygame.Surface((self.rect.w, 1))
        self.top_side.image.fill((0, 255, 0))

    def update_top_side(self):
        # Наследники класса, которым не нужна верхняя коллизия, дожны заменить этот метод на pass
        self.top_side.rect = pygame.Rect(self.rect.x, self.rect.y - 1,
                                         self.rect.w, 1)

    def create_sides(self):
        self.sides_group = pygame.sprite.Group()  # Группа нужна для удобства отрисовки

        self.create_top_side()
        self.down_side = pygame.sprite.Sprite(self.sides_group)
        self.left_side = pygame.sprite.Sprite(self.sides_group)
        self.right_side = pygame.sprite.Sprite(self.sides_group)
        self.update_sides()

        # Визуализация коллизий для дебага
        self.down_side.image = pygame.Surface((self.rect.w - self.rect.w // 3, 1))
        self.down_side.image.fill((0, 255, 0))
        self.left_side.image = pygame.Surface((1, self.rect.h - self.max_vy * 2))
        self.left_side.image.fill((0, 255, 0))
        self.right_side.image = pygame.Surface((1, self.rect.h - self.max_vy * 2))
        self.right_side.image.fill((0, 255, 0))

    def update_sides(self):
        """Левая и правая коллизия должны отступать от верхней и нижней на максимальное расстояние,
        которое может пролететь объект за один кадр, иначе возможны ложные срабатывания,
        вызванные вылетом краёв коллизий за текстуры.  С верхней и нижней такое невозможно, т.к.
        к моменту их проверки уже произведена проверка правой и левой, во время которой объекту
        присвоены корректные координаты по x. (Всё дело в порядке проверки коллизий)"""
        self.update_top_side()
        # Нижняя коллизия не может быть слишком широкой, иначе объект не сможет упасть
        self.down_side.rect = pygame.Rect(self.rect.x + self.rect.w // 6, self.rect.bottom,
                                          self.rect.w - self.rect.w // 3, 1)

        self.left_side.rect = pygame.Rect(self.rect.x - 1, self.rect.y + self.max_vy, 1,
                                          self.rect.h - self.max_vy * 2)
        self.right_side.rect = pygame.Rect(self.rect.right, self.rect.y + self.max_vy, 1,
                                           self.rect.h - self.max_vy * 2)
