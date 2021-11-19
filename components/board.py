from math import sin, cos, pi, sqrt
import pygame
from color import *
from hexagon import *
from robber import *
from button import *
from settlement import *
import random
from calculation import *


class MainBoard:
    def __init__(self, surface):
        side = min(surface.get_width(), surface.get_height())*3/4
        self.super_surface = surface
        self.surface = pygame.Surface((side, side))
        self.settlement_buttons = []
        self.surface.set_colorkey((0, 0, 0))
        self.hexes = []
        self.draw_board()
        self.settlement_points = []
        self.calc_settlement_points()
        self.draw_settlement_points()
        self.update()



    def draw_board(self):
        x, y = self.surface.get_width()/2, self.surface.get_height()/2
        side = self.surface.get_width()*4/9
        self.hex = pygame.draw.polygon(self.surface, LIGHTBLUE, [
            (x + side * cos(2 * pi * i / 6),y + side * sin(2 * pi * i / 6))
            for i in range(6)
        ])
        element = []
        element += ["pasture"] * 4 + ["forest"] * 4 + ["field"] * 4 + ["hill"] * 3 + ["mountain"] * 3
        random.shuffle(element)
        random.shuffle(element)
        element.insert(9, "desert")
        # print(element)
        num = [2] + [12] + [3, 4, 5, 6, 8, 9, 10, 11] * 2
        random.shuffle(num)
        random.shuffle(num)
        num.insert(9, 7)
        self.hexes = {
            2: [],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: [],
            10: [],
            11: [],
            12: []
        }
        initX, initY = 150, 80
        hex_side = 50

        for i in range(19):
            if(i <= 2):
                hex = Hexagon(self.surface, self, i, num[i], element[i], hex_side, ((i-0)*2*hex_side + initX, initY))
            elif( 3 <= i <= 6):
                hex = Hexagon(self.surface, self, i, num[i], element[i], hex_side, ((i-3)*2*hex_side + initX - hex_side, 2*hex_side+initY-15))
            elif( 7 <= i <= 11):
                hex = Hexagon(self.surface, self, i, num[i], element[i], hex_side, ((i-7)*2*hex_side + initX - hex_side*2, 4*hex_side+initY-30))
                # if element[i] == "desert":
                #     robber = Robber(self.surface, self,
                #                     ((i - 7) * 2 * hex_side + initX - hex_side, 5 * hex_side + initY - 25))

            elif( 12 <= i <= 15):
                hex = Hexagon(self.surface, self, i, num[i], element[i], hex_side, ((i-12)*2*hex_side + initX - hex_side, 6*hex_side+initY-45))
            else:
                hex = Hexagon(self.surface, self, i, num[i], element[i], hex_side, ((i-16)*2*hex_side + initX, 8*hex_side+initY-60))
            self.hexes[num[i]].append(hex)


    def get_sett_buttons(self):
        return self.settlement_buttons

    def hexes_infos(self):
        return self.hexes

    # Find settle points
    def calc_settlement_points(self):
        hex_points_board = []
        # Obtain all corner points
        for i in range(2,13):
            for hex in self.hexes[i]:
                hex_points = i.get_corner()
                # Give hex to settlements
                for j in hex_points:
                    points_x = (j[0] + hex.position[0] + 340)
                    points_y = (j[1] + hex.position[1] + 100)
                    hex_points_board.append((points_x, points_y))

        # Delete corner points duplicates
        for corner_t in hex_points_board:
            add = True
            if (len(self.settlement_points) > 0):
                for sett_t in self.settlement_points:

                    if abs(sett_t[0] - corner_t[0]) < 2 and abs(sett_t[1] - corner_t[1]) < 2:
                        add = False
            if (add):
                self.settlement_points.append(corner_t)

        # Add settlement buttons to board
        for i in self.settlement_points:
            new_sett_button = Button('', (0, 191, 255), (200, 250, 250), (i[0]), (i[1]))
            self.settlement_buttons.append(new_sett_button)
        print(len(self.settlement_points))
        print(self.settlement_points)

        # print(len(self.settlement_points))
    def draw_settlement_points(self):
        for i in self.settlement_points:
            pygame.draw.circle(self.surface, BLUE, i, 12)

        # print(len(self.settlement_points))

    # def hexes_shrink(self, hexes):
    #     asyncio.get_event_loop().run_until_complete(asyncio.wait([hex.shrink() for hex in hexes]))
    #     loop = asyncio.get_event_loop()
    #     cors = asyncio.wait(tasks)
    #     loop.run_until_complete(cors)

    def update(self):
        rect = self.super_surface.blit(self.surface, blit_position_transfer(self.super_surface, self.surface))
        pygame.display.update(rect)