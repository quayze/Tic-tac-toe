import pygame
from functions import * 
from settings import *
from player import *
from moveable_object import *

class Marker(Moveable):
    def __init__(self, owner : Player, pos):
        self.surface = pygame.Surface((PIXEL_SIZE * MarkerConfig.MARKER_SIZE, PIXEL_SIZE * MarkerConfig.MARKER_SIZE), pygame.SRCALPHA).convert_alpha()
        super().__init__(pos, self.surface.get_width(), self.surface.get_height())

        
        self.owner = owner
        self.placed = False

        #rendu ui
        image = get_marker(self.owner.marker_type)
        self.image = pygame.transform.scale(image, self.surface.get_size())
        self.surface.blit(self.image, (0, 0))

        self.shadow.set_image(self.image)


    def draw(self, surface : pygame.Surface):
        if self.handle_shadow: self.shadow.draw(surface)
        surface.blit(self.surface, self.rect)
        

    def get_placed(self):
        self.placed = True

    def juice_up(self, size, rot, t):
        pass




