import pygame
from main_board import MainBoard
from operation_board import OperationBoard
from random import *
from player import Player
from robber import Robber
from city import *
from color import *
from status_board import StatusBoard


class Window:
    def __init__(self):
        pygame.init()
        clock = pygame.time.Clock()
        scree_hight = 800
        screen_width = 1280
        screen = pygame.display.set_mode((screen_width, scree_hight))
        screen.fill((0, 191, 255))
        self.surface = screen
        self.current_player = None
        pygame.display.set_caption("Catan")
        self.main_board = MainBoard(self)
        self.hexes = self.main_board.hexes_infos()

        # test_player = Player([], [], BLUE)
        # test_city = City(test_player, screen, (10, 10))

        self.operation_board = OperationBoard(self)
        self.operation_board.change_board_type("Build")
        # operation_board.change_board_type("Trade")

        self.status_board = StatusBoard(self)
        # robber = Robber(screen, (640, 400))

        # User input for player color, settlement locations
        my_player = Player(BLUE)
        computer = Player(RED)
        # settlement1 = Settler(my_player, Board, (0, 0))
        # my_player.settlements.append(settlement1)
        # Hardcode adding settlement to tile for test purposes
        # hexes[7].settlements.append(settlement1)

        # set cursor style
        global cursor_state
        cursor_state = "normal"
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        is_opbhover = False
        is_mbhover = False
        self.round = 1
        self.real_player = my_player
        self.current_player = my_player
        pygame.display.flip()
        while True:
            clock.tick(20)
            if (self.operation_board is not None):
                if self.operation_board.type == "Init":
                    self.operation_board.remove()
                    is_opbhover = False
                else:
                    if not is_mbhover:
                        is_opbhover = self.operation_board.check_hover(pygame.mouse.get_pos())

            # Settlement button operations. Checks for cursor hover and clicks and changes color
            if not is_opbhover:
                if self.operation_board.type == "Build":
                    is_mbhover = self.main_board.check_hover(pygame.mouse.get_pos(), self.current_player)

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()

                # elif event.type == pygame.MOUSEBUTTONDOWN:
                #     # for test, should be delete after finishing UI part:
                #     # xMouse = event.pos[0]
                #     # yMouse = event.pos[1]
                #     xMouse = event.pos[0] - self.main_board.x
                #     yMouse = event.pos[1] - self.main_board.y
                    # print(xMouse, yMouse)
                    # for test, the above codes should be delete after finishing UI part:

                    # if pygame.mouse.get_pressed()[0]:
                    #     if(operation_board is not None):
                    #         if (operation_board.type == "Roll"):
                    #            if (operation_board.check_hover(pygame.mouse.get_pos())):
                    #                 total = operation_board.roll_dice(main_board, hexes)
                    #                 operation_board.change_board_type("Trade")

                                    # if total < 7:
                                    #     operation_board = self.remove(operation_board)
                                    # self.search_hexes(hexes, total)

                            # else:
                            #     # add AI turn
                            #     computer_turn_select = randint(0, 5)
                            #     comp_num1, comp_num2 = self.dice_roll()
                            #     comp_total = comp_num1 + comp_num2
                            #     self.search_hexes(hexes, comp_total)
                            #     if computer_turn_select == 0:
                            #         pass
                            #         # build road
                            #     elif computer_turn_select == 1:
                            #         pass
                            #         # build/choose settlement
                            #     elif computer_turn_select == 2:
                            #         pass
                            #         # attempt trade

            pygame.display.update()


    # the surface object must include a "remove" funcition
    def remove(self, surface):
        surface.remove()
        del surface
        return None

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
                        #settlement.owner.add_single_resources(tile.element)
                        print("We did it 2")
                    # Iterate through cities?





if __name__ == '__main__':
    game = Window()
