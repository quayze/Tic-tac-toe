import pygame
from settings import *
from functions import *
from pygame import Vector2

class PopUp:
    def __init__(self, object, alignment = 'sides'):
        self.object = object
        self.render = True
        self.active = False
        self.alignment = alignment
        self.center = Vector2(WIDTH//2, HEIGHT //2)
        self.offset = 20

        self.surface = generate_nine_slice(200, 200)
        self.rect = self.surface.get_rect()

        self.object_pos = self.object.rect.center
        self.update_pos()


    def start_rendering(self):
        self.render = True
    def stop_rendering(self):
        self.render = False


    def update_pos(self):
        if self.alignment == 'sides':
            obj_rect : pygame.Rect = self.object.rect
            if obj_rect.centerx >= self.center.x:
                self.rect.midright = Vector2(obj_rect.midleft) + Vector2(-self.offset, 0)
            else:
                self.rect.midleft = Vector2(obj_rect.midright) + Vector2(self.offset, 0) 

        elif self.alignment == 'heights':
            obj_rect : pygame.Rect = self.object.rect
            if obj_rect.centery >= self.center.y:
                self.rect.midbottom = Vector2(obj_rect.midtop) + Vector2(0, -self.offset)
            else:
                self.rect.midtop = Vector2(obj_rect.midbottom) + Vector2(0, self.offset)


    

    def update(self, dt):
        if self.object_pos != self.object.rect.center:
            self.update_pos()
            self.object_pos = self.object.rect.center

    def handle_mouse(self, mouse_pos):
        if self.object.rect.collidepoint(mouse_pos):
            self.active = True
        elif self.active:
            self.active = False

    def draw(self, screen):
        if not self.active or not self.render:
            return
        screen.blit(self.surface, self.rect)