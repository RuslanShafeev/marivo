import pygame
from Utilities import load_image, all_sprites, castle_group, tiles_group, PPM


class FlagPole(pygame.sprite.Sprite):
    """Класс флагштока. Проверкой коллизии занимается Player"""
    image = load_image("flagpole.png")

    def __init__(self, x, y):
        """y - нижняя часть, так удобнее, не нужно помнить высоту флагштока"""
        super().__init__(all_sprites, castle_group)
        self.image = FlagPole.image
        self.rect = self.image.get_rect()
        # Перевод координат из блоков в пиксели.
        self.rect.x, self.rect.y = (x - 1) * PPM, (y - 10) * PPM
        self.flag = Flag(x, y)  # Создаем флажок

    def start(self):
        self.flag.start()


class Flag(pygame.sprite.Sprite):
    """Класс флажка, может опускаться пока не достигнет блока"""
    image = load_image("flag.png")

    def __init__(self, x, y):
        super().__init__(all_sprites, castle_group)
        self.image = Flag.image
        self.rect = self.image.get_rect()
        # Перевод координат из блоков в пиксели. Флажок имеет смещение относительно флагштока
        self.rect.x, self.rect.y = (x - 1.5) * PPM, (y - 9) * PPM
        self.vy = 0

    def update(self):
        """Если скорость не равна 0, то метод опускает флажок, сбрасывает скорость, когда флажок
        коснется блока"""
        self.rect.y += self.vy
        if self.vy and pygame.sprite.spritecollideany(self, tiles_group):
            self.vy = 0

    def start(self):
        """Чтобы заставить флажок опуститься присваеваем ему вертикалькую скорость"""
        self.vy = 10
