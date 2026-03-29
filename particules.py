import pygame
from pygame import Vector2
from drawable import *

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, surface : pygame.Surface, life_time):
        super().__init__()
        self.pos = pos
        self.image = surface
        self.rect = self.image.get_rect(center = self.pos)
        self.life_time = life_time

    def update(self, dt):
        self.life_time -= dt
        if self.life_time <= 0:
            self.update_death(dt)
            return
        
    def update_death(self, dt):
        self.kill()


class VanishParticle(Particle):
    def __init__(self, pos, surface, life_time, direction = (1, 0), speed = 0, angle = 0, kill_duration = 1):
        surf = pygame.transform.rotate(surface, angle)
        super().__init__(pos, surf, life_time)
        self.speed = speed
        self.direction = Vector2(direction)
        if not self.direction.length() == 0:
            self.direction = self.direction.normalize()

        self.alpha = 255
        self.alpha_decreasing = 255/kill_duration


    def update(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos
        return super().update(dt)
    
    def update_death(self, dt):
        self.alpha -= self.alpha_decreasing * dt
        self.image.set_alpha(self.alpha)
        if self.alpha <= 0:
            self.kill()