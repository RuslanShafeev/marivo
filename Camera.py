from Utilities import *

class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        if obj.rect.right < 0:
            obj.kill()

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = min(0, -(target.rect.x + target.rect.w // 2 - WIDTH // 2))
        target.rect.x += self.dx
        if target.rect.x <= 0:
            target.rect.x = 0
            target.vx = max(0, target.vx)