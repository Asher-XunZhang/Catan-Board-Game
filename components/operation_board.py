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
        self.x = surface.get_width() * 0.7
        self.y = surface.get_height() * 0.7
        self.type = "Init"
        self.height = surface.get_height() * 0.3
        self.width = surface.get_width() * 0.3
        self.surface = pygame.surface.Surface((self.width, self.height))
        self.surface.fill(LIGHTBLUE)
        self.super_surface = surface
        self.draw_board()

    def change_board_type(self, type):
        if (type == "RollDice"):
            self.type = "RollDice"
            self.button = Button(self.surface, 'Roll Dice', BLACK, (self.x + self.width * 1 / 4, self.y + self.height * 4 / 5))
        elif (type == "ExchangeResource"):
            self.type = "ExchangeResource"
            pass
        elif (type == "RobResource"):
            self.type = "RobResource"
            pass
        elif (type == "FinishTurn"):
            self.type = "FinishTurn"
            pass
        self.update()

    def roll_dice(self):
        dice1 = Dice(self.surface, (self.x + self.width * 1 / 4, self.y + self.height * 1 / 4))
        dice2 = Dice(self.surface, (self.x + self.width * 3 / 4, self.y + self.height * 1 / 4))
        value1 = randint(1, 6)
        value2 = randint(1, 6)
        async def roll_animation():
            await asyncio.gather(dice1.roll(value1), dice2.roll(value2))
            print(value1, value2)
        asyncio.run(roll_animation())
        return value1, value2

    def draw_board(self):
        self.super_surface.blit(self.surface, (self.x, self.y))

    def update(self):
        self.draw_board()

    def clean_board(self):
        self.surface.fill(DARKSKYBLUE)
        self.update()

    def check_click(self, position):
        return self.button.check_click(position)

    def change_button_text(self, text):
        self.button.change(text = text)
        # self.update()

    def change_button_color(self, color):
        self.button.change(color = color)
        # self.update()





