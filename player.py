class Player:
    def __init__(self, name : str, markers_type = 'cross', color_theme = 'blue'):
        self.name = name
        self.marker_type = markers_type
        self.color_theme = color_theme
        self.balance = 20

    def pay(self, amount : int):
        self.balance += amount

    def lose_money(self, amount : int):
        if amount < 0:
            amount = min(abs(amount), self.balance)
            self.balance -= amount

    def get_balance(self):
        return self.balance