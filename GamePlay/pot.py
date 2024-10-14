class Pot:
    def __init__(self, size):
        self.size = size

    def get_size(self):
        return self.size
    
    def raise_pot(self, increase):
        self.size = self.size + increase
        return f"Pot size raised to: ${self.size}"
    
    def clear_pot(self):
        self.size = 0
