import pygame
from case import Case
from item import *
from item_area import *
from table import Table

class CaseInventory(ItemArea):
    def __init__(self, player, pos, max_items=5):

        self.player = player
        self.bg_surface = generate_nine_slice(InterfacesConfig.PLAYER_INV_WIDTH, InterfacesConfig.PLAYER_INV_HEIGHT, color = (0, 0, 255))
        self.bg_rect = self.bg_surface.get_rect(center = pos)

        screen_center = HEIGHT//2
        if pos[1] < screen_center:
            self.items_pos = pos[0], self.bg_rect.bottom - 80
        else:
            self.items_pos = pos[0], self.bg_rect.top + 80

        super().__init__(InterfacesConfig.PLAYER_INV_WIDTH -100, self.items_pos, max_items)

        self.table = None



    def draw(self, screen):
        screen.blit(self.bg_surface, self.bg_rect)
        return super().draw(screen)
    

    

    
        

