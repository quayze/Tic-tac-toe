import pygame
from moveable_object import Moveable
from functions import *


class Button(Moveable):
    def __init__(self, pos, width, height, color = (255, 255, 255), text = '', text_size = 50):
        super().__init__(pos, width, height)
        self.image = generate_nine_slice(width, height, color)



        text_surface = get_text_surface(text, text_size)
        text_rect = text_surface.get_rect(center = (self.image.get_width()//2, self.image.get_height()/2))
        self.image.blit(text_surface, text_rect)


        self.hover_image = self.image.copy()
        self.hover_image.fill((170, 170, 170), special_flags= pygame.BLEND_RGBA_MULT)

        self.active_image = self.image
        self.shadow.set_image(self.image)

        self.active = True



    def handle_mouse(self, mouse_pos):
        if not self.active:
            return
        mouse_but = pygame.mouse.get_pressed()

        if mouse_but[0] and not self.rect.collidepoint(mouse_pos):
            self.hold = True

        elif not mouse_but[0]:
            self.hold = False

        if self.hold:
            return

        if self.rect.collidepoint(mouse_pos) and not self.state == 'on_mouse':
            self.active_image = self.hover_image
            self.state = 'hover'

        if mouse_but[0] and self.state == 'hover':
            self.rect.center = self.shadow.obtain_pos()
            self.state = 'on_mouse'

        if not mouse_but[0] and self.state == 'on_mouse':
            self.state = 'hover'
            self.rect.center = self.pos
            if self.on_release:
                self.on_release()
            

        if not self.rect.collidepoint(mouse_pos) and self.state == 'hover':
            self.active_image = self.image
            self.state = 'idle'


    def draw(self, screen):
        self.shadow.draw(screen)
        screen.blit(self.active_image, self.rect)


    def update(self, dt):
        pass


