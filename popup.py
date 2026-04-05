import pygame
from settings import *
from functions import *
from pygame import Vector2

class PopUp:
    def __init__(self, object, alignment = 'top', width = 500):
        self.object = object
        self.render = False
        self.alignment = alignment
        self.center = Vector2(WIDTH//2, HEIGHT //2)
        self.offset = 20
        self.offset_betwenn_el = 15
        self.width = width
        self.height = 200

        self.border_offset = NineSliceConfig.PIXEL_SIZE * 2
        self.update_surface()

        self.center_width = self.rect.width - 2 * self.border_offset

        self.object_pos = self.object.rect.center
        self.update_pos()

        self.elements : list[PopupElement] = []


    def open(self):
        self.render = True

    def close(self):
        self.render = False

    def update_surface(self):
        self.image = generate_nine_slice(self.width, self.height, center_color= (120, 120, 120))
        self.surface = pygame.Surface((self.image.get_width(), self.image.get_height()), pygame.SRCALPHA).convert_alpha()
        self.rect = self.surface.get_rect()
        self.update_pos()



    def update_pos(self):
        obj_rect : pygame.Rect = self.object.rect
        if self.alignment == 'left':
            self.rect.midright = Vector2(obj_rect.midleft) + Vector2(-self.offset, 0)
        elif self.alignment == 'right':
            self.rect.midleft = Vector2(obj_rect.midright) + Vector2(self.offset, 0) 

        elif self.alignment == 'top':
            self.rect.midbottom = Vector2(obj_rect.midtop) + Vector2(0, -self.offset)
        elif self.alignment == 'bottom':
            self.rect.midtop = Vector2(obj_rect.midbottom) + Vector2(0, self.offset)

    def add_text(self, text, bg_color = (255, 255, 255)):
        element = PopupText(self.center_width, 
                                       mid_pos= (self.get_next_pos()), text=text, bg_color = bg_color)
        self.elements.append(element)

        self.set_height(element)
        
    def add_title(self, text):
        if self.elements != []:
            return
        
        element = PopupTitle(self.center_width, 
                                       mid_pos= (self.get_next_pos()), text=text)
        self.elements.append(element)

        max_width = self.width - 2*self.border_offset - 30
        if element.rect.width > max_width:
            self.width = element.rect.width + 2*self.border_offset + 30
            self.update_surface()
            element.change_pos((self.rect.width // 2, self.border_offset + self.offset_betwenn_el))
            self.center_width = self.rect.width - 2 * self.border_offset

        self.set_height(element)

    def set_height(self, element):
        max_pos = self.height - self.border_offset - self.offset_betwenn_el
        if element.get_bottom_rect() > max_pos:
            self.height = element.get_bottom_rect() + self.border_offset + self.offset_betwenn_el
            self.update_surface()
        

        
        

    def get_next_pos(self):
        if self.elements == []:
            return self.rect.width // 2, self.border_offset + self.offset_betwenn_el
        else:
            return self.rect.width // 2, self.elements[-1].get_bottom_rect() + self.offset_betwenn_el
    

    def update(self, dt):
        if self.object_pos != self.object.rect.center:
            self.update_pos()
            self.object_pos = self.object.rect.center

    def draw(self, screen):
        if not self.render:
            return
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(self.image, (0, 0))
        for element in self.elements:
            element.draw(self.surface)
        screen.blit(self.surface, self.rect)


class PopupElement:
    def __init__(self, popup_width, mid_pos, surface):
        self.popup_width = popup_width
        self.surface = surface
        self.rect = self.surface.get_rect(midtop = mid_pos)

    def draw(self, popup):
        popup.blit(self.surface, self.rect)

    def get_bottom_rect(self):
        return self.rect.bottom
    
    def change_pos(self, pos):
        self.rect.midtop = pos

class PopupText(PopupElement):
    def __init__(self, popup_width, mid_pos, text, bg_color = (255, 255, 255)):
        
        width = popup_width - 20
        offset = 10
        text_surface = get_warp_text(text, PopupConfig.TEXT_SIZE, width, (0, 0, 0))
        text_rect = text_surface.get_rect(midtop = (width//2, offset))
        surface = generate_nine_slice(width, text_surface.get_height()+ offset*2, pixel_size= 3, color= bg_color)
        surface.blit(text_surface, text_rect)

        super().__init__(popup_width, mid_pos, surface)

class PopupTitle(PopupElement):
    def __init__(self, popup_width, mid_pos, text):
        
        surface = get_text_surface(text, PopupConfig.TITLE_SIZE)
        super().__init__(popup_width, mid_pos, surface)


        