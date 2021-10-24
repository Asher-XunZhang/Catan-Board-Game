import pygame

class Road:

    def __init__(self, owner, surface, start, end):
        self.owner = owner
        self.surface = surface
        self.start = start
        self.end = end

    def draw_road(self):
        points = {self.start, self.end} #The two points for the line
        pygame.draw.polygon(self.surface, self.owner.color, points, 4)