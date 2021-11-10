"""
Player class

"""


class Player:
    def __init__(self, settlements, roads, color):
        self.color = color
        self.settlements = settlements
        self.roads = roads
        self.bricks = 0
        self.ore = 0
        self.grain = 0
        self.lumber = 0
        self.wool = 0
        self.development_cards = []
        self.cities = []
        self.victory_points = 0

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

    def send_trade(self, other_player, bricks_val, ore_val, grain_val, lumber_val, wool_val):
        if (bricks_val <= self.bricks or ore_val <= self.ore or grain_val <= self.grain or lumber_val <= self.lumber or wool_val <= self.wool):
            if (bricks_val <= other_player.bricks or ore_val <= other_player.ore or grain_val <= other_player.grain or lumber_val <= other_player.lumber or wool_val <= other_player.wool):
                self.bricks += bricks_val
                self.ore += ore_val
                self.grain += grain_val
                self.lumber += lumber_val
                self.wool += wool_val
                s =  "Trade complete!"
                return s
            else:
                s = "Cannot make trade: Your opponent doesn't have the resources"
                return s
        else:
            s = "Cannot make trade: You don't have the resources"
            return s


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

