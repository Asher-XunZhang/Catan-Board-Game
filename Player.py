"""
Player class

TODO: Add edge case for development cards with victory points
TODO: Add trading call
"""


class Player:
    def __init__(self, resource_cards, development_cards, settlements, cities, roads, victory_points):
        self.resource_cards = resource_cards
        self.development_cards = development_cards
        self.settlements = settlements
        self.cities = cities
        self.roads = roads
        self.victory_points = victory_points

    def get_resource_cards(self):
        return self.resource_cards

    def get_victory_points(self):
        self.count_victory_points()
        return self.victory_points

    def count_victory_points(self):
        # for loop to find VP cards in development cards deck?
        count = len(self.settlements) + \
                2*len(self.cities)
        self.victory_points = count


    """
    def roll(self):
        call roll function
        increment resource cards
    """
