from dice import *
from button import *
from random import *
import time

# OperationType = {
#     "RollDice":"Roll Dice",
#     "ExchangeResource" : "Exchange",
#     "RobResource": "Rob" ,
#     "FinishTurn" : "Finish"
# }

class OperationBoard:
    def __init__(self, surface):
        self.type = "Init"
        self.height = surface.get_height() * 0.3
        self.width = surface.get_width() * 0.3
        self.x = surface.get_width() - self.width - 30
        self.y = surface.get_height() - self.height - 30
        self.button = None
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(LIGHTBLUE)
        self.super_surface = surface
        self.draw_board()

    def change_board_type(self, type):
        if (type == "Roll"):
            if self.button != None:
                self.button.remove()
            self.type = "Roll"
            self.button = Button(self, 'Roll Dice', BLACK, 1/2, 3/4)
        elif (type == "Trade"):
            if self.button != None:
                self.button.remove()
            self.button = Button(self, 'Exchange', BLACK, 1/2, 3/4)
            self.type = "Trade"
        elif (type == "Rob"):
            if self.button != None:
                self.button.remove()
            self.type = "RobResource"
        elif (type == "Finish"):
            if self.button != None:
                self.button.remove()
            self.type = "Finish"
        else:
            if self.button != None:
                self.button.remove()
            self.type = "Init"
        self.update()

    def roll_dice(self):
        dice1 = Dice(self, 1/4, 5/12)
        dice2 = Dice(self, 3/4, 5/12)
        self.update()
        value1 = randint(1, 6)
        value2 = randint(1, 6)
        async def roll_animation():
            global cursor_state
            cursor_state = "wait"
            await asyncio.gather(dice1.roll(value1), dice2.roll(value2))
        asyncio.run(roll_animation())
        self.button.check_click(pygame.mouse.get_pos())

        async def waiting_animation():
            await asyncio.sleep(1.5)

        asyncio.run(waiting_animation())
        # time.sleep(1.5)
        dice1.remove()
        dice2.remove()
        self.update()
        return value1, value2

    def draw_board(self):
        rect = self.super_surface.blit(self.surface, (self.x, self.y))
        pygame.display.update(rect)

    def update(self):
        self.draw_board()

    def remove(self):
        if self.button is not None:
            self.button.remove()
            self.button = None
            del self.button
            self.button = None
        self.surface.fill(DARKSKYBLUE)
        self.update()
        del self

    def check_click(self, position):
        x = position[0] - self.x
        y = position[1] - self.y
        return self.button.check_click((x,y))

    def change_button_text(self, text):
        self.button.change(text = text)

    def change_button_color(self, color):
        self.button.change(color = color)





