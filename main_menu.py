import pygame
from settings import *
from functions import *
from drawable import *
from pygame import Vector2 as V2
from button import *
from shadow import *
from effect import *
from interface import *


class MainMenu(Drawable):
    def __init__(self, game):
        super().__init__(1)
        self.game = game
        self.center = V2(WIDTH//2, HEIGHT//2)
        self.play_button = Button((self.center.x, self.center.y + 200), 400, 200, color= (0, 210, 80), text= ['PLAY'])
        self.state = 'main'

        self.settings = {'player_1_color' : 'red', 'player_2_color' : 'blue',
                          'player_1_marker' : 'cross', 'player_2_marker' : 'round'}
        
        self.player_interface_1 = PlayerInterface(self.game, (self.center.x, 2600), (self.center.x, self.center.y))

    def open(self):
        self.game.add_object(self)
        self.play_button.on_release = self._open_play_interface
        
        play_but = self.player_interface_1.get_element('play')
        play_but.on_release = self._play

        back_but = self.player_interface_1.get_element('back')
        back_but.on_release = self._back

    
    def close(self):
        self.game.remove_object(self)
        self.play_button.delete_callbacks()

    def update(self, dt):
        self.player_interface_1.update(dt)

    def draw(self, screen):
        self.play_button.draw(screen)
    
    def handle_mouse(self, mouse_pos):
        if self.state == 'main':
            self.play_button.handle_mouse(mouse_pos)
        elif self.state == 'pre_game':
            self.player_interface_1.handle_mouse(mouse_pos)

    def _open_play_interface(self):
        if self.player_interface_1.is_closed():
            self.player_interface_1.activate()
            self.state = 'pre_game'

    def _back(self):
        if self.player_interface_1.is_open():
            self.player_interface_1.desactivate()
            self.state = 'main'

    def _play(self):
        self.close()
        self.game.new_run()