import pygame
from functions import *
from drawable import *
from pygame import Vector2

class InteractiveBox(Drawable):
    def __init__(self, width, height, pos, color = (255, 255, 255), alpha = 255, text = None, text_size = 100, text_pos = None):
        super().__init__(z = 30)
        self.pos = pos
        self.surface = generate_nine_slice(width, height, center_color= color, center_alpha= alpha)
        self.rect = self.surface.get_rect(center = pos)
        self.active = False
        self.on_collision = None
        self.text_size = text_size
        self.text_pos = text_pos
        self.update_text(text)

    def update_text(self, text = None):
        if text is not None:
            self.text = get_text_surface(text, self.text_size)
            text_pos = self.text_pos if self.text_pos is not None else self.pos
            self.text_rect = self.text.get_rect(center = text_pos)



    def collision(self, rect):
        if self.rect.colliderect(rect):
            if self.on_collision:
                self.on_collision()
            return True
        else:
            return False
        
    def draw(self, screen):
        if self.active:
            screen.blit(self.surface, self.rect)
            if self.text is None:
                return
            screen.blit(self.text, self.text_rect)

    def activate(self):
        self.active = True

    def desactivate(self):
        self.active = False
        