import pygame
from color import *
from calculation import *

# TODO: more functions

class Settlement:
    def __init__(self, super_surface_object, radius, color, hover_color, x, y):

        self.color = color
        self.hover_color = hover_color
        self.hover_status = False

        self.clicked = BLACK

        self.side = radius*2
        self.surface = pygame.Surface((self.side, self.side))

        self.super_surface = super_surface_object.surface
        self.super_surface_object = super_surface_object

        self.x = x
        self.y = y

        self.display_settlement_button()
        self.display()


    def display(self):
        self.super_surface.blit(self.surface, (self.x, self.y))
        self.super_surface_object.update()

    def update(self):
        self.display()

    def remove(self):
        self.surface.fill(LIGHTBLUE)
        self.update()

    def update_together(self):
        self.super_surface.blit(self.surface, (self.x, self.y))

    def check_hover(self, position):
        x_match = position[0] > self.x - self.side and position[0] < self.x + self.side
        y_match = position[1] > self.y - self.side and position[1] < self.y + self.side
        if x_match and y_match:
            self.hover_status = True
            settlement_object = self
        else:
            self.hover_status = False
            settlement_object = None
        self.display_settlement_button()
        return (self.hover_status, settlement_object)

    # Display settlement circle button
    def display_settlement_button(self):
        if self.hover_status:
            pygame.draw.circle(self.surface, self.hover_color, (self.side/2, self.side/2), 10)
        else:
            pygame.draw.circle(self.surface, self.color, (self.side/2, self.side/2), 10)
        self.update_together()


    def get_pos(self):
        return (self.x, self.y)

    def change_button_color(self, color, hover_color):
        self.color = color
        self.hover_color = hover_color

