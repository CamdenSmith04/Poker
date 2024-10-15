class Player:

    def __init__(self, name, balance, hand, current_bet):
        self.name = name
        self.balance = balance
        self.hand = hand
        # self.round_bet = round_bet
        # self.action = action
        self.current_bet = current_bet

    def initialize(self):
        return f"\nPlayer: {self.name}\nBalance: ${float(self.balance)}\nHand: {self.hand}\nCurrent Bet: ${self.current_bet}"
    
    def get_name(self):
        print(self.name)
        return self.name
    
    def get_balance(self):
        print(f"${self.balance}")
        return self.balance
    
    def get_hand(self):
        print(f"{self.hand}")
        return self.hand
    
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

    def set_current_bet(self, new_bet):
        self.current_bet = new_bet
        return

