import pygame
from settings import *
from bonus_case import *
from pygame import Vector2
from player import Player
from marker import Marker
from table import Table
from marker_container import *
from player_interface import *
from context import GameContext
from item import *
from item_area import *
from button import *


class TicTacToe:
    def __init__(self, game_session : GameSession, game):
        self.session : GameSession = game_session
        self.game = game


        self.player1, self.player2 = self.session.players
        self.active_player = self.player1
        self.inventories = self.session.inventories
        self.table = Table(self.game)
        self.state = 'playing'  # 'playing', 'win', 'draw'
        self.winner = None


        self.start_turn()
        


    def new_game(self, first_player = None):
        self.active_player = first_player if first_player is not None else random.choices([self.player1, self.player2])[0]

        self.table.reset_cases()
        self.state = 'playing'  # 'playing', 'win', 'draw'
        self.winner = None
        self.start_turn()


    def _active_inventory(self):
        return self.session.get_inventory(self.active_player)

    def start_turn(self):
        inv = self._active_inventory()
        inv.add_marker()
        inv.set_case_callback(self._place_case)
        inv.set_release_callback(self._try_place)

    def _place_case(self):
        inv = self._active_inventory()
        current_item : Item = inv.case_inventory.get_selected()
        if current_item is None:
            return
        index = self.table.try_place_case(current_item)
        if index is None:
            return
        
        case = current_item.object
        self.table.change_case(case, index)
        inv.case_placed()
        

    def _try_place(self):
        inv = self._active_inventory()
        marker = inv.marker_container.marker
        if marker is None:
            return
        context = GameContext(self.active_player, self.table, self.session)
        case, context = self.table.try_place_marker(marker, context)
        if case is None:
            return
        
        context = self.table.place_marker(marker, context, case)
        
        inv.notify_placed()
        self.apply_context_events(context)
        self.apply_effects(context)

    def apply_context_events(self, context : GameContext):
        self.table.apply_context(context)
        for player, gain in context.gains.items():
            player.pay(gain)
        for effect in context.effects:
            self.game.add_effect(effect)
    

    def apply_effects(self, context : GameContext):
        result, winner = self.table.get_result()
        if result == 'win':
            print(result, winner.name)
            self.state = 'win'
            self.winner = winner
            self.end_round(context)
        elif result == 'draw':
            print(result)
            self.state = 'draw'
            self.end_round(context)
        elif result == 'ongoing':
            self.active_player = self.player1 if self.active_player == self.player2 else self.player2
            if context.replay: self.active_player = context.player
            
            
            for inv in self.inventories.values():
                inv.delete_callbacks()

            self.start_turn()

    def end_round(self, context :GameContext):
        context = self.table.trigger_end_round_ablility(context)
        for player, gain in context.gains.items():
            player.pay(gain)
        for player, lost in context.losts.items():
            player.lose_money(lost)

        self.new_game(context.first_to_play)




    def handle_input(self, mouse_pos):
        if self.state != 'playing':
            return


    def update(self, dt):
        self.table.update(dt)



