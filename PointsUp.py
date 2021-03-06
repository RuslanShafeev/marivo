import pygame
from Utilities import *


class PointsUp(pygame.sprite.Sprite):
    """Класс вылетающих на экране очков"""
    SIZE = 20
    pygame.font.init()
    FONT = load_font("SuperMario256.ttf", SIZE)
    TIMER_LIM = 20  # Время существования в кадрах

    def __init__(self, x, y, points):
        super().__init__(all_sprites, particles_group)
        self.image = PointsUp.FONT.render(str(int(points)), 1, pygame.Color('white'))
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x, y)
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer == PointsUp.TIMER_LIM:
            self.kill()
        self.rect.y -= 1
