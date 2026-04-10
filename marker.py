import pygame
from functions import * 
from settings import *
from player import *
from moveable_object import *

class Marker(Moveable):
    def __init__(self, owner : Player, pos):
        self.base_surface = pygame.Surface((PIXEL_SIZE * MarkerConfig.MARKER_SIZE, PIXEL_SIZE * MarkerConfig.MARKER_SIZE), pygame.SRCALPHA).convert_alpha()
        super().__init__(pos, self.base_surface.get_width(), self.base_surface.get_height())
        self.size = 1
        self.scale_duration = 0
        
        self.owner = owner
        self.placed = False

        #rendu ui
        image = get_marker(self.owner.marker_type)
        self.image = pygame.transform.scale(image, self.base_surface.get_size())
        self.base_surface.blit(self.image, (0, 0))
        self.surface = self.base_surface.copy()


        self.shadow.set_image(self.image)


    def draw(self, surface : pygame.Surface):
        if self.handle_shadow: self.shadow.draw(surface)
        surface.blit(self.surface, self.rect)

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
        



    def update_scale(self, dt):
        if self.scale_duration > 0:

            progress = min(1, self.scale_time / self.scale_duration)
            self.size = self.base_size + (self.final_size - self.base_size) * ease_out_back(progress, s= 5)
            self.surface = resize(self.base_surface, self.size)
            self.rect = self.surface.get_rect(center = self.pos)
            self.scale_time += dt
            
            if progress >= 1:
                self.scale_duration = 0
                self.size = self.final_size
                self.surface = resize(self.base_surface, self.size)
                self.rect = self.surface.get_rect(center = self.pos)



    def juice(self, final_scale = 1, duration = 0.3):
        self.scale_duration = duration
        self.scale_time = 0
        self.final_size = final_scale
        self.base_size = self.size

    def get_placed(self):
        self.placed = True