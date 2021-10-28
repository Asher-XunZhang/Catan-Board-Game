import pygame

class Settler:
    def __init__(self, owner, surface, position):
        self.owner = owner
        self.surface = surface
        self.position = position

    def draw_settlement(self):
        pygame.draw.polygon(self.surface, self.owner.color, self.position, 2)
