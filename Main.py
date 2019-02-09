import pygame
from Utilities import *
from Map import *
from Hud import Hud

time = pygame.time.Clock()

sec = 0
while True:
    player.process_events(pygame.event.get())
    screen.fill((92, 148, 252))

    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)

    players_group.update()
    all_sprites.update()

    for hud in huds:
        hud.draw(screen)

    items_group.draw(screen)
    enemies_group.draw(screen)
    tiles_group.draw(screen)
    players_group.draw(screen)
    particles_group.draw(screen)

    for scores_txt in scores:
        scores_txt.draw(screen)

    pygame.display.flip()
    time.tick(60)
    sec += 1 / 30
    if sec >= 1:
        Map.tick()
        sec = 0