class Player:

    def __init__(self, name, balance, hand, current_bet):
        self.name = name
        self.balance = balance
        self.hand = hand
        # self.round_bet = round_bet
        # self.action = action
        self.current_bet = current_bet

    def initialize(self):
        return f"Player: {self.name} has ${float(self.balance)} and has the following cards: {self.hand}"
    
    def get_name(self):
        print(self.name)
        return self.name
    
    def get_balance(self):
        print(f"${self.balance}")
        return self.balance
    
    def get_hand(self):
        print(f"{self.hand}")
        return self.hand
    
    # def get_round_bet(self):
    #     print(f"{self.round_bet}")
    #     return self.round_bet
    
    # def get_action(self):
    #     print(f"{self.action}")
    #     return self.action
    def get_current_bet(self):
        print(f"{self.current_bet}")
        return self.current_bet
    
    def set_name(self, new_name):
        self.name = new_name
        return
    
    def set_balance(self, new_balance):
        self.balance = new_balance
        return
    
    def set_hand(self, new_hand):
        self.hand = new_hand
        return
    
    # def set_round_bets(self, new_round_bet):
    #     self.round_bet = new_round_bet
    #     return
    
    # def set_action(self, new_action):
    #     self.action = new_action
    #     return

    def set_current_bet(self, new_bet):
        self.current_bet = new_bet
        return

