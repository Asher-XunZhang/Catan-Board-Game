from math import sin, cos, pi, ceil,floor,radians
import pygame
from calculation import *


Type = {
    "wool" : "resources/wool.png",
    "lumber" : "resources/lumber.png",
    "grain" : "resources/grain.png",
    "brick" : "resources/brick.png",
    "ore" : "resources/ore.png",
    "desert" : "resources/desert.png"
}
Color = {
    "wool" : (255, 255, 255),
    "lumber"  : (153,  76, 0),
    "grain" : (255, 128, 0),
    "brick" : (205,92,92),
    "ore"   : (224, 224, 224),
    "desert": (255,215,0)
}

class Hexagon:
    def __init__(self, surface, id, type, hex_side, position):
        self.hex_side = hex_side
        self.surface = pygame.Surface((self.hex_side*2, self.hex_side*2))
        self.id = id
        self.type = type
        self.position = position
        self.image = pygame.image.load(Type[type]).convert_alpha()
        self.draw_regular_polygon(Color[type], (0, 0))
        self.surface.set_colorkey((0, 0, 0))
        surface.blit(self.surface, position)

        # Settlement points
        n, r = 6, self.hex_side
        x, y = self.surface.get_width() / 2, self.surface.get_height() / 2
        self.corner_points = [
            (x + (r + 7) * sin(2 * pi * i / n), y + (r + 7) * cos(2 * pi * i / n))
            for i in range(n)
        ]

    def get_corner(self):
        return self.corner_points

    def draw_regular_polygon(self, color, position):
        n, r = 6, self.hex_side
        x, y = self.surface.get_width()/2, self.surface.get_height()/2
        points = [
            (x + r * sin(2 * pi * i / n), y + r * cos(2 * pi * i / n))
            for i in range(n)
        ]
        self.hex = pygame.draw.polygon(self.surface, color, points)
        self.image = pygame.transform.scale(self.image, (self.hex_side, self.hex_side))
        self.surface.blit(self.image, blit_position_transfer(self.surface, self.image))
