"""
Development Card Class

TODO: Implement Monopoly card
"""
from road import Road


class DevelopmentCard:
    def __init__(self, name, victory_points, description):
        self.name = name
        self.victory_points = victory_points
        self.description = description

    def get_victory_points(self):
        return self.victory_points

    def action(self, player, robber):
        if self.name == "Victory Point":
            pass
        elif self.name == "Knight":
            robber.move()
        elif self.name == "Year of Plenty":
            player.add_double_resources("field")
        elif self.name == "Road Building":
            road1 = Road(player, 0, 0, 0)
            road1.draw_road()
            road2 = Road(player, 0, 0, 0)
            road2.draw_road()
            player.roads += road1
            player.roads += road2
