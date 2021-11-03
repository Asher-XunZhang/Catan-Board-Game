from math import sin, cos, pi, ceil,floor,radians
import pygame
from calculation import *

class Hexagon:
    Image = {
        "wool": "../resources/img/wool.png",
        "lumber": "../resources/img/lumber.png",
        "grain": "../resources/img/grain.png",
        "brick": "../resources/img/brick.png",
        "ore": "../resources/img/ore.png",
        "hill": "../resources/img/brick.png",
        "forest": "../resources/img/lumber.png",
        "field": "../resources/img/grain.png",
        "mountain": "../resources/img/ore.png",
        "pasture": "../resources/img/wool.png",
        "desert": "../resources/img/desert.png",
    }
    Color = {
        "pasture": (124, 252, 0),
        "forest": (153, 76, 0),
        "field": (255, 128, 0),
        "hill": (178, 34, 34),  # (205, 92, 92),
        "mountain": (192, 192, 192),  # (224,224,224),
        "desert": (255, 215, 0)
    }
    def __init__(self, surface, id, num, type, hex_side, position):
        self.hex_side = hex_side
        self.surface = pygame.Surface((self.hex_side*2, self.hex_side*2))
        self.id = id
        self.type = type
        self.settlements = []
        self.num = num
        self.position = position
        self.font = pygame.font.SysFont('Arial', 25)
        self.image = pygame.image.load(self.Image[type]).convert_alpha()
        self.draw_regular_polygon(self.Color[type], (0, 0))
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

        pygame.draw.circle(self.surface, (255, 255, 255), (x, y + 30), 15)
        num_text = self.font.render(str(self.num), True, (6, 6, 6))
        self.surface.blit(num_text, (x - 8, y + 15))

        self.image = pygame.transform.scale(self.image, (self.hex_side, self.hex_side))
        self.surface.blit(self.image, blit_position_transfer(self.surface, self.image))