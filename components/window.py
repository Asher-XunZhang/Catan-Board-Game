import pygame
from board import Board
from random import *
from player import Player
from robber import Robber
from button import *
from dice import *

class Window:
    def __init__(self):
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((1280, 800))
        screen.fill((0, 191, 255))
        pygame.display.set_caption("Catan")
        board = Board(screen)
        hexes = board.hexes_infos()

        roll_button_x = 100
        roll_button_y = 600

        roll_button = Button('Roll Dice', WHITE, roll_button_x, roll_button_y)
        roll_button.display(screen)

        # User input for player color, settlement locations
        my_player = Player(0, 0, 0, 0, 0, [], [], [], [], 0, "blue")
        robber = Robber(board, (0, 0))
        pygame.display.flip()
        while True:
            clock.tick(20)

            # Button hover animation:
            if roll_button.check_click(pygame.mouse.get_pos()):
                roll_button = Button('Roll Dice', BLACK, roll_button_x, roll_button_y)
            else:
                roll_button = Button('Roll Dice', WHITE, roll_button_x, roll_button_y)
            roll_button.display(screen)
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
                        if roll_button.check_click(pygame.mouse.get_pos()):
                            num1, num2 = self.dice_roll()
                            start_x = roll_button.x + roll_button.WIDTH/2 - 100
                            start_y = roll_button.y - 100
                            self.dice_1 = Dice(screen, start_x, start_y)
                            self.dice_2 = Dice(screen, 100 + self.dice_1.position[0], self.dice_1.position[1])
                            asyncio.run(self.dice_roll_animation(num1, num2))

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
                                            pass
                                            # settlement.owner.add_single_resources(tile.element)
                                        # Iterate through cities?

            pygame.display.update()

    def dice_roll(self):
        # seed(1)
        value1 = randint(1, 6)
        value2 = randint(1, 6)
        return value1, value2

    async def dice_roll_animation(self, num1, num2):
        await asyncio.gather(self.dice_1.roll(num1), self.dice_2.roll(num2))




if __name__ == '__main__':
    game = Window()
