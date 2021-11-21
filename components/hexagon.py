from math import sin, cos, pi, ceil,floor,radians
import pygame
from color import *
import asyncio
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

    def __init__(self, surface, super_surface_object, id, num, type, hex_side, position):
        self.hex_side = hex_side
        self.super_surface = surface
        self.super_surface_object = super_surface_object
        self.x = position[0]
        self.y = position[1]
        self.surface = pygame.Surface((self.hex_side*2, self.hex_side*2))
        self.id = id
        self.type = type
        self.settlements = []
        self.players = []
        self.num = num
        self.font = pygame.font.SysFont('Arial', 25)
        self.image = pygame.image.load(self.Image[type]).convert_alpha()
        self.draw_regular_polygon(self.Color[type])
        self.surface.set_colorkey(TRASPARENT)
        self.display()

    def get_corner(self):
        # Settlement points
        n, r = 6, self.hex_side
        x, y = self.surface.get_width() / 2, self.surface.get_height() / 2
        corner_points = [
            (x + (r + 7) * sin(2 * pi * i / n), y + (r + 7) * cos(2 * pi * i / n))
            for i in range(n)
        ]
        return corner_points

    def draw_regular_polygon(self, color, text_color = WHITE):
        n, r = 6, self.hex_side
        x, y = self.surface.get_width()/2, self.surface.get_height()/2
        points = [
            (x + r * sin(2 * pi * i / n), y + r * cos(2 * pi * i / n))
            for i in range(n)
        ]
        self.hex = pygame.draw.polygon(self.surface, color, points)

        self.circle_radius = 30
        self.circle_surface = pygame.Surface((self.circle_radius, self.circle_radius))
        self.text_color = text_color
        pygame.draw.circle(self.circle_surface, text_color, (self.circle_radius/2 , self.circle_radius/2), 15)
        num_text = self.font.render(str(self.num), True, (6, 6, 6))
        self.circle_surface.blit(num_text, blit_position_transfer(self.circle_surface, num_text))
        self.circle_surface.set_colorkey(TRASPARENT)
        self.surface.blit(self.circle_surface, blit_position_transfer(self.surface, self.circle_surface, x=1/2, y=4/5))

        self.image = pygame.transform.scale(self.image, (self.hex_side, self.hex_side))
        self.surface.blit(self.image, blit_position_transfer(self.surface, self.image))


    async def shrink(self):
        clock = pygame.time.Clock()
        current_time = pygame.time.get_ticks()
        duration = 1500
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_WAIT)
        while pygame.time.get_ticks() < current_time + duration:
            clock.tick(20)
            self.shrink_color()
            await asyncio.sleep(0.1)
        self.change_num_color(WHITE)

    def shrink_color(self):
        if self.text_color == WHITE:
            self.text_color = RED
            self.change_num_color(RED)
        else:
            self.text_color = WHITE
            self.change_num_color(WHITE)
        self.update()

    def change_num_color(self, color):
        self.draw_regular_polygon(self.Color[self.type], color)
        self.update()

    def display(self):
        self.super_surface.blit(self.surface, (self.x, self.y))
        if len(self.super_surface_object.settlement_points) > 0:
            self.super_surface_object.draw_settlement_points()
        self.super_surface_object.update()

    def update(self):
        self.display()

    def add_player(self, player):
        if player not in self.players:
            self.players.append(player)

    def update_player_resources(self):
        for player in self.players:
            player.add_single_resources(self.type)


