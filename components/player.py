"""
Player class

"""


class Player:
    def __init__(self, color):
        self.color = color
        self.settlement = 0
        self.city = 0
        self.road = 0
        self.resources = {
            "brick": 0,
            "ore": 0,
            "grain": 0,
            "lumber": 0,
            "wool": 0
        }
        self.total_points = 0

    def get_total_points(self):
        return self.settlement * 1 + self.city * 2 #TODO: Check the rule that if roads should be counted to points

