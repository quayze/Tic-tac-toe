class Player:
    def __init__(self, name : str, markers_type = 'cross', color_theme = 'blue'):
        self.name = name
        self.marker_type = markers_type
        self.color_theme = color_theme
        self.balance = 0

    def pay(self, amount : int):
        self.balance += amount

    def get_balance(self):
        return self.balance