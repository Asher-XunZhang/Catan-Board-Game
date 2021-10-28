"""
Robber Class

TODO: Create visual representation
"""
import pygame


class Robber:
    def __init__(self, surface, position):
        self.surface = surface
        self.position = position

    def move(self, new_position):
        self.position = new_position
