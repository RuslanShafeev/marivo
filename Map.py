from Tile import Tile
from Player import Player
from Goomba import Goomba
from Tube import Tube


world = 'normal'

player = Player(150, 100, world)

for i in range(50, 1188, 48):
    Tile(i, 600, 'Floor')

for i in range(300, 450, 48):
    Tile(i, 400, 'BrickPlain')

for i in range(360, 602, 48):
    Tile(2, i, 'BrickPlain')

Tile(550, 552, 'Floor')
Tile(900, 552, 'Floor')

Tube(1000, 600, 3)

Goomba(750, 300, world)
Goomba(690, 300, world)