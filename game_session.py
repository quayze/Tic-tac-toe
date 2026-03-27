from player_interface import PlayerInventory
class GameSession:
    def __init__(self, player_1, player_2):
        self.players = [player_1, player_2]
        self.inventories = {
            player_1: PlayerInventory(player_1),
            player_2: PlayerInventory(player_2, pos='top')
        }

    def get_inventory(self, player):
        return self.inventories[player]