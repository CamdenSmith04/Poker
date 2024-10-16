class Table:
    def __init__(self, pot, topBet, cards):
        self.pot = pot
        self.topBet = topBet
        self.cards = cards

    def set_pot_(self, new_pot):
        self.pot = new_pot
        return
   
    def set_round_bet(self, new_topBet):
        self.topBet = new_topBet
        return
    
    def set_cards(self, new_cards):
        self.set_cards = new_cards
        return