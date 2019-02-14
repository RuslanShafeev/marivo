import pygame
from Utilities import *
import Utilities
import Map

time = pygame.time.Clock()

levels = ['level1', 'level2']
current_level = 0
Map.load_level(levels[current_level], Utilities)


while True:
    hud.update()
    hud.draw(screen)

    if hud.get_load_level_request():
        Map.load_level(levels[0], Utilities, resetscore=True)
        hud.set_lives(3)
    elif hud.get_game_over():
        time.tick(FPS)
        pygame.display.flip()
        continue

    if Map.player.get_flagpoled() and not hud.get_time():
        current_level = (current_level + 1) % len(levels)
        Map.load_level(levels[current_level], Utilities)

    Map.player.process_events(pygame.event.get())
    screen.fill((92, 148, 252))

    camera.update(Map.player)
    for sprite in all_sprites:
        camera.apply(sprite)

    players_group.update()
    all_sprites.update()

    [group.draw(screen) for group in groups]
    hud.draw(screen)

    time.tick(FPS)
    pygame.display.flip()
