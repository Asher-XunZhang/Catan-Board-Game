import pygame


class Road:

    def __init__(self, owner, surface, start, end):
        self.owner = owner
        self.surface = surface
        self.start = start
        self.end = end
        self.width = 4

    def draw_road(self):
        pygame.draw.line(self.surface, self.owner.color, self.start, self.end, 5)

    def check_click(self, x, y):
        x_match = self.start < x < self.end + self.width
        y_match = self.start < y < self.end + self.HEIGHT
        if x_match and y_match:
            return True
        else:
            return False

