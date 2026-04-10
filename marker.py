import pygame
from functions import * 
from settings import *
from player import *
from moveable_object import *

class Marker(Moveable):
    def __init__(self, owner : Player, pos):
        self.owner = owner

        surface = pygame.Surface((PIXEL_SIZE * MarkerConfig.MARKER_SIZE, PIXEL_SIZE * MarkerConfig.MARKER_SIZE), pygame.SRCALPHA).convert_alpha()
        image = get_marker(self.owner.marker_type)
        self.image = pygame.transform.scale(image, surface.get_size())
        surface.blit(self.image, (0, 0))

        super().__init__(pos, surface)
        
        self.placed = False

    def hover_trigger(self):
        self.juice(1.05)
        return super().hover_trigger()
    
    def not_hovering_trigger(self):
        self.juice(1)
        return super().not_hovering_trigger()
    
    def on_mouse_trigger(self):
        self.juice(1.2)
        return super().on_mouse_trigger()
    
    def on_realease_trigger(self):
        self.juice(1.05)
        return super().on_realease_trigger()

    def update(self, dt):
        super().update(dt)
        self.update_scale(dt)
        

    def get_placed(self):
        self.placed = True