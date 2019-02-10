import pygame
from Utilities import *
from Map import *


time = pygame.time.Clock()
cur_frame = 0

while True:
    player.process_events(pygame.event.get())
    screen.fill((92, 148, 252))

    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)

    players_group.update()
    all_sprites.update()
    hud.update(cur_frame)

    items_group.draw(screen)
    enemies_group.draw(screen)
    tiles_group.draw(screen)
    players_group.draw(screen)
    particles_group.draw(screen)
    hud.draw(screen)

    for scores_txt in scores:
        scores_txt.draw(screen)

    cur_frame = (cur_frame + 1) % 60

    pygame.display.flip()
    time.tick(FPS)
