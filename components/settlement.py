import pygame


# TODO: more functions

class Settlement:
    def __init__(self, surface, position):
        self.owner = None
        self.surface = surface
        self.position = position

    def draw_settlement(self):
        pygame.draw.rect(self.surface, self.owner.color, self.position, 2)

    def assign_settlement_player(self, player):
        self.owner = player

    # Function to clear colors using blit
    """ TESTING WITH RED should be  (255, 255, 255, 128)"""

    def clear_settlement(self):
        pygame.draw.rect(self.surface, (255, 0, 0), self.position, 2)

    def get_position(self):
        return self.position
