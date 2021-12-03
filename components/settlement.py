import pygame
import asyncio
from color import *
from calculation import *

class Settlement:
    def __init__(self, super_surface_object, radius, color, hover_color, x, y):
        self.type = "initial"
        self.image = None
        self.image_color = None
        self.image_current_color = None
        self.image_color_hover = RED
        self.image_type = None
        self.player = None

        self.color = color
        self.hover_color = hover_color
        self.hover_status = False
        self.radius = radius
        self.side = radius*2
        self.surface = pygame.Surface((self.side, self.side))

        self.super_surface = super_surface_object.surface
        self.super_surface_object = super_surface_object

        self.x = x
        self.y = y

        self.display_settlement_button()
        self.display()


    def display(self):
        self.super_surface.blit(self.surface, (self.x, self.y))
        self.super_surface_object.update()

    def update(self):
        self.display()

    def remove(self):
        self.surface.fill(LIGHTBLUE)
        self.update()

    def update_together(self):
        self.super_surface.blit(self.surface, (self.x, self.y))

    async def check_hover(self, position):
        x_match = position[0] > self.x and position[0] < self.x + self.side
        y_match = position[1] > self.y and position[1] < self.y + self.side
        if x_match and y_match:
            if self.hover_status != True:
                self.hover_status = True
            settlement_object = self
        else:
            if self.hover_status != False:
                self.hover_status = False
            settlement_object = None
        await asyncio.sleep(0.001)
        self.display_settlement_button()
        return (self.hover_status, settlement_object)

    # Display settlement circle button
    def display_settlement_button(self):
        pygame.draw.circle(self.surface, self.color, (self.side / 2, self.side / 2), self.radius)
        if self.hover_status:
            if self.type == "initial":
                pygame.draw.circle(self.surface, self.hover_color, (self.side/2, self.side/2), self.radius, 2)
            else:
                if (self.image!=None) & (self.image_type == self.type) & (self.image_current_color != self.image_color_hover):
                    pygame.pixelarray.PixelArray(self.image).replace(self.image_current_color, self.image_color_hover)
                    self.surface.blit(self.image, blit_position_transfer(self.surface, self.image))
                else:
                    self.image = pygame.image.load(ImageResource[self.type]).convert_alpha()
                    self.image= pygame.transform.scale(self.image, (self.side, self.side))
                    self.image_type = self.type
                    pygame.pixelarray.PixelArray(self.image).replace(BLACK, self.image_color_hover)
                    self.image_current_color = self.image_color_hover
                    self.surface.blit(self.image, blit_position_transfer(self.surface, self.image))

        else:
            if self.type == "initial":
                pygame.draw.circle(self.surface, self.color, (self.side/2, self.side/2), self.radius)
            else:
                if (self.image != None) & (self.image_type == self.type) & (self.image_current_color != self.image_color):
                    pygame.pixelarray.PixelArray(self.image).replace(self.image_current_color, self.image_color)
                    self.surface.blit(self.image, blit_position_transfer(self.surface, self.image))
                else:
                    self.image = pygame.image.load(ImageResource[self.type]).convert_alpha()
                    self.image = pygame.transform.scale(self.image, (self.side, self.side))
                    self.image_type = self.type
                    if(self.image_current_color == None):
                        self.image_current_color = BLACK
                    pygame.pixelarray.PixelArray(self.image).replace(self.image_current_color, self.image_color)
                    self.image_current_color = self.image_color
                    self.surface.blit(self.image, blit_position_transfer(self.surface, self.image))
        self.update_together()


    def get_pos(self):
        return (self.x, self.y)

    def update_type(self, player = None):
        if self.type != "city":
            if self.type == "initial":
                if player != None:
                    self.player = player
                    self.image_color = self.player.color
                self.type = "settlement"
            elif self.type == "settlement":
                self.type = "city"
            self.display_settlement_button()

