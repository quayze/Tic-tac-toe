import pygame
from square import Square
from item import *
from item_area import *
from table import Table

class CaseInventory(ItemArea):
    def __init__(self, player, pos, game, max_items=5):

        self.player = player
        color_theme = self.player.color_theme
        self.bg_surface = generate_nine_slice(InterfacesConfig.PLAYER_INV_WIDTH, InterfacesConfig.PLAYER_INV_HEIGHT, get_color('case_inv', color_theme))
        self.bg_rect = self.bg_surface.get_rect(center = pos)

        screen_center = HEIGHT//2
        if pos[1] < screen_center:
            self.items_pos = pos[0], self.bg_rect.bottom - 80
        else:
            self.items_pos = pos[0], self.bg_rect.top + 80

        super().__init__(InterfacesConfig.PLAYER_INV_WIDTH -100, self.items_pos, game, max_items)

        self.table = None

    def get_pos(self):
        return self.bg_rect.center
    
    def get_size(self):
        return self.bg_surface.get_size()



    def draw(self, screen):
        screen.blit(self.bg_surface, self.bg_rect)
    

    

    
        

