class GameRules:

    def __init__(self, blinds):
        self.blinds = blinds


class Blinds:
    def __init__(self, small, big):
        self.small = small
        self.big = big

    def get_small(self):
        print(self.small)
        return self.small
    
    def get_big(self):
        print(self.big)
        return self.big

    def set_small(self, new_small):
        self.small = new_small
        return
    
    def set_big(self, new_big):
        self.big = new_big
        return
