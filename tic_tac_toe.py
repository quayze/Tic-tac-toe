import pygame
from settings import *
from bonus_squares import *
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
from effect_group import *


class TicTacToe:
    def __init__(self, game_session : GameSession, game):
        self.session : GameSession = game_session
        self.game = game
        self.game_effects = EffectGroup()

        self.player1, self.player2 = self.session.players
        self.active_player = self.player1
        self.inventories = self.session.inventories
        self.table = Table(self.game)
        self.state = 'playing'  # 'playing', 'win', 'draw', 'ending'
        self.winner = None
        self.context = None

    def start_playing(self):
        self.state = 'playing' 
        self.winner = None
        self.turns_left = 10
        self.table.activate()
        self.table.spawn_squares()
        self.start_turn()
        


    def new_game(self, first_player = None):
        self.turns_left -= 1

        self.active_player = first_player if first_player is not None else random.choices([self.player1, self.player2])[0]

        context = GameContext()
        context = self.table.reset_cases(context)
        self.apply_context_events(context)


        self.state = 'playing'
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
            self.game_effects.add_effect(effect,self.game)

    

    def apply_effects(self, context : GameContext):
        self.context = context
        result, winner, squares = self.table.get_result()

        if result == 'win':
            self.state = 'win'
            self.winner = winner
            self.game_effects.add_effect(WinEffect(squares[0].get_pos(), squares[-1].get_pos(),
                                                   overshoot= 40), self.game)

        elif result == 'draw':
            self.state = 'draw'

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
        

        if self.turns_left == 0:
            self.state = 'ending'
            context = GameContext()
            context = self.table.destroy(context)
            self.apply_context_events(context)
            return
        
        self.new_game(context.first_to_play)

    def handle_input(self, mouse_pos):
        if self.state != 'playing':
            return


    def update(self, dt):
        self.table.update(dt)

        if self.state == 'playing':
            pass
        elif self.state == 'win':
            self.update_win(dt)
        elif self.state == 'draw':
            self.update_draw(dt)
        elif self.state == 'ending':
            self.update_ending(dt)

    def update_win(self, dt):
        if self.game_effects.is_done():
            self.end_round(self.context)
    
    def update_draw(self, dt):
        if self.game_effects.is_done():
            self.end_round(self.context)

    def update_ending(self, dt):
        if self.game_effects.is_done():
            self.game.next_phase()

    
            



