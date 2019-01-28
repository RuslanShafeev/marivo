from Tile import Tile
from Player import Player

player = Player(150, 100)

for i in range(50, 900, 48):
    Tile(i, 600, 'Floor')


for i in range(300, 450, 48):
    Tile(i, 350, 'BrickPlain')

for i in range(360, 602, 48):
    Tile(2, i, 'BrickPlain')

Tile(550, 552, 'Floor')
