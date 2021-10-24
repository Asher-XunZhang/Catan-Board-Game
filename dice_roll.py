from random import seed
from random import randint


def dice_roll():
    seed(1)
    value = randint(1, 12)
    # if value == 7, call robber
