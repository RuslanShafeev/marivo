import pygame
from Utilities import *
import Map
import Level1, Level2

time = pygame.time.Clock()
cur_frame = 0
level = Level1
map, player, all_sprites, groups = level.init()

while True:
    player.process_events(pygame.event.get())
    screen.fill((92, 148, 252))

    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)

    for group in groups:
        group.update()
        group.draw(screen)

    hud.update()
    hud.draw(screen)

    if player.rect.y > HEIGHT and hud.get_lives():
        map, player, all_sprites, groups = level.init()
        hud.reset()

    pygame.display.flip()
    time.tick(FPS)
