import pygame
from pygame import Vector2
from functions import *
from shadow import *

class Moveable:
    def __init__(self, pos, width, height):
        self.rect = pygame.rect.Rect((0, 0, width, height))
        self.rect.center = pos
        self.pos = Vector2(pos)
        self.hold = False

        self.can_move = True
        self.anchor : Vector2 = None
        self.anchor_reach = True

        self.state = 'idle' #idle, hover, on_mouse

        self.on_release = None

        self.shadow = Shadow(self.pos)

    def handle_mouse(self, mouse_pos):
        if not self.can_move:
            return
        mouse_but = pygame.mouse.get_pressed()
        self.move_to_mouse(mouse_pos)

        if mouse_but[0] and not self.rect.collidepoint(mouse_pos):
            self.hold = True

        elif not mouse_but[0]:
            self.hold = False

        if self.hold:
            return


        if self.rect.collidepoint(mouse_pos) and not self.state == 'on_mouse':
            self.state = 'hover'

        if mouse_but[0] and self.state == 'hover':
            self.offset = Vector2(mouse_pos) - self.pos
            self.shadow.set_offset("strong")
            self.state = 'on_mouse'

        if not mouse_but[0] and self.state == 'on_mouse':
            self.state = 'hover'
            self.shadow.set_offset()
            self.get_direction_to_anchor()
            if self.on_release:
                self.on_release()
            

        if not self.rect.collidepoint(mouse_pos) and self.state == 'hover':
            self.state = 'idle'

    def get_direction_to_anchor(self):
        if self.anchor is None:
            return
        direction = self.anchor - self.pos
        if direction.length() > 0:
            self.anchor_reach = False
            self.direction = direction.normalize()
        
    def move_to_mouse(self, mouse_pos):
        if self.state == 'on_mouse':
            self.pos = Vector2(mouse_pos) - self.offset
            self.rect.center = self.pos

    def update_pos(self, dt):
        if self.state == 'on_mouse' or self.anchor is None or self.anchor_reach:
            return
        distance = self.pos.distance_to(self.anchor)
        speed = 100 + distance*7
        self.pos += self.direction * speed * dt
        if self.pos.distance_to(self.anchor) <= speed * dt:
            self.pos = self.anchor
            self.anchor_reach = True
        self.rect.center = self.pos

    def set_anchor(self, pos : tuple):
        self.anchor = Vector2(pos)
        self.get_direction_to_anchor()

    def stop_reacting_to_mouse(self):
        self.can_move = False
        self.state = 'idle'

    def update(self, dt):
        self.update_pos(dt)
        self.shadow.update(self.rect.center)



    def set_pos(self, pos):
        self.pos = pos
        self.rect.center = pos

    def get_pos(self):
        return self.pos
    
    def get_anchor(self):
        return self.anchor
    
