import pygame


class Hud:
    FONT = "data/SuperMario256.ttf"

    def __init__(self, cx, y, title, value, size):
        self.x, self.y = cx, y
        self.title = str(title)
        self.value = str(value)
        self.size = size
        self.font = pygame.font.Font(Hud.FONT, size)
        self.title_render = self.font.render(self.title, 1, pygame.Color('white'))
        self.title_rect = self.title_render.get_rect()
        self.title_rect.left = cx - self.title_rect.w // 2
        self.title_rect.top = y
        self.value_render = self.font.render(self.value, 1, pygame.Color('white'))
        self.value_rect = self.value_render.get_rect()
        self.value_rect.left = self.x - self.value_rect.w // 2
        self.value_rect.top = self.y + int(self.title_rect.h)
        print(self.title_rect, self.value_rect)

    def set_value(self, value):
        self.value = str(value)
        self.value_render = self.font.render(self.value, 1, pygame.Color('white'))
        self.value_rect = self.value_render.get_rect()
        self.value_rect.left = self.x - self.value_rect.w // 2
        self.value_rect.top = self.y + int(self.title_rect.h)

    def get_value(self):
        return self.value

    def draw(self, screen):
        screen.blit(self.title_render, self.title_rect)
        screen.blit(self.value_render, self.value_rect)