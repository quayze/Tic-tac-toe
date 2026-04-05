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

    def change_text(self, text):
        self.get_pos(text)
        self.update_text(text)    

    def get_pos(self, text):
        text_lenght = 0
        for letter in text:
            text_lenght += get_text_dimensions(letter, self.size, 'width')
        print(text_lenght)

        if self.alignment == 'midleft':
            self.first_letter_pos = self.pos
        elif self.alignment == 'center':
            mid_lenght = text_lenght/2
            self.first_letter_pos = self.pos - Vector2(mid_lenght, 0)
            

    def update_text(self, text):
        self.letters.clear()
        pos = self.first_letter_pos
        for letter in text:
           
            self.letters.append(AnimLetter(letter, self.size, (255, 255, 255), pos))
            pos += Vector2(self.offset_between, 0)

        print(self.letters[-1].rect.right - self.letters[0].rect.left)

    def draw(self, screen):
        for letter in self.letters:
            letter.draw(screen)

    def update(self, dt):
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
        self.state = 'idle'
        self.timer = 0

    def draw(self, screen):
        self.shadow.draw(screen)
        screen.blit(self.surf, self.rect)

    def update(self, dt):
        if self.state == 'idle':
            self.idle_anim(dt)
        
    def idle_anim(self, dt):   
        self.rect.centery = self.pos[1] + 10*sin(self.timer)
        self.timer += dt

        