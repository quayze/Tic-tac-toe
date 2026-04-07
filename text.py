import pygame
from settings import *
from functions import *
from shadow import *
from pygame import Vector2
from math import sin

class AnimText:
    def __init__(self, text, size, pos, align = 'center', anim_speed = 1.5):   
        self.letters : list[AnimLetter] = []
        self.pos = Vector2(pos)
        self.size = size
        self.alignment = align
        self.offset_between = max(1, int(size * 0.7))
        self.anim_speed = anim_speed
        self.change_text(text)
        self.state = 'disable'

        self.text_length = 0

    def change_text(self, text):
        self.text = text
        self.get_pos(text)
        self.update_text(text)    

    def get_pos(self, text):
        self.text_length = 0
        self.text_length = self.offset_between * (len(text) - 1)
        letter_height = get_text_dimensions(text[0], self.size)

        if self.alignment == 'midleft':
            self.first_letter_pos = self.pos
        elif self.alignment == 'center':
            mid_lenght = self.text_length/2
            self.first_letter_pos = self.pos + Vector2(-mid_lenght, 0)
        elif self.alignment == 'midtop':
            mid_height = letter_height/2
            mid_lenght = self.text_length/2
            self.first_letter_pos = self.pos + Vector2(-mid_lenght, mid_height)
            

    def update_text(self, text):
        self.letters.clear()
        pos = self.first_letter_pos
        for letter in text:
           
            self.letters.append(AnimLetter(letter, self.size, (255, 255, 255), pos, self.anim_speed))
            pos += Vector2(self.offset_between, 0)

    def start(self):
        self.state = 'start_anim'
        self.delay = 0

    def update_animation(self, dt):
        if self.state != 'start_anim':
            return
        self.delay -= dt
        if self.delay <= 0:
            self.delay = 1/self.anim_speed
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

    def set_pos(self, pos, alignment = None):
        self.alignment = alignment if alignment is not None else self.alignment
        self.pos = pos
        self.change_text(self.text)

    def get_height(self):
        return self.letters[0].rect.height
    
    def get_width(self):
        return self.letters[-1].rect.right - self.letters[0].rect.left
    
    def get_bottom(self):
        return self.letters[0].rect.bottom
    
    def get_center(self):
        return self.first_letter_pos + Vector2((self.letters[-1].rect.right - self.letters[0].rect.left) //2, 0)


class AnimLetter:
    def __init__(self, letter, size, color, pos, speed = 1.5):
        self.pos = pos
        self.surf = get_text_surface(letter, size, color)
        self.rect = self.surf.get_rect(center = pos)
        self.offset = size * 0.1
        self.shadow = Shadow(self.pos)
        self.shadow.set_image(self.surf)
        self.shadow.set_parallax(y_abs= self.offset )
        self.state = 'disable'
        self.timer = 0
        self.speed = speed

    def draw(self, screen):
        self.shadow.draw(screen)
        screen.blit(self.surf, self.rect)

    def update(self, dt):
        if self.state == 'animate':
            self.idle_anim(dt)
        
    def idle_anim(self, dt):   
        self.rect.centery = self.pos[1] + self.offset *sin(self.timer*self.speed)
        self.timer += dt

        