"""
Player class

TODO: Add edge case for development cards with victory points
TODO: Add trading call
"""


class Player:
    def __init__(self, bricks, ore, grain, lumber, wool,
                 development_cards, settlements, cities, roads,
                 victory_points, color):
        self.bricks = bricks
        self.color = color
        self.ore = ore
        self.grain = grain
        self.lumber = lumber
        self.wool = wool
        self.development_cards = development_cards
        self.settlements = settlements
        self.cities = cities
        self.roads = roads
        self.victory_points = victory_points

    def get_resource_cards(self):
        return self.bricks, self.ore, self.grain, \
               self.lumber, self.wool

    def get_victory_points(self):
        self.count_victory_points()
        return self.victory_points

    def count_victory_points(self):
        count = 0
        for card in self.development_cards:
            count += self.development_cards.get_victory_points(card)
        count += len(self.settlements) + 2 * len(self.cities)
        self.victory_points = count

    """
    def roll(self):
        call roll function
        increment resource cards
    """
