import pygame
from settings import *
from functions import *
from player import Player
from text import *

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

        self.shadow = Shadow(self.pos)
        self.shadow.set_image(self.surface)
        self.shadow.set_parallax(x_mult= 0.02, y_abs= 10)

        

        screen_center = HEIGHT//2
        if self.pos[1] < screen_center:
            self.text_pos = self.pos[0], self.rect.bottom - 80
        else:
            self.text_pos = self.pos[0], self.rect.top + 80

        self.text = AnimText('0', 100, self.text_pos)

        self.update_text()

    def update_text(self):
        self.current_balance = self.player.get_balance()
        self.money_text = f'{self.current_balance}'
        self.text.change_text(self.money_text)
        self.text.start()

    def update(self, dt):
        self.text.update(dt)
        if self.current_balance != self.player.get_balance():
            self.update_text()

    
    def draw(self, screen):
        self.shadow.draw(screen)
        screen.blit(self.surface, self.rect)
        self.text.draw(screen)