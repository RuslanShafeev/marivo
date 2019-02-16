import pygame
from Utilities import *
from Items import *
import random


class Particle(pygame.sprite.Sprite):
    """Частицы, создающиеся при разрушении блоков. Имеют случайный угол повората."""

    def __init__(self, pos, dx, dy, image):
        """Частица создается на основе переданного изображения."""
        super().__init__(all_sprites, particles_group)
        self.image = pygame.transform.rotate(
            pygame.transform.scale(image, (image.get_width() // 2, image.get_height() // 2)),
            random.randint(30, 60))

        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]  # Скорости в пикелях на кадр
        self.rect.x, self.rect.y = pos
        self.gravity = GRAVITY  # Ускорений свободного падения

    def update(self):
        self.velocity[1] += self.gravity  # Свободное падение
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if self.rect.y > HEIGHT:  # Уничтожаются при падении вниз за границу экрана
            self.kill()


class TilesBase(pygame.sprite.Sprite):
    """Базовый класс для всех блоков. Предоставляет метод создания частиц, убийства врагов"""
    ITEMS = {'MushroomSizeUp': MushroomSizeUp, 'MushroomLiveUp': MushroomLiveUp,
             'MushroomDeadly': MushroomDeadly, 'FireFlower': FireFlower, 'Star': Star, 'Coin': Coin}

    # Загрузка всех изображений и распределение их на группы
    IMAGES = {name: surf for name, surf in
              zip(['normal', 'underground', 'castle', 'underwater'],
                  cut_sheet(load_image("Tile.png"), 11, 4))}

    def __init__(self, x, y):
        super().__init__(all_sprites, tiles_group)
        self.rect = self.image.get_rect()
        self.rect = self.rect.move((x - 1) * PPM, y * PPM)  # Перевод координат из блоков в пиксели

    def interact(self, mario_state):
        pass

    def create_particles(self):
        """Создание 4 частиц при разрушении блока"""
        Particle(self.rect.topleft, -5, 0, self.image)
        Particle(self.rect.midtop, 5, 0, self.image)
        Particle(self.rect.midleft, -5, 5, self.image)
        Particle(self.rect.center, 5, 5, self.image)

    def kill_enemies(self):
        """Убиство врагов стоящих на активированном блоке"""
        [enemy.fast_die() for enemy in
         pygame.sprite.spritecollide(self, enemies_group, False, self.check_enemy_collide)]

    def check_enemy_collide(self, tile, enemy):
        """Проверка столконвения блока с нижней стороной врага"""
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
        """BrickPlain сразу же разрушается при взаимодействии"""
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
    """Блок-контейнер. Может хранить несколько item'ов. После создания бонусов
     превращается в Stone"""

    def __init__(self, x, y, world, item=None):
        self.world = world
        self.image = TilesBase.IMAGES[world][1]
        self.stone_image = TilesBase.IMAGES[world][9]
        super().__init__(x, y)

        # Хранит рандомное количество монет или 1 любой другой item
        self.items = ([item] if item else []) * (random.randint(5, 10) if item == 'Coin' else 1)
        self.moving = False
        self.start_y = self.rect.y  # Начальная точка движения блока при взаимодейтсвии
        self.end_y = self.start_y - 14  # Конечная точка движения блока при взаимодейтсвии

    def interact(self, mario_state):
        """Взаимодействие происходит по-разному для большого и маленького Марио. Для маленького
        вместо цветка создается увеличивающий гриб"""
        if self.rect.y == self.start_y and self.image is not self.stone_image:
            self.kill_enemies()
            if self.items:  # Создание item'ов
                item_obj = TilesBase.ITEMS[self.items.pop()]
                if item_obj is FireFlower and mario_state == 'small':
                    item_obj = MushroomSizeUp
                item_obj(self.rect.x / PPM + 1, self.end_y / PPM, self.world)
                if not self.items:
                    self.image = self.stone_image
                self.moving = True
            elif mario_state == 'small':
                self.moving = True
            else:
                self.create_particles()  # Если блок пустой, то может быть уничтожен большим Марио
                self.kill()

    def update(self):
        self.move()

    def move(self):
        """Анимация движения вверх-вниз"""
        if self.moving:
            if self.rect.y > self.end_y:
                self.rect.y -= 3
            else:
                self.moving = False
        elif self.rect.y < self.start_y:
            self.rect.y += 3


class InvincibleTile(TilesBase):
    """Секретный невидимый блок. Появляется при взамодействии"""

    def __init__(self, x, y, world, item):
        self.x, self.y = x, y
        self.world = world
        self.item = item
        self.used = False  # Видим ли блок
        self.image = TilesBase.IMAGES[world][10]
        super().__init__(x, y)

    def interact(self, mario_state):
        if self.used:
            return
        item_obj = TilesBase.ITEMS[self.item]
        if item_obj is FireFlower and mario_state == 'small':
            # Для маленького Марио вместо цветка создается увеличивающий гриб
            item_obj = MushroomSizeUp
        item_obj(self.rect.x / PPM + 1, (self.rect.y - 14) / PPM, self.world)
        self.image = TilesBase.IMAGES[self.world][9]
        self.used = True


class Quest(TilesBase):
    """Блок со знаком вопроса. Хранит максимум 1 item. После создания бонуса превращается в Stone"""

    def __init__(self, x, y, world, item):
        self.world = world
        self.frames = TilesBase.IMAGES[world][6:10]
        self.cur_frame = 0  # Счетчик кадров
        self.image = self.frames[self.cur_frame]
        super().__init__(x, y)

        self.item = item
        self.moving = False
        self.start_y = self.rect.y  # Начальная точка движения блока при взаимодейтсвии
        self.end_y = self.start_y - self.rect.h // 3  # Конечная точка движения блока

    def update(self):
        if self.image is not self.frames[3]:
            self.cur_frame = (self.cur_frame + 1) % 60  # Обновление счетчика кадров

            # Изменение картинки каждые 10 кадров. Тем самым создается анимация мерцания
            self.image = self.frames[self.cur_frame // 10 % 3]
            self.move()

    def interact(self, mario_state):
        self.kill_enemies()
        if self.item:  # Создание item'ов
            item_obj = TilesBase.ITEMS[self.item]
            if item_obj is FireFlower and mario_state == 'small':
                # Для маленького Марио вместо цветка создается увеличивающий гриб
                item_obj = MushroomSizeUp
            item_obj(self.rect.x / PPM + 1, self.end_y / PPM, self.world)
            self.item = None
            self.moving = True

    def move(self):
        """Анимация движения вверх-вниз"""
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
