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

    def add_single_resources(self, element):
        if element == "hills":
            self.bricks += 1
        elif element == "pasture":
            self.wool += 1
        elif element == "forest":
            self.lumber += 1
        elif element == "field":
            self.grain += 1
        elif element == "mountain":
            self.ore += 1

    def add_double_resources(self, element):
        if element == "hills":
            self.bricks += 2
        elif element == "pasture":
            self.wool += 2
        elif element == "forest":
            self.lumber += 2
        elif element == "field":
            self.grain += 2
        elif element == "mountain":
            self.ore += 2


    """
    def roll(self):
        call roll function
        increment resource cards
    """
