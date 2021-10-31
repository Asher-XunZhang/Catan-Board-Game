import pygame



WHITE = (255, 255, 255)
BLACK = (1, 1, 1)
RED = (255, 0, 0)

class Button(object):
	def __init__(self, text, color, x, y):
		# font = pygame.font.SysFont('Arial', 36)
		font = pygame.font.Font('../resources/font/OpenSans-Semibold.ttf', 28)
		self.surface = font.render(text, True, color)
		self.WIDTH = self.surface.get_width()
		self.HEIGHT = self.surface.get_height()
		self.x = x
		self.y = y

	def display(self, surface):
		surface.blit(self.surface, (self.x, self.y))

	def check_click(self, position):
		x_match = position[0] > self.x and position[0] < self.x + self.WIDTH
		y_match = position[1] > self.y and position[1] < self.y + self.HEIGHT
		if x_match and y_match:
			return True
		else:
			return False