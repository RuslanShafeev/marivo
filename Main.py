import pygame
from Utilities import hud, screen, FPS, camera, all_sprites, players_group, groups
import Utilities
import Map


def main():
    time = pygame.time.Clock()

    levels = ['level1', 'level2']  # Названия уровней
    current_level = 0  # Индекс текущего уровня
    Map.load_level(levels[current_level], Utilities)  # Создание спрайтов уровня

    while True:
        # Обновление интерфейса
        hud.update()

        if hud.get_load_level_request():
            # Если hud сообщает, что закончилось время или жизни, то загружаем первый уровень
            Map.load_level(levels[0], Utilities, resetscore=True)
            hud.set_lives(3)  # Возвращаем жизни. Время откатится автоматически
        elif hud.get_game_over():
            # Если hud сообщает, что выводит заставку game over, то  не делаем ничего,
            # кроме смены кадров
            time.tick(FPS)
            pygame.display.flip()
            continue

        # Условие, сигнализирующее об окончании уровня и подсчета очков
        if Map.player.get_flagpoled() and not hud.get_time():
            # Загружаем следующий или первый уровень
            current_level = (current_level + 1) % len(levels)
            Map.load_level(levels[current_level], Utilities)

        Map.player.process_events(pygame.event.get())  # Разбором событий занимается player
        screen.fill((92, 148, 252))

        # изменяем ракурс камеры
        camera.update(Map.player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)

        players_group.update()
        all_sprites.update()

        [group.draw(screen) for group in groups]  # отрисовка групп в нужном порядке
        hud.draw(screen)  # hud рисуется всегда поверх

        time.tick(FPS)
        pygame.display.flip()


if __name__ == '__main__':
    main()
