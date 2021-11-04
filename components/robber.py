"""
Robber Class

"""
import pygame

GREY = (128,128,128)

class Robber:
    def __init__(self, surface, position):
        self.surface = surface
        self.position = position
        pygame.draw.circle(surface, GREY, position, 18)

    def move(self, surface, new_position):
        self.position = new_position
        pygame.draw.circle(surface, GREY, new_position, 18)

