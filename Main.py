import pygame
from Utilities import *
from Map import *

time = pygame.time.Clock()

while True:
    player.process_events(pygame.event.get())
    screen.fill((92, 148, 252))
    all_sprites.update()
    all_sprites.draw(screen)
    pygame.display.flip()
    time.tick(60)
