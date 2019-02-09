import pygame


class PointsUp:
    FONT = "data/SuperMario256.ttf"
    SIZE = 20
    TIMER_LIM = 20

    def __init__(self, x, y, points, array):
        self.x, self.y = x, y
        self.points = str(points)
        self.array = array
        self.font = pygame.font.Font(PointsUp.FONT, PointsUp.SIZE)
        self.points_render = self.font.render(self.points, 1, pygame.Color('white'))
        self.points_rect = self.points_render.get_rect()
        self.points_rect.left = x
        self.points_rect.top = y - PointsUp.SIZE
        self.timer = 0

    def draw(self, screen):
        self.timer += 1
        if self.timer == PointsUp.TIMER_LIM:
            del self.array[self.array.index(self)]
        self.points_rect.top -= 1
        screen.blit(self.points_render, self.points_rect)