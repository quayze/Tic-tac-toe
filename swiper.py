import pygame
from settings import *
from functions import *
from drawable import *
from pygame import Vector2 as V2
from button import *
from shadow import *
from effect import *


class Swiper:
    def __init__(self, pos, button_color = (220, 30, 30)):
        self.pos = V2(pos)
        self.elements = {}
        self.button_color = button_color

        


    def _swipe_right(self):
        
        el_list = list(self.elements.keys())
        index = el_list.index(self.current_element)
        index += 1
        if index >= len(el_list):
            index = 0

        self.current_element = el_list[index]

    def _swipe_left(self):
        el_list = list(self.elements.keys())
        index = el_list.index(self.current_element)
        index -= 1
        if index < 0:
            index = len(el_list) -1

        self.current_element = el_list[index]
        self.current_element

    def draw(self, surface : pygame.Surface):
        self.button_left.draw(surface)
        self.button_right.draw(surface)
        self.elements[self.current_element].draw(surface)

    def update(self, dt):
        pass

    def handle_mouse(self, mouse_pos):
        self.button_left.handle_mouse(mouse_pos)
        self.button_right.handle_mouse(mouse_pos)


    def add_element(self, name, element):
        if name not in self.elements:
            self.elements[name] = element
            element.rect.center = self.pos
            if len(self.elements) == 1:
                self.current_element = name
                self.create_buttons(element)

    
    def create_buttons(self, element):
        height = element.rect.height
        left = element.rect.left
        right = element.rect.right
        self.button_left = Button((left - 60, self.pos.y), 50, height, color= self.button_color, text= ['<'], pixel_size= 4)
        self.button_right = Button((right + 60, self.pos.y), 50, height, color= self.button_color, text= ['>'], pixel_size= 4)

        self.button_left.on_release = self._swipe_left
        self.button_right.on_release = self._swipe_right





    def get_active(self):
        return self.elements[self.current_element]
    
    def get_active_name(self):
        return self.current_element
    

class SwiperImage:
    def __init__(self, image, size):
        self.image = image
        self.image = resize(self.image, size)
        self.rect = self.image.get_rect()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        
