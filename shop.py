import pygame
from settings import *
from drawable import Drawable
from functions import *
from pygame import Vector2
from player_interface import GameSession
from button import *
from item import *
from item_area import *
from bonus_squares import *
from player import *
from effect import *
from interact_box import *

class Shop(Drawable):
    def __init__(self, game_session : GameSession, game):
        super().__init__(1)
        self.game = game
        self.session = game_session
        self.player1, self.player2 = self.session.players
        

        self.center = Vector2(WIDTH//2, HEIGHT//2)
        self.surface = generate_nine_slice(1400, 600, color= (120, 0, 120))
        self.rect = self.surface.get_rect(center = self.center)

        self.reroll_but = Button(self.center - Vector2(500, 0), 300, 500, (0, 200, 30), text= ['Reroll', '5'])
        self.reroll_price = 5
        self.close_but = Button(self.center + Vector2(500, 0), 300, 500, (200, 0, 0))

        self.case_area = ItemArea(600, self.center, self.game, max_items= 5)
        self.max_cases = 5


        
        self.pay_surfaces = {self.player1 : self.session.get_square_pay_surface(self.player1),
                             self.player2 : self.session.get_square_pay_surface(self.player2)
                             }
        

    def _enable_pay_box(self):
        current_item = self.case_area.get_selected()
        self.pay_surfaces[self.player_active].update_text(f'BUY {current_item.price}')
        self.pay_surfaces[self.player_active].activate()

    def _pay_item(self):
        current_item = self.case_area.get_selected()
        price = current_item.price
        self.pay_surfaces[self.player_active].desactivate()

        if self.pay_surfaces[self.player_active].collision(current_item.rect):
            inventory = self.session.get_inventory(self.player_active)
            if inventory.can_add_item():
                if self.player_active.get_balance() >= price:
                    self.player_active.lose_money(price)
                    self.case_area.transfer()
                    inventory.add_item(current_item)
                    inventory.delete_callbacks()

            self.activate_reroll()

    def _reroll_shop(self):
        if self.player_active.get_balance() >= self.reroll_price:
            self.player_active.lose_money(self.reroll_price)

            if self.player_active.get_balance() < self.reroll_price:
                self.reroll_but.desactivate()

            self.reroll_items()

            self.game.add_effect(
                SoundEffect(sound_path= SFX.CASH)
            )



    def open(self):
        self.game.add_object(self)
        self.reroll_items()
        self.player_active : Player = self.player1

        self.activate_reroll()
        self.close_but.update_text(['Next', 'Player'])
        self.close_but.on_release = self._next_player

    def _close(self):
        self.game.remove_object(self)
        self.case_area.clear()
        self.game.next_phase()

    def _next_player(self):
        self.player_active = self.player2
        self.reroll_items()
        self.activate_reroll()
        self.close_but.update_text(['Next', 'Game'])
        self.close_but.on_release = self._close

    def activate_reroll(self):
        if self.player_active.get_balance() >= self.reroll_price:
            self.reroll_but.activate() 
            if self.reroll_but.on_release is None:
                self.reroll_but.on_release = self._reroll_shop
        else:
            self.reroll_but.desactivate()


    def reroll_items(self):
        self.case_area.clear()
        for i in range(self.max_cases):
            case = generate_random_square()
            item = SquareItem(self.center + Vector2(i, 0), width= 100, height= 100, object= case)
            item.on_release = self._pay_item
            item.on_click = self._enable_pay_box
            self.case_area.add_item(item)


    def update(self, dt):
        self.case_area.update(dt)
    
    def handle_mouse(self, mouse_pos):
        self.case_area.handle_mouse(mouse_pos)
        self.reroll_but.handle_mouse(mouse_pos)
        self.close_but.handle_mouse(mouse_pos)
        

    def draw(self, screen):
        screen.blit(self.surface, self.rect)
        self.reroll_but.draw(screen)
        self.close_but.draw(screen)
