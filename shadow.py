import pygame
from settings import *

class Shadow:
    def __init__(self, object_pos):

        self.image = None
        
        self.object_pos = object_pos

        self.anchor_pos = WIDTH//2, HEIGHT

        self.x_mult = None
        self.y_mult = None
        self.x_abs = 0
        self.y_abs = 0

        self.get_pos()

    def set_image(self, image):
        self.image : pygame.Surface = image.copy()
        self.image.fill((0, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.image.set_alpha(100)
        self.rect = self.image.get_rect()
        self.get_pos()


    def get_pos(self):
        pos_x, pos_y = self.object_pos
        center_x, center_y = self.anchor_pos
        offset_x = center_x - pos_x
        offset_y = center_y - pos_y


        if self.x_mult is not None:
            x_parallax =  offset_x * self.x_mult
        else:
            x_parallax = self.x_abs

        if self.y_mult is not None:
            y_parallax = offset_y * self.y_mult
        else:
            y_parallax = self.y_abs

        self.pos = pos_x + x_parallax, pos_y + y_parallax

        self.image_pos()

    def image_pos(self):
        if self.image is not None:
            self.rect.center = self.pos

    def draw(self, surface):
        surface.blit(self.image, self.rect)


        
    
    def update(self, object_pos):
        if object_pos != self.object_pos:
            self.object_pos = object_pos
            self.get_pos()

    def set_parallax(self, x_mult = None, y_mult = None, x_abs = 0, y_abs = 0):
        self.x_mult = x_mult
        self.y_mult = y_mult
        self.x_abs = x_abs
        self.y_abs = y_abs
        self.get_pos()


    def obtain_pos(self):
        return self.pos
