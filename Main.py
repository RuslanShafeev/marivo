import pygame
from Utilities import *
import Utilities
import Map

time = pygame.time.Clock()

while True:
    hud.update()
    hud.draw(screen)

    if hud.get_load_level_request():
        Map.load_level(Map.lvl1, utils=Utilities, resetscore=True)
        hud.set_lives(3)
    elif hud.get_game_over():
        time.tick(FPS)
        pygame.display.flip()
        continue

    if Map.player.flagpoled and not hud.get_time():
        Map.load_level(Map.lvl2, utils=Utilities)

    Map.player.process_events(pygame.event.get())
    screen.fill((92, 148, 252))

    camera.update(Map.player)
    for sprite in all_sprites:
        camera.apply(sprite)

    players_group.update()
    all_sprites.update()


    decor_group.draw(screen)
    items_group.draw(screen)
    enemies_group.draw(screen)
    castle_group.draw(screen)
    tiles_group.draw(screen)
    players_group.draw(screen)
    particles_group.draw(screen)
    hud.draw(screen)

    time.tick(FPS)
    pygame.display.flip()
