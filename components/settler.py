import pygame

class Settler:
    def __init__(self, surface, position):
        self.owner = None
        self.surface = surface
        self.position = position

    def draw_settlement(self):
        pygame.draw.polygon(self.surface, self.owner.color, self.position, 2)
