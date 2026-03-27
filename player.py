class Player:
    def __init__(self, name : str, markers_type = 'cross'):
        self.name = name
        self.marker_type = markers_type
        self.balance = 0

    def pay(self, amount : int):
        self.balance += amount

    def get_balance(self):
        return self.balance