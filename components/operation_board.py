from dice import *
from button import *
from random import *

OperationType = {
    "RollDice":"Roll Dice",
    "ExchangeResource" : "Exchange",
    "RobResource": "Rob" ,
    "FinishTurn" : "Finish"
}

class OperationBoard:
    def __init__(self, surface):
        self.type = "Init"
        self.height = surface.get_height() * 0.3
        self.width = surface.get_width() * 0.3
        self.x = surface.get_width() - self.width - 30
        self.y = surface.get_height() - self.height - 30

        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(LIGHTBLUE)
        self.super_surface = surface
        self.draw_board()

    def change_board_type(self, type):
        if (type == "RollDice"):
            self.type = "RollDice"
            self.button = Button(self, 'Roll Dice', BLACK, 1/2, 3/4)
        elif (type == "ExchangeResource"):
            self.type = "ExchangeResource"
        elif (type == "RobResource"):
            self.type = "RobResource"
        elif (type == "FinishTurn"):
            self.type = "FinishTurn"
        else:
            self.type = "Init"
        self.update()

    def roll_dice(self):
        dice1 = Dice(self, 1/4, 5/12)
        dice2 = Dice(self, 3/4, 5/12)
        self.update()
        value1 = randint(1, 6)
        value2 = randint(1, 6)
        async def roll_animation():
            await asyncio.gather(dice1.roll(value1), dice2.roll(value2))
        asyncio.run(roll_animation())
        return value1, value2

    def draw_board(self):
        self.super_surface.blit(self.surface, (self.x, self.y))

    def update(self):
        self.draw_board()

    def remove(self):
        # self.button.remove()
        # self.button = None
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
        # self.update()

    def change_button_color(self, color):
        self.button.change(color = color)
        # self.update()





