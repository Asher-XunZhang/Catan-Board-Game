# Player class

class Player:
    def __init__(self, resource_cards, development_cards):
        self.resource_cards = resource_cards
        self.development_cards = development_cards

    def get_resource_cards(self):
        return self.resource_cards

    """
    def roll(self):
        call roll function
    """
