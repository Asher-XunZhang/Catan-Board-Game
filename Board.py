import pygame, sys, random
from pygame.locals import *
from math import sin, cos, pi

# set up game
pygame.init()
FPS = 30
clock = pygame.time.Clock()

# function to update game window display
def update_window():
	pygame.display.update()

# set window specifications
WIDTH, HEIGHT = 900, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catan 3000")

WATER = (0, 0, 255)
FOREST = (50, 120, 80)
PASTURE = (40, 255, 0)
FIELD = (255, 255, 0)
HILL = (255, 100, 50)
MOUNTAIN = (100, 100, 100)
DESERT = (50, 50, 0)

# set tile locations
tile_locations = [(260,240), (230, 290), (320, 240), (350, 290), (320, 340), (260, 340),
				(230, 390), (260, 445), (320, 440), (350, 390), (410, 290), (440, 240),
				(410, 190), (350, 190), (320, 135), (260, 340), (260, 140), (230, 190),
				(170, 190), (140, 240), (170, 290), (140, 340), (170, 390), (260, 550),
				(320, 550), (350, 500), (410, 500), (440, 445), (500, 445), (530, 395), 
				(500, 340), (530, 290), (500, 240), (530, 190), (500, 135), (440, 135),
				(410, 80), (350, 80), (320, 30), (260, 30), (230, 80), (170, 80), (140, 135),
				(80, 135), (50, 190), (80, 240), (50, 290), (80, 340), (50, 395), (80, 445),
				(140, 445), (170, 500), (230, 500), (410, 390), (440, 340)]


# create Board class
class Board:
	hex_tiles = []

	def __init__(self, size):
		self.tiles = []
		self.tiles += [FOREST]*4
		self.tiles += [PASTURE]*4
		self.tiles += [HILL]*3
		self.tiles += [FIELD]*4
		self.tiles += [MOUNTAIN]*4
		self.tiles += [DESERT]

		self.hexHeight = 0.8 * size

		self.cX = WIN.get_rect().centerx
		self.cY = WIN.get_rect().centery

		# center tile
		self.hex_tiles.append(Hex((self.cX, self.cY), size, self.tiles[0]))
		
		# inner ring of tiles
		self.hex_tiles.append(Hex((self.cX, self.cY - (2*self.hexHeight)), size, self.tiles[1]))
		self.hex_tiles.append(Hex((self.cX, self.cY + (2*self.hexHeight)), size, self.tiles[2]))
		self.hex_tiles.append(Hex((self.cX - (1.5*size), self.cY - self.hexHeight), size, self.tiles[3]))
		self.hex_tiles.append(Hex((self.cX + (1.5*size), self.cY - self.hexHeight), size, self.tiles[4]))
		self.hex_tiles.append(Hex((self.cX - (1.5*size), self.cY + self.hexHeight), size, self.tiles[5]))
		self.hex_tiles.append(Hex((self.cX + (1.5*size), self.cY + self.hexHeight), size, self.tiles[6]))
		
		# outer ring of tiles
		self.hex_tiles.append(Hex((self.cX - (3*size), self.cY), size, self.tiles[7]))
		self.hex_tiles.append(Hex((self.cX + (3*size), self.cY), size, self.tiles[8]))
		self.hex_tiles.append(Hex((self.cX, self.cY - (4*self.hexHeight)), size, self.tiles[9]))
		self.hex_tiles.append(Hex((self.cX, self.cY + (4*self.hexHeight)), size, self.tiles[10]))
		
		self.hex_tiles.append(Hex((self.cX + (1.5*size), self.cY + (3*self.hexHeight)), size, self.tiles[11]))
		self.hex_tiles.append(Hex((self.cX + (1.5*size), self.cY - (3*self.hexHeight)), size, self.tiles[12]))
		self.hex_tiles.append(Hex((self.cX - (1.5*size), self.cY - (3*self.hexHeight)), size, self.tiles[13]))
		self.hex_tiles.append(Hex((self.cX - (1.5*size), self.cY + (3*self.hexHeight)), size, self.tiles[14]))
		
		self.hex_tiles.append(Hex((self.cX + (3*size), self.cY+(2*self.hexHeight)), size, self.tiles[15]))
		self.hex_tiles.append(Hex((self.cX + (3*size), self.cY-(2*self.hexHeight)), size, self.tiles[16]))
		self.hex_tiles.append(Hex((self.cX - (3*size), self.cY+(2*self.hexHeight)), size, self.tiles[17]))
		self.hex_tiles.append(Hex((self.cX - (3*size), self.cY-(2*self.hexHeight)), size, self.tiles[18]))
		

	def draw(self):
		# draw the tiles
		for h in self.hex_tiles:
			h.draw()

# create hexogonal tile class
class Hex:
	def __init__(self, centre, size, color):
		self.hexX = centre[0]
		self.hexY = centre[1]
		self.hexSize = size
		self.color = color
		
		self.points = []
		self.points.append((self.hexX - self.hexSize, self.hexY))
		self.points.append((self.hexX - (self.hexSize/2), self.hexY - (0.866*self.hexSize)))
		self.points.append((self.hexX + (self.hexSize/2), self.hexY - (0.866*self.hexSize)))
		self.points.append((self.hexX + self.hexSize, self.hexY))
		self.points.append((self.hexX + (self.hexSize/2), self.hexY + (0.866*self.hexSize)))
		self.points.append((self.hexX - (self.hexSize/2), self.hexY + (0.866*self.hexSize)))
		
	def draw(self): 
		pygame.draw.polygon(WIN, self.color, self.points, 0)

""" Set up board """
board = Board(60)

# run game unless QUIT
run = True
while run:
	clock.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
			sys.exit()

	# draw the window and update
	update_window()

	# draw the board
	board.draw()

pygame.quit()