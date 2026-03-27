import pygame
from settings import *
from functions import *
from player import Player

class PlayerBalance:
    def __init__(self, player : Player, pos):
        
        self.pos = pos
        self.player = player
        self.marker = None
        self.pos = pos
        self.placed = False
        color_theme = self.player.color_theme
        self.surface = generate_nine_slice(InterfacesConfig.PLAYER_BALANCE_WIDTH, InterfacesConfig.PLAYER_INV_HEIGHT, get_color('money_ui', color_theme))
        self.rect = self.surface.get_rect(center = pos)

        screen_center = HEIGHT//2
        if self.pos[1] < screen_center:
            self.text_pos = self.pos[0], self.rect.bottom - 80
        else:
            self.text_pos = self.pos[0], self.rect.top + 80

        self.update_text()

    def update_text(self):
        self.current_balance = self.player.get_balance()
        self.money_text = f'{self.current_balance} $'
        self.money_surface = get_text_surface(self.money_text, size= 100, color= (255, 255, 255))
        self.money_rect = self.money_surface.get_rect(center = self.text_pos)

    def update(self, dt):
        if self.current_balance != self.player.get_balance():
            self.update_text()

    
    def draw(self, screen):
        screen.blit(self.surface, self.rect)
        screen.blit(self.money_surface, self.money_rect)