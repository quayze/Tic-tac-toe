import pygame
from settings import *
from marker import *
from marker_container import *
from player_balance import PlayerBalance
from square_inventory import SquareInventory
from item import *
from drawable import *
from interact_box import *

class PlayerInventory(Drawable):
    def __init__(self, player, game,  pos = 'bottom'):
        self.game = game
        super().__init__(4)
        if pos == 'bottom':
            self.pos_y = HEIGHT - InterfacesConfig.PLAYER_INV_OFFSET
            self.container_y = HEIGHT - InterfacesConfig.MAKER_CONTAINER_OFFSET
            self.x_offset = 1
        elif pos == 'top':
            self.pos_y = InterfacesConfig.PLAYER_INV_OFFSET
            self.container_y = InterfacesConfig.MAKER_CONTAINER_OFFSET
            self.x_offset = -1

        self.center_x = WIDTH // 2

        self.player = player

        self.marker_container = MarkerContainer(self.player, (self.center_x, self.container_y), self.game)
        self.player_balance = PlayerBalance(self.player, (self.center_x + 400*self.x_offset, self.pos_y))
        self.square_inventory = SquareInventory(self.player, (self.center_x - 500*self.x_offset, self.pos_y), self.game)

        self.init_pay_interface()

        self.game.add_object(self)

    def init_pay_interface(self):
        square_inventory_size = self.square_inventory.get_size()
        square_inv_pos = self.square_inventory.get_pos()
        items_pos = self.square_inventory.items_pos
        self.pay_square_surface = InteractiveBox(square_inventory_size[0], square_inventory_size[1], square_inv_pos, color= (0, 255, 0), 
                                        alpha= 150, text= 'BUY', text_pos= items_pos)
        self.game.add_object(self.pay_square_surface)

        p_balance_size = self.player_balance.rect.size
        p_balance_pos = self.player_balance.pos
        p_balance_txt_pos = self.player_balance.text_pos
        self.refund_surface = InteractiveBox(p_balance_size[0], p_balance_size[1], p_balance_pos, color= (255, 0, 0), 
                                        alpha= 150, text= 'REFUND', text_pos= p_balance_txt_pos)
        self.game.add_object(self.refund_surface)
        

    def handle_mouse(self, mouse_pos):
        self.marker_container.handle_mouse(mouse_pos)
        self.square_inventory.handle_mouse(mouse_pos)

    def update(self, dt):
        self.marker_container.update(dt)
        self.square_inventory.update(dt)
        self.player_balance.update(dt)

    def add_marker(self):
        self.marker_container.add_marker()

    def add_item(self, item : SquareItem):
        self.square_inventory.add_item(item)

    def can_add_item(self):
        return self.square_inventory.can_add()

    def set_release_callback(self, callback):
        self.marker_container.marker.on_release = callback

    def set_square_callback(self, callback):
        self.square_inventory.set_callback(callback)


    def marker_placed(self):
        return self.marker_container.placed

    def notify_placed(self):
        self.marker_container.marker = None
        self.marker_container.placed = True

    def square_placed(self):
        self.square_inventory.delete()

    def delete_callbacks(self):
        self.square_inventory.delete_callback()
        if self.marker_container.has_marker():
            self.marker_container.marker.on_release = None


    def draw(self, screen):
        self.marker_container.draw(screen)
        self.player_balance.draw(screen)
        self.square_inventory.draw(screen)


    

class GameSession:
    def __init__(self, player_1, player_2, game):
        self.players = [player_1, player_2]
        self.inventories = {
            player_1: PlayerInventory(player_1, game= game),
            player_2: PlayerInventory(player_2, pos='top', game= game)
        }

    def get_inventory(self, player):
        return self.inventories[player]
    
    def get_square_pay_surface(self, player):
        return self.inventories[player].pay_square_surface