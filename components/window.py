import pygame
from main_board import MainBoard
from random import *
from player import Player
from robber import Robber
from button import *
from dice import *
from city import *
from color import *
from settlement import Settlement
from operation_board import OperationBoard, OperationType



class Window:
    def __init__(self):
        pygame.init()
        clock = pygame.time.Clock()
        scree_hight = 800
        screen_width = 1280
        screen = pygame.display.set_mode((screen_width, scree_hight))
        screen.fill((0, 191, 255))
        pygame.display.set_caption("Catan")
        board = MainBoard(screen)
        hexes = board.hexes_infos()

        test_player = Player([], [], BLUE)
        test_city = City(test_player, screen, (10, 10))

        operation_board = OperationBoard(screen)
        operation_board.change_board_type("RollDice")

        robber = Robber(screen, (640, 400))

        # User input for player color, settlement locations
        my_player = Player([], [], BLUE)
        computer = Player([], [], RED)
        # settlement1 = Settler(my_player, Board, (0, 0))
        # my_player.settlements.append(settlement1)
        # Hardcode adding settlement to tile for test purposes
        # hexes[7].settlements.append(settlement1)

        pygame.display.flip()
        while True:
            clock.tick(20)

            test_city.draw_city()

            # Button hover animation:
            if(operation_board.button != None):
                if operation_board.check_click(pygame.mouse.get_pos()):
                    operation_board.change_button_color(RED)
                else:
                    operation_board.change_button_color(BLACK)
                pygame.display.update()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # for test, should be delete after finishing UI part:
                    xMouse = event.pos[0]
                    yMouse = event.pos[1]
                    # print(xMouse, yMouse)
                    # for test, the above codes should be delete after finishing UI part:

                    if pygame.mouse.get_pressed()[0]:
                        if operation_board.check_click(pygame.mouse.get_pos()):
                            num1, num2 = operation_board.roll_dice()
                            total = num1 + num2
                            self.search_hexes(hexes, total)

                        # add AI turn
                        computer_turn_select = randint(0, 5)
                        comp_num1, comp_num2 = self.dice_roll()
                        comp_total = comp_num1 + comp_num2
                        self.search_hexes(hexes, comp_total)
                        if computer_turn_select == 0:
                            pass
                            # build road
                        elif computer_turn_select == 1:
                            pass
                            # build/choose settlement
                        elif computer_turn_select == 2:
                            pass
                            # attempt trade



            pygame.display.update()

    def dice_roll(self):
        value1 = randint(1, 6)
        value2 = randint(1, 6)
        return value1, value2

    def search_hexes(self, hexes, total):
        if total == 7:
            # pick new position for robber
            pass
        else:
            for tile in hexes:
                # Check for robber, do not increment if present
                if tile.num == total:
                    for settlement in tile.settlements:
                        pass
                        # settlement.owner.add_single_resources(tile.element)
                    # Iterate through cities?




if __name__ == '__main__':
    game = Window()
