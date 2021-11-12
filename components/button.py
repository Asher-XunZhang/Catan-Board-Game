import pygame
from color import *

class Button:
	def __init__(self, surface, text, color, position):
		self.font = pygame.font.Font('../resources/font/OpenSans-Semibold.ttf', 28)
		self.super_surface = surface
		self.text = text
		self.color = color
		self.surface = self.font.render(self.text, True, self.color)
		self.WIDTH = self.surface.get_width()
		self.HEIGHT = self.surface.get_height()
		self.x = position[0]
		self.y = position[1]
		self.display()

	def display(self):
		self.super_surface.blit(self.surface, (self.x, self.y))

	def check_click(self, position):
		x_match = position[0] > self.x and position[0] < self.x + self.WIDTH
		y_match = position[1] > self.y and position[1] < self.y + self.HEIGHT
		if x_match and y_match:
			return True
		else:
			return False

	def change(self, color=None, text = None):
		if color:
			self.color = color
		if text:
			self.text = text
		print(self.text)
		print(self.color)
		self.surface = self.font.render(self.text, True, self.color)
		self.display()