import pygame
from settings import *
from functions import *
from drawable import *
from pygame import Vector2 as V2
from button import *
from shadow import *
from effect import *
from interface import *
from effect_group import *
from square import *


class MainMenu(Drawable):
    def __init__(self, game):
        super().__init__(1)
        self.game = game
        self.center = V2(WIDTH//2, HEIGHT//2)
        self.play_button = Button((self.center.x, self.center.y + 130), 500, 130, color= (0, 150, 70), text= ['PLAY'])
        self.settings_button = Button((self.center.x, self.center.y + 280), 500, 130, color= (150, 150, 150), text= ['SETTINGS'])
        self.quit_button = Button((self.center.x, self.center.y + 430), 500, 130, color= (150, 0, 0), text= ['QUIT'])
        self.state = 'main'

        self.settings = {'p1_color' : 'red', 'p2_color' : 'blue',
                          'p1_marker' : 'cross', 'p2_marker' : 'round'}
        
        self.play_interface = PlayInterface(self.game, (self.center.x, 2600), (self.center.x, self.center.y), 11)

        self.effects_group = EffectGroup()

        self.squares = []

        self.add_squares()

    def add_squares(self):
        
        self.squares.append(MoveableSquare("DeathSquare", size= 10, pos= (600, 230)))
        self.squares.append(MoveableSquare("SideSquare", size= 10, pos= (400, 500)))
        self.squares.append(MoveableSquare("YinYangSquare", size= 10, pos= (200, 270)))
        self.squares.append(MoveableSquare("BurningSquare", size= 10, pos= (300, 800)))

        self.squares.append(MoveableSquare("ReplaySquare", size= 10, pos= (1400, 600)))
        self.squares.append(MoveableSquare("MoneySquare", size= 10, pos= (1500, 200)))
        self.squares.append(MoveableSquare("RandomSquare", size= 10, pos= (1700, 750)))

        self.squares.append(MoveableSquare("DefaultSquare", size= 15, pos= (960, 350)))

    def open(self):
        self.game.add_object(self)
        self.play_button.on_release = self._open_play_interface
        self.quit_button.on_release = self._quit_game

        
        play_but = self.play_interface.get_element('play')
        play_but.on_release = self._play

        back_but = self.play_interface.get_element('back')
        back_but.on_release = self._back

        for square in self.squares:
            self.game.add_object(square)

    
    def close(self):
        self.game.remove_object(self)
        self.play_button.delete_callbacks()

        for square in self.squares:
            self.game.remove_object(square)

    def update(self, dt):
        self.play_interface.update(dt)
        for square in self.squares:
            square.update(dt)
        

    def draw(self, screen):
        self.play_button.draw(screen)
        self.quit_button.draw(screen)
        self.settings_button.draw(screen)
    
    def handle_mouse(self, mouse_pos):
        if self.state == 'main':
            self.play_button.handle_mouse(mouse_pos)
            self.quit_button.handle_mouse(mouse_pos)
            self.settings_button.handle_mouse(mouse_pos)
            for square in self.squares:
                square.handle_mouse(mouse_pos)
        elif self.state == 'pre_game':
            self.play_interface.handle_mouse(mouse_pos)

    def _open_play_interface(self):
        if self.play_interface.is_closed():
            self.play_interface.activate()
            self.state = 'pre_game'

    def _back(self):
        if self.play_interface.is_open():
            self.play_interface.desactivate()
            self.state = 'main'

    def _play(self):
        if not self.change_settings():
            return

    
        self.close()
        self.game.create_players(p1_marker =  self.settings['p1_marker'], 
                                 p1_theme = self.settings['p1_color'], 
                                 p2_marker =  self.settings['p2_marker'], 
                                 p2_theme =  self.settings['p2_color'])
        self.game.new_run()

    def _quit_game(self):
        self.game.quit()

    def change_settings(self):
        self.settings['p1_marker'] = self.play_interface.get_p1_marker()
        self.settings['p2_marker'] = self.play_interface.get_p2_marker()

        self.settings['p1_color'] = self.play_interface.get_p1_color()
        self.settings['p2_color'] = self.play_interface.get_p2_color()

        if self.settings['p1_marker'] == self.settings['p2_marker']:
            text = get_text_surface("Players must have different markers")
            self.effects_group.add_effect(ParticleEffect(self.center, 1, text, GrowParticle, 
                                                         kill_duration= 0.5, death_effect= ScaleDeath, scale= 0.7), self.game)
            return False
        
        if self.settings['p1_color'] == self.settings['p2_color']:
            text = get_text_surface("Players must have different color themes")
            self.effects_group.add_effect(ParticleEffect(self.center, 1, text, GrowParticle, 
                                                         kill_duration= 0.5, death_effect= ScaleDeath, scale= 0.7), self.game)
            return False
        
        return True
    
