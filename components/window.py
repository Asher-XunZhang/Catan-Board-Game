import pygame
from board import Board
from random import *
from player import Player
from robber import Robber
from settler import Settler


def dice_roll():
    seed()
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
        settlement1 = Settler(my_player, Board, (0, 0))
        my_player.settlements.append(settlement1)
        # Hardcode adding settlement to tile for test purposes
        hexes[7].settlements.append(settlement1)
        robber = Robber(board, (0, 0))
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
                        # pick new position for robber
                        new_position = 0
                        robber.move(new_position)
                    else:
                        for tile in hexes:
                            # Check for robber, do not increment if present
                            if tile.num == total:
                                for settlement in tile.settlements:
                                    settlement.owner.add_single_resources(tile.type)
                                # Iterate through cities

            pygame.display.update()


if __name__ == '__main__':
    game = Window()