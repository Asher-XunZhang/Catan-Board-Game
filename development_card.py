"""
Development Card Class

"""


class DevelopmentCard:
    def __init__(self, name, victory_points, description):
        self.name = name
        self.victory_points = victory_points
        self.description = description

    def get_victory_points(self):
        return self.victory_points
