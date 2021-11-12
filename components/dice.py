import pygame
import random
import asyncio
from color import *
from calculation import *

class Dice:
    diceStopImg = {
        1: pygame.image.load("../resources/img/dice/dice_1.png"),
        2: pygame.image.load("../resources/img/dice/dice_2.png"),
        3: pygame.image.load("../resources/img/dice/dice_3.png"),
        4: pygame.image.load("../resources/img/dice/dice_4.png"),
        5: pygame.image.load("../resources/img/dice/dice_5.png"),
        6: pygame.image.load("../resources/img/dice/dice_6.png")
    }
    diceSpinImg = [  pygame.image.load("../resources/img/dice/dice_action_1.png"),
                     pygame.image.load("../resources/img/dice/dice_action_2.png"),
                     pygame.image.load("../resources/img/dice/dice_action_3.png")]

    def __init__(self, super_surface_object, x, y):
        self.super_surface = super_surface_object.surface
        self.super_surface_object = super_surface_object

        self.dice = pygame.image.load("../resources/img/dice/dice_action_0.png")
        self.diceRect = self.dice.get_rect()
        self.surface = pygame.Surface((self.diceRect.width, self.diceRect.height))

        position = blit_position_transfer(self.super_surface, self.surface, x, y)
        self.x = position[0]
        self.y = position[1]

        self.surface.fill(LIGHTBLUE)

        self.StopStatus= random.randint(1,6)
        self.SpinStatus=0

        self.surface.blit(self.dice, self.diceRect)
        self.update()


    def update(self):
        self.super_surface.blit(self.surface, (self.x, self.y))
        self.super_surface_object.update()

    async def roll(self, value):
        clock = pygame.time.Clock()
        current_time = pygame.time.get_ticks()
        duration = 600
        while pygame.time.get_ticks() < current_time + duration:
            clock.tick(20)
            self.move()
            await asyncio.sleep(0.001)
            pygame.display.update()
        self.stop(value)

    def move(self):
        self.SpinStatus += 1
        if self.SpinStatus == 3:
            self.SpinStatus = 0
        self.surface.fill(LIGHTBLUE)
        self.surface.blit(self.diceSpinImg[self.SpinStatus], self.diceRect)
        self.update()


    def stop(self, value):
        self.StopStatus = value
        self.surface.fill(LIGHTBLUE)
        self.surface.blit(self.diceStopImg[self.StopStatus], self.diceRect)
        self.update()
