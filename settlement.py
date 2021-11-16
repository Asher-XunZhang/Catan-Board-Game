import pygame

class Settlement:
    def __init__(self, owner, surface, position):
        self.owner = owner
        self.surface = surface
        self.position = position

    def assign_settlement_player(self, player):
        self.owner = player
