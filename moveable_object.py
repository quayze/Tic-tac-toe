import pygame
from pygame import Vector2
from functions import *
from shadow import *
from drawable import *

class Moveable(Drawable):
    def __init__(self, pos, surface : pygame.Surface):
        self.base_z = 10
        super().__init__(z = self.base_z)

        self.pos = Vector2(pos)
        self.base_surface = surface
        self.surface = self.base_surface.copy()
        self.rect = self.surface.get_rect(center = pos)
        

        self.hold = False
        self.can_move = True
        self.anchor : Vector2 = None
        self.anchor_reach = True

        self.move = False

        self.state = 'idle' #idle, hover, on_mouse

        self.shadow = Shadow(self.pos)
        self.shadow.set_parallax(**ShadowConfig.DEFAULT)
        self.shadow.set_image(self.surface)
        self.handle_shadow = True

        #----------------------
        # CALLBACKS
        #----------------------
        self.on_release = None
        self.on_click = None

        #----------------------
        # JUICE
        #----------------------
        self.size = 1
        self.scale_duration = 0

    def handle_mouse(self, mouse_pos):
        if not self.can_move or self.move:
            return
        mouse_but = pygame.mouse.get_pressed()
        self.move_to_mouse(mouse_pos)

        if mouse_but[0] and not self.rect.collidepoint(mouse_pos):
            self.hold = True

        elif not mouse_but[0]:
            self.hold = False

        if self.hold:
            return

        if self.rect.collidepoint(mouse_pos) and not self.state == 'on_mouse' and not self.state == 'hover':
            self.state = 'hover'
            self.hover_trigger()

        if mouse_but[0] and self.state == 'hover':
            self.state = 'on_mouse'
            self.offset = Vector2(mouse_pos) - self.pos
            self.on_mouse_trigger()

        if not mouse_but[0] and self.state == 'on_mouse':
            self.state = 'hover'
            self.on_realease_trigger()
            
            
        if not self.rect.collidepoint(mouse_pos) and self.state == 'hover':
            self.state = 'idle'
            self.not_hovering_trigger()

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
        if self.state == 'on_mouse' or self.anchor is None or self.anchor_reach or self.move:
            return
        distance = self.pos.distance_to(self.anchor)
        speed = 100 + distance*7
        self.pos += self.direction * speed * dt
        if self.pos.distance_to(self.anchor) <= speed * dt:
            self.pos = Vector2(self.anchor)
            self.anchor_reach = True
        self.rect.center = self.pos

    def update_scale(self, dt):
        if self.scale_duration <= 0:
            return
        progress = min(1, self.scale_time / self.scale_duration)
        self.size = self.base_size + (self.final_size - self.base_size) * max(0.01, ease_out_back(progress, s= self.ease_force))
        self.surface = resize(self.base_surface, self.size)
        self.rect = self.surface.get_rect(center = self.pos)
        self.scale_time += dt
        
        if progress >= 1:
            self.scale_duration = 0
            self.size = self.final_size
            self.surface = resize(self.base_surface, self.size)
            self.rect = self.surface.get_rect(center = self.pos)



    def set_anchor(self, pos : tuple):
        self.anchor = Vector2(pos)
        self.get_direction_to_anchor()

    def stop_reacting_to_mouse(self):
        self.can_move = False
        self.state = 'idle'
    
    def start_reacting_to_mouse(self):
        self.can_move = True
        self.state = 'idle'

    
    def set_shadow(self, activated = True):
        self.handle_shadow = activated

    def set_shadow_parallax(self, x_mult= None, y_mult= None, x_abs= 0, y_abs= 0):
        self.shadow.set_parallax(x_mult= x_mult, y_mult= y_mult, x_abs= x_abs, y_abs= y_abs)

    def update(self, dt):
        self.update_pos(dt)
        self.update_scale(dt)
        self.update_auto_move(dt)
        self.shadow.update(self.rect.center)

    def draw(self, surface : pygame.Surface):
        self.shadow.draw(surface)
        surface.blit(self.surface, self.rect)

    def set_pos(self, pos):
        self.pos = pos
        self.rect.center = pos
    
    def set_z(self, new_z):
        if new_z >= 100:
            return
        else:
            if self.z == self.base_z:
                self.z = new_z
            self.base_z = new_z

    def juice(self, final_scale=1, duration=0.3, ease_force = 5):
        self.scale_duration = duration
        self.scale_time = 0
        self.final_size = final_scale
        self.base_size = self.size
        self.ease_force = ease_force

    def change_surface(self, new_surf: pygame.Surface):
        self.base_surface = new_surf
        self.surface = self.base_surface.copy()
        self.rect = self.surface.get_rect(center = self.pos)

    def get_pos(self):
        return self.pos
    
    def get_rect(self):
        return self.rect
    
    def get_anchor(self):
        return self.anchor
    
    #----------------------------------------
    # AUTO MOVE
    #----------------------------------------

    def move_to(self, target_pos):
        self.move = True
        self.target = Vector2(target_pos)
        self.target_direction = self.target - self.pos
        if self.target_direction.length() != 0 : self.target_direction = self.target_direction.normalize()
        self.speed = 100
        self.on_mouse_trigger()

    def update_auto_move(self, dt):
        if not self.move:
            return
        self.pos += self.target_direction * self.speed * dt
        self.rect.center = self.pos
        if self.pos.distance_to(self.target) <= self.speed * dt:
            self.move = False
            self.pos = Vector2(self.target)
            self.rect.center = self.pos
            self.on_realease_trigger()

            

    
    #----------------------------------------
    # TRIGGERS can be used by child classes
    #----------------------------------------

    def on_mouse_trigger(self):
        self.z = 100
        self.shadow.set_parallax(**ShadowConfig.STRONG)
        if self.on_click:
            self.on_click()

    def on_realease_trigger(self):
        self.z = self.base_z
        self.shadow.set_parallax(**ShadowConfig.DEFAULT)
        if self.on_release:
            self.on_release()

        self.get_direction_to_anchor()

    def hover_trigger(self):
        pass

    def not_hovering_trigger(self):
        pass

    def delete_callbacks(self):
        self.on_click = None
        self.on_release = None