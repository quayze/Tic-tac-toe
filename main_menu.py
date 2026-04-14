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


class MainMenu(Drawable):
    def __init__(self, game):
        super().__init__(1)
        self.game = game
        self.center = V2(WIDTH//2, HEIGHT//2)
        self.play_button = Button((self.center.x, self.center.y + 200), 400, 200, color= (0, 150, 70), text= ['PLAY'])
        self.state = 'main'

        self.settings = {'p1_color' : 'red', 'p2_color' : 'blue',
                          'p1_marker' : 'cross', 'p2_marker' : 'round'}
        
        self.play_interface = PlayInterface(self.game, (self.center.x, 2600), (self.center.x, self.center.y))

        self.effects_group = EffectGroup()

    def open(self):
        self.game.add_object(self)
        self.play_button.on_release = self._open_play_interface
        
        play_but = self.play_interface.get_element('play')
        play_but.on_release = self._play

        back_but = self.play_interface.get_element('back')
        back_but.on_release = self._back

    
    def close(self):
        self.game.remove_object(self)
        self.play_button.delete_callbacks()

    def update(self, dt):
        self.play_interface.update(dt)

    def draw(self, screen):
        self.play_button.draw(screen)
    
    def handle_mouse(self, mouse_pos):
        if self.state == 'main':
            self.play_button.handle_mouse(mouse_pos)
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