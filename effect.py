
import pygame
from particules import *
import random

class Effect(Drawable):
    def __init__(self, pos, delay = 0, sound = None, z_index = 50):
        super().__init__(z_index)
        self.pos = pos
        self.delay = delay
        self.sound = sound
        self.starting = False


    def start(self, game):
        self.starting = True
        game.add_object(self)
    
    def update(self, dt):
        if not self.starting :
            return
        if self.delay > 0:
            self.delay -= dt
            return
        return True
    
    def draw(self, screen):
        if not self.starting or self.delay > 0:
            return
        return True
        


class ParticleEffect(Effect):
    def __init__(self, pos, amount, surface : pygame.Surface, life_time = (1, 1), dir_range_x = (-1, 1), dir_range_y = (-1, 1), speed_range = (0, 0), angle_range = (0, 0), 
                 kill_duration = 1,  delay=0, sound=None, z_index=50):
        super().__init__(pos, delay, sound, z_index)
        self.amount = amount
        self.surface = surface
        self.lf_range = life_time
        self.s_range = speed_range
        self.a_range = angle_range
        self.d_x_range = dir_range_x
        self.d_y_range = dir_range_y
        self.kill_dur = kill_duration
        self.particules = pygame.sprite.Group()

    def start(self, game):
        super().start(game)
        self.add_particules()

    def add_particules(self):
        for _ in range(self.amount):
            speed = self.s_range[0] if self.s_range[0] == self.s_range[1] else random.randint(self.s_range[0], self.s_range[1])
            angle = self.a_range[0] if self.a_range[0] == self.a_range[1] else random.randint(self.a_range[0], self.a_range[1])
            life_time = self.lf_range[0] if self.lf_range[0] == self.lf_range[1] else random.uniform(self.lf_range[0], self.lf_range[1])
            d_x = self.d_x_range[0] if self.d_x_range[0] == self.d_x_range[1] else random.uniform(self.d_x_range[0], self.d_x_range[1])
            d_y = self.d_y_range[0] if self.d_y_range[0] == self.d_y_range[1] else random.uniform(self.d_y_range[0], self.d_y_range[1])


            self.particules.add(VanishParticle(self.pos, self.surface, life_time, (d_x, d_y), speed, angle, self.kill_dur))
            

    def update(self, dt):
        if not super().update(dt):  # ← bloqué tant que delay > 0
            return 
        
        self.particules.update(dt)
        if len(self.particules) == 0:
            self.kill()

    def draw(self, screen):
        if not super().draw(screen):  # ← bloqué tant que delay > 0
            return 

        self.particules.draw(screen)




