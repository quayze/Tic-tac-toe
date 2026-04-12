import pygame
from settings import *
from functions import *
from drawable import *
from pygame import Vector2 as V2
from button import *
from shadow import *
from effect import *

class Interface(Drawable):
    def __init__(self, game, base_pos, active_pos, width, height, color, center_color):
        super().__init__(1)
        self.state = 'disable'
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        self.rect = self.surface.get_rect(center = base_pos)
        self.surf_image = generate_nine_slice(width, height, color, center_color= center_color)
        self.game = game


        self.screen_center = V2(WIDTH//2, HEIGHT//2)
        self.center = V2(self.surface.get_width()//2, self.surface.get_height()//2)
        self.pos = V2(base_pos)
        self.base_pos = V2(base_pos)
        self.active_pos = V2(active_pos)

        self.shadow = Shadow(self.pos)
        self.shadow.set_image(self.surf_image)
        self.shadow.set_parallax(x_abs= 10, y_abs= 10)

        self.open_time = 0.5

        self.elements = {}

    def handle_mouse(self, mouse_pos):
        mouse_pos = V2(mouse_pos) - V2(self.rect.topleft)
        for element in self.elements.values():
            if hasattr(element, 'handle_mouse'):
                element.handle_mouse(mouse_pos)

    def update(self, dt):
        self.shadow.update(self.rect.center)
        self.update_opening(dt)
        self.update_closing(dt)
        for element in self.elements.values():
            element.update(dt)

    def draw(self, screen):
        self.shadow.draw(screen)
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(self.surf_image, (0, 0))
        for element in self.elements.values():
            element.draw(self.surface)
        screen.blit(self.surface, self.rect)

    def activate(self):
        if self.state == 'disable':
            self.state = 'open'
            self.game.add_object(self)
            self.start_pos = V2(self.pos)
            self.duration = self.open_time
            self.current_time = 0

    def desactivate(self):
        if self.state == "enable":
            self.state = 'close'
            self.start_pos = V2(self.pos)
            self.duration = self.open_time
            self.current_time = 0

    def update_opening(self, dt):
        if self.state == 'open':
            progression = self.current_time / self.duration
            self.pos = self.start_pos + (self.active_pos - self.start_pos) * ease_out_back(progression)
            self.current_time += dt

            self.rect.center = self.pos
            if progression >= 1:
                self.pos = V2(self.active_pos)
                self.rect.center = self.pos
                self.state = "enable"

    def update_closing(self, dt):
        if self.state == 'close':
            progression = self.current_time / self.duration
            self.pos = self.start_pos + (self.base_pos - self.start_pos) * progression
            self.current_time += dt

            self.rect.center = self.pos
            if progression >= 1:
                self.pos = V2(self.base_pos)
                self.rect.center = self.pos
                self.state = "disable"

    def add_element(self, name, element):
        if name not in self.elements:
            self.elements[name] = element

    def get_element(self, name):
        if name in self.elements:
            return self.elements[name]
        
    def is_closed(self):
        return self.state == 'disable'
    def is_open(self):
        return self.state == 'enable'



class GameInterface(Interface):
    def __init__(self, game):
        self.screen_center = V2(WIDTH//2, HEIGHT//2)
        super().__init__(game, (-300, self.screen_center.y), (200, self.screen_center.y), 600, 500, (255, 255, 255), (100, 0, 100))
        self.add_element('skip_button', Button((300, self.center.y), 250, 30, (255, 200, 0), ['Skip turn'], 30))


class PlayerInterface(Interface):
    def __init__(self, game, base_pos, active_pos):
        self.screen_center = V2(WIDTH//2, HEIGHT//2)
        super().__init__(game, base_pos, active_pos, 800, 600, (255, 255, 255), (100, 100, 100))
        self.add_element('play', Button((self.center.x, self.center.y), 250, 100, (0, 210, 80), ['Start'], 30, 4))
        self.add_element('back', Button((self.center.x, self.center.y + 200), 500, 80, (255, 210, 0), ['Back'], 30, 4))
        










    
    


    
