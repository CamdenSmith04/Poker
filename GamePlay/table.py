class Table:
    def __init__(self, players, pot, round_bet, round_players, cards):
        self.players = players
        self.pot = pot
        self.round_bet = round_bet
        self.round_players = round_players
        self.cards = cards

    # Used to remove players if they quit the game
    def set_players(self, new_players):
        self.players = new_players
        return

    # Used to keep track of the pot each hand
    def set_pot_(self, new_pot):
        self.pot = new_pot
        return
    
    # Used to keep track of the highest bet people have to match
    def set_round_bet(self, new_round_bet):
        self.round_bet = new_round_bet
        return
    
    # Used to skip players who fold
    def set_round_players(self, new_round_players):
        self.round_players = new_round_players
        return
    
    def set_cards(self, new_cards):
        self.set_cards = new_cards
        return