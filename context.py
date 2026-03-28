from player import Player


class GameContext:
    def __init__(self, player : Player, table, game_session = None):
        self.player = player
        self.table = table
        self.game_session = game_session

        self.try_place = False
        self.marker_placed = False
        self.new_round = False
        self.end_round = False
        self.destroyed = False

        self.replay = False
        self.blueprint = False
        self.index = None

        self.first_to_play = None
        self.changed_case = {} # case : [new_case, marker]
        self.changed_markers = {}
        self.gains = {} # player : gain
        self.losts = {}

    def add_changed_case(self, base_case, new_case):
        self.changed_case[base_case] = new_case

    def add_marker(self, target_case, marker = None):
        self.changed_markers[target_case] = marker
        


    def add_gain(self, player, gain : int):
        if player not in self.gains:
            self.gains[player] = gain
        else:
            self.gains[player] += gain

    def add_lost(self, player, lost : int):
        if player not in self.losts:
            self.losts[player] = lost
        else:
            self.losts[player] += lost
