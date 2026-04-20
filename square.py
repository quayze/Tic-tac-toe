import pygame, ast
from settings import * 
from marker import Marker
from pygame import Vector2
from functions import * 
from moveable_object import *

class Square:
    def __init__(self, pos = (0, 0)):
        self.pos = Vector2(pos)
        self.surface = pygame.Surface((PIXEL_SIZE * SquareConfig.CASE_SIZE, PIXEL_SIZE * SquareConfig.CASE_SIZE), pygame.SRCALPHA).convert_alpha()
        self.rect = self.surface.get_rect(center = pos)
        self.marker = None
        
        #-----------------------------------
        # interaction attributes
        #-----------------------------------
        self.blueprint = True
        self.counting = True
        self.placable = [DefaultSquare]
        #-----------------------------------
        # data
        #-----------------------------------
        data = get_square_data(type(self).__name__)
        self.name = data['name']
        self.description = data['description']
        self.rarity = data['rarity']
        self.image_coord = ast.literal_eval(data['image'])
        self.get_image(*self.image_coord)



    def place_marker(self, marker : Marker):
        if marker is None : return
        self.marker : Marker = marker
        self.marker.get_placed()
        self.marker.set_anchor(self.pos)
        self.marker.set_shadow_parallax(y_abs= 20)

    def get_image(self, frame_x = 0, frame_y = 0):
        sprite_sheet = load_image('squares', SquareConfig.CASE_SHEET)
        image = get_image(sprite_sheet, SquareConfig.CASE_SIZE, SquareConfig.CASE_SIZE, frame_x, frame_y)
        self.image = image

    def blit_image(self):
        resized_image = pygame.transform.scale(self.image, self.surface.get_size())
        self.surface.blit(resized_image, (0, 0))

    def draw(self, screen):
        screen.blit(self.surface , self.rect)

    def update(self, dt):
        if self.marker is None:
            return
        self.marker.update(dt)

    def get_marker(self):
        return self.marker
    
    def remove_marker(self):
        if self.marker is not None:
            self.marker.kill()
            self.marker = None

    def get_pos(self):
        return self.pos
    
    def in_surroundings(self, pos : tuple):
        return self.rect.collidepoint(pos)
    
    def get_owner(self):
        if self.marker is None:
            return None
        else:
            return self.marker.owner
    
    def can_place(self):
        return self.marker is None
    
    def set_marker(self, marker=None):
        self.marker = marker

    def has_marker(self):
        return self.marker != None
        

    def set_pos(self, pos):
        self.pos = pos
        self.rect.center = pos

    def copy_attributes(self, square):
        pass

    def trigger_effect(self, context):
        return context

#----------------------------------------------
# DEFAULT SQUARE
#----------------------------------------------    

class DefaultSquare(Square):
    """Base case functionning"""
    def __init__(self, pos = (0, 0)):
        super().__init__(pos)
        self.get_image()
        self.blit_image()

    def trigger_effect(self, context):
        return context
        


class MoveableSquare(Moveable):
    def __init__(self, name, size, pos):
        image = get_square(name)
        image = resize(image, size)
        super().__init__(pos, image)
        self.set_anchor(pos)

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