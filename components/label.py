import pygame
from color import *
from calculation import *

class Label:
    def __init__(self, super_surface_object, text, color, front_size, x, y, porpotion = True):
        self.font = pygame.font.Font('../resources/font/OpenSans-Semibold.ttf', front_size)
        self.text = text
        self.color = color

        self.surface = self.font.render(self.text, True, self.color)

        self.width = self.surface.get_width()
        self.height = self.surface.get_height()

        self.super_surface = super_surface_object.surface
        self.super_surface_object = super_surface_object

        if porpotion:
            position = blit_position_transfer(self.super_surface, self.surface, x, y)
        else:
            position = (x, y)

        self.x = position[0]
        self.y = position[1]
        self.display()

    def display(self):
        self.super_surface.blit(self.surface, (self.x, self.y))
        self.super_surface_object.update()

    def update(self):
        self.display()

    def remove(self):
        self.surface.fill(LIGHTBLUE)
        self.update()

    def change(self, color=None, text = None):
        if color:
            self.color = color
        if text:
            self.text = text
        self.surface = self.font.render(self.text, True, self.color)
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.display()