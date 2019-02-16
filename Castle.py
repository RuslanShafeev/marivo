import pygame
from Utilities import load_image, all_sprites, castle_group, PPM


class Castle(pygame.sprite.Sprite):
    """Класс замка в конце уровня"""
    image = load_image("castle_big.png")
    SMALL_HEIGHT = 4
    BIG_HEIGHT = 10

    def __init__(self, x, y, is_big):
        """y координата - нижняя сторона, т.к. замки имеют разную высоту"""
        super().__init__(all_sprites, castle_group)
        self.image = Castle.image
        self.rect = self.image.get_rect()
        x_off = 4  # Замок слегка сдвинут по x
        if is_big:  # Вычисление верхней строны в зависимости от высоты.
            y -= Castle.BIG_HEIGHT
        else:
            # Маленький замок - это большой, низ которого спрятан под землей :)
            y -= Castle.SMALL_HEIGHT
        # Перевод координат из блоков в пиксели
        self.rect.x, self.rect.y = (x - x_off - 1) * PPM, y * PPM

    def get_centre(self):
        """Возвращает координаты двери"""
        return self.rect.x + 4 * PPM
