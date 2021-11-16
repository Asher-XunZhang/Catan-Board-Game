# TODO: clean up button display functions. May not all be needed.

import pygame, sys, math

WHITE = (255, 255, 255)
BLACK = (1, 1, 1)
RED = (255, 0, 0)


class Button(object):
	def __init__(self, text, color, hover_color, x, y):
		# font = pygame.font.SysFont('Arial', 36)
		font = pygame.font.Font('resources/font/OpenSans-Semibold.ttf', 28)
		self.surface_text = font.render(text, True, color)
		self.color = color
		self.hover_color = hover_color
		self.WIDTH = self.surface_text.get_width()
		self.HEIGHT = self.surface_text.get_height()
		self.x = x
		self.y = y

	# Diplay button with text
	def display_button_text(self, surface):
		surface.blit(self.surface_text, (self.x, self.y))

	def display_settlement_button(self, surface, hover):
		if hover:
			pygame.draw.circle(surface, self.hover_color, ((self.x), (self.y)), 10)
		else:
			pygame.draw.circle(surface, self.color, ((self.x),(self.y)), 10)
		playing = True

	def check_click(self, position):
		x_match = position[0] > self.x and position[0] < self.x + self.WIDTH
		y_match = position[1] > self.y and position[1] < self.y + self.HEIGHT
		if x_match and y_match:
			return True
		else:
			return False

	def get_pos(self):
		return [self.x, self.y]

	def change_button_color(self, color, hover_color):
		self.color = color
		self.hover_color = hover_color
