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
        self.shadow.draw(surface)
        surface.blit(self.surface, self.rect)
        

    def get_placed(self):
        self.placed = True

    def juice_up(self, size, rot, t):
        pass
    





#recupère une image en fonction d'un type
def get_marker(marker_type):
    markers = load_image('marker', MarkerConfig.MARKERS_SHEET)
    if marker_type == 'cross':
        return get_image(markers, MarkerConfig.MARKER_SIZE, MarkerConfig.MARKER_SIZE)
    
    elif marker_type == 'round':
        return get_image(markers, MarkerConfig.MARKER_SIZE, MarkerConfig.MARKER_SIZE, frame_x= 1)
    
    elif marker_type == 'donut':
        return get_image(markers, MarkerConfig.MARKER_SIZE, MarkerConfig.MARKER_SIZE, frame_x= 2)
    
    elif marker_type == 'nugget_guy':
        return get_image(markers, MarkerConfig.MARKER_SIZE, MarkerConfig.MARKER_SIZE, frame_x= 3)