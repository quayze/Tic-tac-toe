import pygame
from settings import *

class Shadow:
    def __init__(self, object_pos):

        self.image = None
        
        self.object_pos = object_pos

        self.offset = 'default' # default, strong, minimal

        self.get_pos()

    def set_image(self, image):
        self.image : pygame.Surface = image.copy()
        self.image.fill((0, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.image.set_alpha(100)
        self.rect = self.image.get_rect()
        self.get_pos()


    def get_pos(self):
        pos_x, pos_y = self.object_pos
        center_x = WIDTH//2
        center_y = HEIGHT
        offset_x = center_x - pos_x
        offset_y = center_y - pos_y

        if self.offset == 'default':
            self.pos = pos_x + offset_x * 0.05 , pos_y + 20
        elif self.offset == 'strong':
            self.pos = pos_x + offset_x * 0.2 , pos_y + 60
        elif self.offset == 'minimal':
            self.pos = pos_x + offset_x * 0.01 , pos_y + 10
        elif self.offset == 'bottom':
            self.pos = pos_x , pos_y + 10

        self.image_pos()

    def image_pos(self):
        if self.image is not None:
            self.rect.center = self.pos

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self, object_pos):
        if object_pos != self.object_pos:
            self.object_pos = object_pos
            self.get_pos()


    def set_offset(self, offset = 'default'):
        self.offset = offset
        self.get_pos()


    def obtain_pos(self):
        return self.pos
