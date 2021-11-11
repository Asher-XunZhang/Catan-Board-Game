import pygame


class City:
    def __init__(self, owner, surface, position):
        self.owner = owner
        self.color = owner.color
        self.surface = surface
        self.position = position

    def draw_city(self):
        pygame.draw.rect(self.surface, self.color, (self.position[0], self.position[1], 20, 20))