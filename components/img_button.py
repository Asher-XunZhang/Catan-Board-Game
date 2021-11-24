import pygame
from color import *
from calculation import *

class ImgButton:
    def __init__(self, super_surface_object, imgResource, size, x, y, proportion = True):
        self.size = size

        self.super_surface = super_surface_object.surface
        self.super_surface_object = super_surface_object
        self.color = BLACK
        self.image = pygame.image.load(imgResource).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.imageRect = self.image.get_rect()
        self.surface = pygame.Surface((self.imageRect.width, self.imageRect.height))
        self.surface.blit(self.image, blit_position_transfer(self.surface, self.image))
        self.surface.set_colorkey(TRASPARENT)
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        self.is_hover = False

        if proportion:
            position = blit_position_transfer(self.super_surface, self.surface, x, y)
        else:
            position = (x, y)
        self.x = position[0]
        self.y = position[1]
        self.display()

    def display(self):
        self.super_surface.blit(self.surface, (self.x, self.y))
        self.super_surface_object.update()

    def update(self):
        self.display()

    def remove(self):
        self.surface.fill(LIGHTBLUE)
        self.update()

    def check_click(self, position):
        x_match = position[0] > self.x and position[0] < self.x + self.width
        y_match = position[1] > self.y and position[1] < self.y + self.height
        global cursor_state
        if x_match and y_match:
            if self.is_hover != True:
                self.is_hover = True
                cursor_state = "hand"
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                self.change_color(RED)
        else:
            if self.is_hover != False:
                self.is_hover = False
                cursor_state = "normal"
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                self.change_color(BLACK)
        return self.is_hover

    def change_color(self, color=None):
        if color:
            pygame.pixelarray.PixelArray(self.surface).replace(self.color, color)
            self.color = color
            self.display()