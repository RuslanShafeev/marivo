import pygame
from Utilities import *
import Utilities
import Map

time = pygame.time.Clock()

while True:
    hud.update()
    hud.draw(screen)

    if hud.get_load_level_request():
        Map.load_level(Map.lvl1, Utilities, resetscore=True)
        hud.set_lives(3)
    elif hud.get_game_over():
        time.tick(FPS)
        pygame.display.flip()
        continue

    if Map.player.get_flagpoled() and not hud.get_time():
        if Map.cur == Map.lvl1:
            Map.load_level(Map.lvl2, Utilities)
        else:
            hud.start_game_over()
            hud.game_over_draw(screen)

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
