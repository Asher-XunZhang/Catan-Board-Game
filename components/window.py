import pygame
from board import Board
from random import *
from player import Player
# import Robber


def dice_roll():
    seed(1)
    value1 = randint(1, 6)
    value2 = randint(1, 6)
    return value1, value2


class Window:
    def __init__(self):
        pygame.init()
        screen = pygame.display.set_mode((1280, 800))
        screen.fill((0,191,255))
        pygame.display.set_caption("Catan")
        board = Board(screen)
        hexes = board.hexes_infos()
        # User input for player color, settlement locations
        my_player = Player(0, 0, 0, 0, 0, [], [], [], [], 0, "blue")
        # Create Robber
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    xMouse = event.pos[0]
                    yMouse = event.pos[1]
                    print(xMouse, yMouse)
                    num1, num2 = dice_roll()
                    total = num1 + num2
                    if total == 7:
                        pass
                        # Call Robber move function
                    else:
                        for tile in hexes:
                            if tile.num == total:
                                for settlement in tile.settlements:
                                    pass
                                    # settlement.owner.add_single_resources(tile.element)
                                # Iterate through cities?

            pygame.display.update()


if __name__ == '__main__':
    game = Window()