from math import sin, cos, pi, sqrt
import pygame
from hexagon import Hexagon
import random
from calculation import *


class Board:
    def __init__(self, surface):
        side = min(surface.get_width(), surface.get_height())*3/4
        self.surface = pygame.Surface((side, side))
        self.draw_board()
        self.surface.set_colorkey((0,0,0))
        surface.blit(self.surface, blit_position_transfer(surface, self.surface))


    def draw_board(self):
        x, y = self.surface.get_width()/2, self.surface.get_height()/2
        side = self.surface.get_width()*4/9
        self.hex = pygame.draw.polygon(self.surface, (135,206,250), [
            (x + side * cos(2 * pi * i / 6),y + side * sin(2 * pi * i / 6))
            for i in range(6)
        ])
        element = []
        element += ["wool"] * 4 + ["lumber"] * 4 + ["grain"] * 4 + ["brick"] * 3 + ["ore"] * 3
        random.shuffle(element)
        random.shuffle(element)
        element.insert(9, "desert")
        print(element)
        self.hexes = []
        initX, initY = 150, 80
        hex_side = 50

        for i in range(19):
            if(i <= 2):
                hex = Hexagon(self.surface, i, element[i], hex_side, ((i-0)*2*hex_side + initX, initY))
                # self.hexes.append(hex)
            elif( 3 <= i <= 6):
                hex = Hexagon(self.surface, i, element[i], hex_side, ((i-3)*2*hex_side + initX - hex_side, 2*hex_side+initY-15))
                # self.hexes.append(hex)
            elif( 7 <= i <= 11):
                hex = Hexagon(self.surface, i, element[i], hex_side, ((i-7)*2*hex_side + initX - hex_side*2, 4*hex_side+initY-30))
            elif( 12 <= i <= 15):
                hex = Hexagon(self.surface, i, element[i], hex_side, ((i-12)*2*hex_side + initX - hex_side, 6*hex_side+initY-45))
            else:
                hex = Hexagon(self.surface, i, element[i], hex_side, ((i-16)*2*hex_side + initX, 8*hex_side+initY-60))
            self.hexes.append(hex)

    def hexes_infos(self):
        return self.hexes
