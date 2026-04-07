import pygame
from pygame import Vector2
from drawable import *
from functions import *

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, surface : pygame.Surface, life_time, direction = (1, 0), 
                 speed = 0, angle = 0, kill_duration = 1, scaling = 1, alpha = 255,
                 death_behavior = None):
        super().__init__()
        self.pos : Vector2 = Vector2(pos)
        self.image = surface
        self.alpha = alpha
        self.angle = angle

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

        self.image.set_alpha(self.alpha)

        self.rect = self.image.get_rect(center = self.pos)

        self.life_time = life_time
        self.speed = speed
        self.direction = Vector2(direction)
        self.direction = self.direction.normalize() if not self.direction.length() == 0 else self.direction
        self.kill_duration = kill_duration
        self.death_behavior = death_behavior() if death_behavior is not None else TimedDeath()
        self.death_behavior.setup(self)

    def update(self, dt):
        self.life_time -= dt
        # speed = 0 -> immoveable particle 
        if self.speed != 0:
            self.pos += self.direction * self.speed * dt
            self.rect.center = self.pos

        if self.life_time <= 0:
            self.death_behavior.on_death(self, dt)
        




class SlowDownParticle(Particle):
    def __init__(self, pos, surface, life_time, direction=(1, 0), speed=0, angle=0, kill_duration=1, 
                 scaling=1, alpha = 255, death_behavior = None, final_speed = 0, 
                 full_speed_time = 0.3, time_before_despawn = 0):
        super().__init__(pos, surface, life_time, direction, speed, angle, kill_duration, scaling, alpha, death_behavior)
        self.full_speed = full_speed_time
        self.final_speed = final_speed
        self.speed_decreasing = (self.speed - self.final_speed) / (life_time- self.full_speed)
        self.speed_decreasing = max(self.speed_decreasing, 0)
        self.time_before_despawn = time_before_despawn

    def update(self, dt):
        self.full_speed -= dt
        self.life_time -= dt

        if self.speed != 0:
            self.pos += self.direction * self.speed * dt
            self.rect.center = self.pos

        if self.full_speed <= 0:
            self.speed -= self.speed_decreasing*dt
            self.speed = max(0, self.speed)
        
        if self.life_time <= 0:
            self.time_before_despawn -= dt
            if self.time_before_despawn <= 0:
                self.death_behavior.on_death(self, dt)
            


class TargetParticule(Particle):
    def __init__(self, pos, surface, life_time, direction=(1, 0), speed=0, angle=0, kill_duration=1, 
                 scaling=1, alpha = 255, death_behavior = None, target_pos = (0, 500)):
        pos = Vector2(pos)
        self.target = Vector2(target_pos)
        direction = self.target -pos
        speed = direction.length()/life_time
        kill_duration = kill_duration
        super().__init__(pos, surface, life_time, direction, speed, angle, kill_duration, scaling, alpha, death_behavior)

    def update(self, dt):
        self.life_time -= dt
        # speed = 0 -> immoveable particle 
        if self.speed != 0:
            if self.pos == self.target:
                self.death_behavior.on_death(self, dt)
                return
            
            self.pos += self.direction * self.speed * dt
            self.rect.center = self.pos
            if self.pos.distance_to(self.target) <= self.speed * dt:
                self.pos = self.target
            self.rect.center = self.pos


class FallingParticle(Particle):
    def __init__(self, pos, surface, life_time, direction = (1, 0), speed = 0, angle = 0, kill_duration = 0, 
                 scaling = 1, alpha = 255, death_behavior = None, gravity_direction = (0, 1), gravity_force = 40):
        super().__init__(pos, surface, life_time, direction, speed, angle, kill_duration, scaling, alpha, death_behavior)
        self.gravity_force = gravity_force
        self.gravity = 0
        self.gravity_direction = Vector2(gravity_direction)

    def update(self, dt):
        self.life_time -= dt
        self.pos += self.direction * self.speed * dt
        self.pos += self.gravity * self.gravity_direction * dt
        self.rect.center = self.pos

        self.gravity += self.gravity_force
        if self.life_time <= 0:
            self.death_behavior.on_death(self, dt)


class DeathBehavior:
    def setup(self, particle : Particle): 
        pass

    def on_death(self, particle : Particle, dt):
        particle.kill()

class TimedDeath(DeathBehavior):
    def on_death(self, particle, dt):
        particle.kill_duration -= dt
        if particle.kill_duration <= 0:
            particle.kill()

class FadeDeath(DeathBehavior):
    def setup(self, particle):
        self.alpha = particle.alpha
        self.alpha_rate = self.alpha / particle.kill_duration

    def on_death(self, particle, dt):
        self.alpha -= self.alpha_rate * dt
        particle.image.set_alpha(self.alpha)
        if self.alpha <= 0:
            particle.kill()
    
class ScaleDeath(DeathBehavior):
    def setup(self, particle):
        self.scale = 1
        self.scale_rate = 1 / particle.kill_duration
        self.copy_image = particle.image

    def on_death(self, particle, dt):
        self.scale -= self.scale_rate * dt
        if self.scale <= 0:
            particle.kill()
            return
        particle.image = resize(self.copy_image, self.scale)
        particle.rect = particle.image.get_rect(center = particle.pos)
        