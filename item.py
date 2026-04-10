import pygame
from functions import * 
from settings import *
from player import *
from moveable_object import *
from popup import *

class Item(Moveable):
    def __init__(self, pos, width, height, object, negative = False):
        self.object = object
        self.image = self.object.image.copy()
        surface = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        self.image = pygame.transform.scale(self.image, surface.get_size())
        surface.blit(self.image, (0, 0))

        super().__init__(pos, surface)

        self.negative = negative
        
    def draw(self, surface : pygame.Surface):
        self.shadow.draw(surface)
        surface.blit(self.surface, self.rect)
        

    def get_rect(self):
        return self.rect
    
    def get_object(self):
        return self.object
    
    def hover_trigger(self):
        self.juice(1.05)
        super().hover_trigger()
    
    def not_hovering_trigger(self):
        self.juice(1)
        super().not_hovering_trigger()
    
    def on_mouse_trigger(self):
        self.juice(1.2)
        super().on_mouse_trigger()
    
    def on_realease_trigger(self):
        self.juice(1.05)
        super().on_realease_trigger()

    def update(self, dt):
        super().update(dt)
        self.update_scale(dt)
        

    

class SquareItem(Item):
    def __init__(self, pos, width, height, object, negative=False):
        super().__init__(pos, width, height, object, negative)
        self.popup = PopUp(self, 'top')
        self.popup.add_title(self.object.name)
        self.popup.add_text(self.object.description)
        self.popup.add_text(self.object.rarity.upper(), SquareConfig.RARITY_COLORS[self.object.rarity], (255, 255, 255))
        self.price = SquareConfig.BUY_PRICE[self.object.rarity]
        self.sell_price = SquareConfig.SELL_PRICE[self.object.rarity]

    def hover_trigger(self):
        super().hover_trigger()
        self.popup.open()

    def not_hovering_trigger(self):
        super().not_hovering_trigger()
        self.popup.close()

    def on_mouse_trigger(self):
        super().on_mouse_trigger()
        self.popup.close()
    
    def on_realease_trigger(self):
        super().on_realease_trigger()
        self.popup.open()

    
    def draw(self, screen):
        super().draw(screen)
        self.popup.draw(screen)
    
    def update(self, dt):
        self.popup.update(dt)
        return super().update(dt)

