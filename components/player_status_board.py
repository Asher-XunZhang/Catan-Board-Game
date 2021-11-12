import pygame
from color import *
from math import *
from calculation import *

class StatusBoard():
    def __init__(self, surface):
        side = min(surface.get_width(), surface.get_height()) * 1 / 5
        self.surface = pygame.Surface((side, side))
        self.info = {

        }
        self.draw_board()
        self.super_surface = surface
        self.super_surface.blit(self.surface, blit_position_transfer(surface, self.surface))


    def draw_board(self):
        pass
        # x, y = self.surface.get_width() / 2, self.surface.get_height() / 2
        # side = self.surface.get_width() * 4 / 9
        # self.hex = pygame.draw.polygon(self.surface, (135, 206, 250), [
        #     (x + side * cos(2 * pi * i / 6), y + side * sin(2 * pi * i / 6))
        #     for i in range(6)
        # ])
        # self.update_board()

    def remove_board(self):
        self.surface.fill((0, 0, 0))
        self.update_board()

    def update_board(self):
        self.super_surface.blit(self.surface, blit_position_transfer(self.super_surface, self.surface))



        

