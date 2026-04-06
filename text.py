import pygame
from settings import *
from functions import *
from shadow import *
from pygame import Vector2
from math import sin

class AnimText:
    def __init__(self, text, size, pos, align = 'center'):
        self.letters : list[AnimLetter] = []
        self.pos = Vector2(pos)
        self.size = size
        self.alignment = align
        self.offset_between = max(1, int(size * 0.7))
        self.change_text(text)
        self.state = 'disable'

    def change_text(self, text):
        self.get_pos(text)
        self.update_text(text)    

    def get_pos(self, text):
        text_length = 0
        text_length = self.offset_between * (len(text) - 1)
        letter_height = get_text_dimensions(text[0], self.size)

        if self.alignment == 'midleft':
            self.first_letter_pos = self.pos
        elif self.alignment == 'center':
            mid_lenght = text_length/2
            self.first_letter_pos = self.pos + Vector2(-mid_lenght, 0)
        elif self.alignment == 'midtop':
            mid_height = letter_height/2
            mid_lenght = text_length/2
            self.first_letter_pos = self.pos + Vector2(-mid_lenght, mid_height)
            

    def update_text(self, text):
        self.letters.clear()
        pos = self.first_letter_pos
        for letter in text:
           
            self.letters.append(AnimLetter(letter, self.size, (255, 255, 255), pos))
            pos += Vector2(self.offset_between, 0)

    def start(self):
        self.state = 'start_anim'
        self.delay = 0

    def update_animation(self, dt):
        if self.state != 'start_anim':
            return
        self.delay -= dt
        if self.delay <= 0:
            self.delay = 0.5
            for letter in self.letters:
                if letter.state != 'animate':
                    letter.state = 'animate'
                    return
            self.state = 'animating'



    def draw(self, screen):
        for letter in self.letters:
            letter.draw(screen)

    def update(self, dt):
        self.update_animation(dt)
        for letter in self.letters:
            letter.update(dt)


class AnimLetter:
    def __init__(self, letter, size, color, pos):
        self.pos = pos
        self.surf = get_text_surface(letter, size, color)
        self.rect = self.surf.get_rect(center = pos)
        self.shadow = Shadow(self.pos)
        self.shadow.set_image(self.surf)
        self.shadow.set_offset('bottom')
        self.state = 'disable'
        self.timer = 0

    def draw(self, screen):
        self.shadow.draw(screen)
        screen.blit(self.surf, self.rect)

    def update(self, dt):
        if self.state == 'animate':
            self.idle_anim(dt)
        
    def idle_anim(self, dt):   
        self.rect.centery = self.pos[1] + 10*sin(self.timer*1.5)
        self.timer += dt

        