import pygame
from settings import *
from marker import *
from marker_container import *
from player_balance import PlayerBalance
from case_inventory import CaseInventory
from item import *
from drawable import *

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
        self.player_balance = PlayerBalance(self.player, (self.center_x + 500*self.x_offset, self.pos_y))
        self.case_inventory = CaseInventory(self.player, (self.center_x - 500*self.x_offset, self.pos_y), self.game)

        self.game.add_object(self)

    def handle_mouse(self, mouse_pos):
        self.marker_container.handle_mouse(mouse_pos)
        self.case_inventory.handle_mouse(mouse_pos)

    def update(self, dt):
        self.marker_container.update(dt)
        self.case_inventory.update(dt)
        self.player_balance.update(dt)

    def add_marker(self):
        self.marker_container.add_marker()

    def add_item(self, item : SquareItem):
        self.case_inventory.add_item(item)

    def can_add_item(self):
        return self.case_inventory.can_add()

    def set_release_callback(self, callback):
        self.marker_container.marker.on_release = callback

    def set_case_callback(self, callback):
        self.case_inventory.set_callback(callback)


    def marker_placed(self):
        return self.marker_container.placed

    def notify_placed(self):
        self.marker_container.marker = None
        self.marker_container.placed = True

    def case_placed(self):
        self.case_inventory.delete()

    def delete_callbacks(self):
        self.case_inventory.delete_callback()
        if self.marker_container.has_marker():
            self.marker_container.marker.on_release = None


    def draw(self, screen):
        self.marker_container.draw(screen)
        self.player_balance.draw(screen)
        self.case_inventory.draw(screen)


    

class GameSession:
    def __init__(self, player_1, player_2, game):
        self.players = [player_1, player_2]
        self.inventories = {
            player_1: PlayerInventory(player_1, game= game),
            player_2: PlayerInventory(player_2, pos='top', game= game)
        }

    def get_inventory(self, player):
        return self.inventories[player]