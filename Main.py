import pygame
from Utilities import *
from Map import *
from Hud import Hud


TEXT_SIZE = 40
hud_texts = ["SCORE", 0, "TIME", 400, "WORLD", "1-1", "COINS", 0, "LIVES", 3]
huds = [None] * 5
dx = SIZE[0] // 6
for i in range(5):
    huds[i] = Hud(dx * (i + 1), 20, hud_texts[2 * i], hud_texts[2 * i + 1], TEXT_SIZE)
time = pygame.time.Clock()

while True:
    player.process_events(pygame.event.get())
    screen.fill((92, 148, 252))

    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)

    players_group.update()
    all_sprites.update()

    all_sprites.draw(screen)
    for hud in huds:
        hud.draw(screen)
    players_group.draw(screen)
    pygame.display.flip()
    time.tick(60)
