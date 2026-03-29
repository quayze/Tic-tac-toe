import pygame
from pygame import Vector2
from drawable import *
from functions import *

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, surface : pygame.Surface, life_time, direction = (1, 0), speed = 0, angle = 0, kill_duration = 1, scaling = 1):
        super().__init__()
        self.pos : Vector2 = Vector2(pos)
        self.image = surface

        #change la taille sinon copie la surface
        if scaling != 1 : 
            self.image = resize(self.image, scaling)
        elif angle == 0:
            self.image = surface.copy()

        #change l'angle sinon copie la surface
        if angle != 0 : 
            self.image = pygame.transform.rotate(self.image, angle)
        elif scaling == 1:
            self.image = surface.copy()

        self.rect = self.image.get_rect(center = self.pos)

        self.life_time = life_time
        self.speed = speed
        self.direction = Vector2(direction)
        self.direction = self.direction.normalize() if not self.direction.length() == 0 else self.direction
        self.kill_duration = kill_duration

    def update(self, dt):
        self.life_time -= dt
        # speed = 0 -> immoveable particle 
        if self.speed != 0:
            self.pos += self.direction * self.speed * dt
            self.rect.center = self.pos

        if self.life_time <= 0:
            self.on_death(dt)
            return
        
    def on_death(self, dt):
        self.kill_duration -= dt
        if self.kill_duration <= 0:
            self.kill()


class VanishParticle(Particle):
    def __init__(self, pos, surface, life_time, direction = (1, 0), speed = 0, angle = 0, kill_duration = 1, scaling = 1, base_alpha = 255):
        super().__init__(pos, surface, life_time, direction, speed, angle, kill_duration, scaling)

        self.alpha = base_alpha
        self.alpha_decreasing = base_alpha/self.kill_duration
    
    def on_death(self, dt):
        self.alpha -= self.alpha_decreasing * dt
        self.image.set_alpha(self.alpha)
        if self.alpha <= 0:
            self.kill()


class SlowDownParticle(VanishParticle):
    def __init__(self, pos, surface, life_time, direction=(1, 0), speed=0, angle=0, kill_duration=1, 
                 scaling=1, base_alpha = 255, final_speed = 0, full_speed_time = 0.5, time_before_despawn = 1):
        super().__init__(pos, surface, life_time, direction, speed, angle, kill_duration, scaling, base_alpha)
        self.full_speed = full_speed_time
        self.final_speed = final_speed
        self.speed_decreasing = (self.speed - self.final_speed) / (life_time- self.full_speed)
        self.speed_decreasing = max(self.speed_decreasing, 0)
        self.time_before_despawn = time_before_despawn


    def update(self, dt):
        super().update(dt)
        self.full_speed -= dt
        if self.full_speed <= 0:
            self.speed -= self.speed_decreasing*dt
            self.speed = max(0, self.speed)


    def on_death(self, dt):
        self.time_before_despawn -= dt
        if self.time_before_despawn > 0:
            return
        super().on_death(dt)

class TargetParticule(Particle):
    def __init__(self, pos, surface, life_time, direction=(1, 0), speed=0, angle=0, kill_duration=0, 
                 scaling=1, target_pos = (0, 500)):
        pos = Vector2(pos)
        self.target = Vector2(target_pos)
        direction = self.target -pos
        speed = direction.length()/life_time
        kill_duration = kill_duration
        super().__init__(pos, surface, life_time, direction, speed, angle, kill_duration, scaling)

    def update(self, dt):
        self.life_time -= dt
        # speed = 0 -> immoveable particle 
        if self.speed != 0:
            if self.pos == self.target:
                self.on_death(dt)
                return
            
            self.pos += self.direction * self.speed * dt
            self.rect.center = self.pos
            if self.pos.distance_to(self.target) <= self.speed * dt:
                self.pos = self.target
            self.rect.center = self.pos