import pygame
from functions import * 
from settings import *
from player import *
from moveable_object import *

class Item(Moveable):
    def __init__(self, pos, width, height, object, negative = False):
        self.object = object
        self.image = self.object.image.copy()
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        super().__init__(pos, self.surface.get_width(), self.surface.get_height())
        self.image = pygame.transform.scale(self.image, self.surface.get_size())
        self.surface.blit(self.image, (0, 0))

        self.shadow.set_image(self.image)

        self.negative = negative


    def draw(self, surface : pygame.Surface):
        self.shadow.draw(surface)
        surface.blit(self.surface, self.rect)
        

    def get_rect(self):
        return self.rect
    
    def get_object(self):
        return self.object
    

