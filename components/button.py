import pygame
from color import *
from calculation import *

class Button:
	def __init__(self, super_surface_object, text, color, x, y):
		self.font = pygame.font.Font('../resources/font/OpenSans-Semibold.ttf', 28)
		self.text = text
		self.color = color
		self.surface = self.font.render(self.text, True, self.color)
		self.width = self.surface.get_width()
		self.height = self.surface.get_height()

		self.super_surface = super_surface_object.surface
		self.super_surface_object = super_surface_object
		position = blit_position_transfer(self.super_surface, self.surface, x, y)
		self.x = position[0]
		self.y = position[1]
		self.display()

	def display(self):
		self.super_surface.blit(self.surface, (self.x, self.y))
		self.super_surface_object.update()

	# def remove(self):
	# 	self.surface.fill(DARKSKYBLUE)
	# 	del self

	def check_click(self, position):
		x_match = position[0] > self.x and position[0] < self.x + self.width
		y_match = position[1] > self.y and position[1] < self.y + self.height
		if x_match and y_match:
			return True
		else:
			return False

	def change(self, color=None, text = None):
		if color:
			self.color = color
		if text:
			self.text = text
		self.surface = self.font.render(self.text, True, self.color)
		self.width = self.surface.get_width()
		self.height = self.surface.get_height()
		self.display()