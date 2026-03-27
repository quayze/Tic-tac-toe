from player import Player
from marker import Marker
from settings import *
from functions import *
from table import Table
from case import Case

class MarkerContainer:
    def __init__(self, player : Player, pos, color):
        
        self.pos = pos
        self.player = player
        self.marker = None
        self.pos = pos
        self.placed = False
        self.surface = generate_nine_slice(InterfacesConfig.MARKER_CONTAINER_WIDTH, InterfacesConfig.PLAYER_INV_HEIGHT, color)
        self.rect = self.surface.get_rect(center = pos)

        screen_center = HEIGHT//2
        if self.pos[1] < screen_center:
            self.object_pos = self.pos[0], self.rect.bottom - 80
        else:
            self.object_pos = self.pos[0], self.rect.top + 80

    def add_marker(self):
        self.marker = Marker(self.player, self.object_pos)
        self.marker.set_anchor(self.object_pos)
        self.placed = False



    def handle_mouse(self, mouse_pos):
        if self.marker is None:
            return
        self.marker.handle_mouse(mouse_pos)

    def update(self, dt):
        if self.marker is None:
            return
        self.marker.update(dt)
    
    def draw(self, screen):
        screen.blit(self.surface, self.rect)
        if self.marker is None:
            return
        self.marker.draw(screen)

    def marker_placed(self):
        return self.placed == True
    
    def has_marker(self):
        return self.marker is not None


