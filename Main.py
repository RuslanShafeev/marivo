import pygame
from Utilities import *
from Map import *

time = pygame.time.Clock()

while True:
    player.process_events(pygame.event.get())
    screen.fill((92, 148, 252))

    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)

    players_group.update()
    all_sprites.update()

    items_group.draw(screen)
    enemies_group.draw(screen)
    tiles_group.draw(screen)
    players_group.draw(screen)
    particles_group.draw(screen)

    pygame.display.flip()
    time.tick(60)
