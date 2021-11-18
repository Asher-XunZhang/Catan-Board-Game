import pygame


class Road:

    def __init__(self, surface, start, end):
        self.owner = None
        self.surface = surface
        self.start = start
        self.end = end
        self.width = 4



    def draw_road(self):
        road = pygame.line(self.surface,
                           self.owner.color,
                           [self.start[0], self.start[1]],
                           [self.end[0], self.end[1]],
                           self.width)
        pygame.draw.line(road)

    def assign_player(self, player):
        self.owner = player

    def check_click(self, position):
        if pygame.rect.collidepoint(position[0], position[1]):
            return True
        else:
            return False

