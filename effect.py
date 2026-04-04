
import pygame
from particles import *
import random

class Effect(Drawable):
    def __init__(self, pos, delay = 0, sound = None, z_index = 50):
        super().__init__(z_index)
        self.pos = pos
        self.delay = delay
        self.sound = sound
        self.sound_played = False
        self.starting = False


    def start(self, game):
        self.starting = True
        game.add_object(self)
        self.play_audio(game)

    def play_audio(self, game):
        if self.sound_played:
            return
        if self.sound is None:
            self.sound_played = True
            return
        game.play_sound(sound_path = self.sound)
        self.sound_played = True
    
    def update(self, dt):
        if not self.starting :
            return
        return True
    
    def update_timer(self, dt):
        if self.delay > 0:
            self.delay -= dt
    
    def draw(self, screen):
        if not self.starting:
            return
        return True
    
class SoundEffect(Effect):
    def __init__(self, delay=0, sound_path = None):
        super().__init__((0,0), delay, sound_path, 0)

    def start(self, game):
        self.starting = True
        self.play_audio(game)

    def update(self, dt):
        if not super().update(dt):
            return 
        
        if self.sound_played:
            self.kill()
        


class ParticleEffect(Effect):
    def __init__(self, pos, amount, surface : pygame.Surface, particle_type : Particle,
                 life_time = (1, 1), dir_range_x = (-1, 1), dir_range_y = (-1, 1), speed_range = (0, 0), angle_range = (0, 0), scale_range = (1, 1),
                 kill_duration = 1,  delay=0, sound=None, z_index=50):
        super().__init__(pos, delay, sound, z_index)
        self.amount = amount
        self.surface = surface
        self.lf_range = life_time
        self.s_range = speed_range
        self.a_range = angle_range
        self.d_x_range = dir_range_x
        self.d_y_range = dir_range_y
        self.scl_range = scale_range
        self.kill_dur = kill_duration

        self.particle_type = particle_type
        self.particles = pygame.sprite.Group()

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
            scale = self.scl_range[0] if self.scl_range[0] == self.scl_range[1] else random.uniform(self.scl_range[0], self.scl_range[1])


            self.particles.add(self.particle_type(self.pos, self.surface, life_time, (d_x, d_y), speed, angle, self.kill_dur, scale))
            

    def update(self, dt):
        if not super().update(dt):
            return 
        
        self.particles.update(dt)
        if len(self.particles) == 0:
            self.kill()

    def draw(self, screen):
        if not super().draw(screen): 
            return 

        self.particles.draw(screen)


class BloodEffect(ParticleEffect):
    def __init__(self, pos, direction = (1, 0), delay=0, z_index=50):
        surface = pygame.Surface((10, 10), pygame.SRCALPHA).convert_alpha()
        surface.fill((255, 0, 0))
        sound = None
        amount = 500
        life_time = (0.5, 1)
        kill_duration = 1
        dir_range_x= (0, 0)
        dir_range_y= (0, 0)
        speed_range=(400, 800)
        angle_range=(-180, 180)
        scale_range=(0.5, 1.5)
        super().__init__(pos, amount, surface, SlowDownParticle, life_time, dir_range_x, dir_range_y, speed_range, angle_range, scale_range, kill_duration, delay, sound, z_index)
        self.angle_offset = 30
        self.direction = Vector2(direction)
        self.time_inactive = (0.7, 1)

    def add_particules(self):
        for _ in range(self.amount):
            speed = random.randint(self.s_range[0], self.s_range[1])
            angle = random.randint(self.a_range[0], self.a_range[1])
            life_time = random.uniform(self.lf_range[0], self.lf_range[1])

            dir_angle = random.uniform(-self.angle_offset, self.angle_offset)
            direction = self.direction.rotate(dir_angle)

            time_inactive = random.uniform(self.time_inactive[0], self.time_inactive[1])

            scale =random.uniform(self.scl_range[0], self.scl_range[1])
            full_time_speed = life_time / 3

            self.particles.add(self.particle_type(self.pos, self.surface, life_time, direction, speed, angle, 
                                                  self.kill_dur, scale, full_speed_time = full_time_speed, time_before_despawn = time_inactive))

class TargetEffect(ParticleEffect):
    def __init__(self, pos, amount, surface, target : tuple, adaptative_angle = False,
                 life_time=(1, 1), angle_range=(0, 0), scale_range=(1, 1), 
                 kill_duration=0, delay=0, sound=None, z_index=50):
        self.target = target
        self.adaptative_angle = adaptative_angle
        super().__init__(pos, amount, surface, TargetParticule, life_time, (0, 0), (0, 0), (0, 0), angle_range, scale_range, kill_duration, delay, sound, z_index)


    def add_particules(self):
        for _ in range(self.amount):
            if self.adaptative_angle:
                direction = Vector2(self.target) - Vector2(self.pos)
                angle = direction.angle_to((0, -1))
            else:
                angle = random.randint(self.a_range[0], self.a_range[1])

            life_time = random.uniform(self.lf_range[0], self.lf_range[1])
            scale =random.uniform(self.scl_range[0], self.scl_range[1])

            self.particles.add(self.particle_type(self.pos, self.surface, life_time, angle = angle, kill_duration= self.kill_dur, 
                 scaling= scale, target_pos = self.target))
            
class VanishEffect(ParticleEffect):
    def __init__(self, pos, amount, surface, life_time=(1, 1), dir_range_x=(-1, 1), 
                 dir_range_y=(-1, 1), speed_range=(0, 0), angle_range=(0, 0), scale_range=(1, 1),
                 base_alpha = 255, 
                 kill_duration=1, delay=0, sound=None, z_index=50):
        super().__init__(pos, amount, surface, VanishParticle, life_time, dir_range_x, dir_range_y, 
                         speed_range, angle_range, scale_range, kill_duration, delay, sound, z_index)
        self.base_alpha = base_alpha


    def add_particules(self):
        for _ in range(self.amount):
            speed = self.s_range[0] if self.s_range[0] == self.s_range[1] else random.randint(self.s_range[0], self.s_range[1])
            angle = self.a_range[0] if self.a_range[0] == self.a_range[1] else random.randint(self.a_range[0], self.a_range[1])
            life_time = self.lf_range[0] if self.lf_range[0] == self.lf_range[1] else random.uniform(self.lf_range[0], self.lf_range[1])
            d_x = self.d_x_range[0] if self.d_x_range[0] == self.d_x_range[1] else random.uniform(self.d_x_range[0], self.d_x_range[1])
            d_y = self.d_y_range[0] if self.d_y_range[0] == self.d_y_range[1] else random.uniform(self.d_y_range[0], self.d_y_range[1])
            scale = self.scl_range[0] if self.scl_range[0] == self.scl_range[1] else random.uniform(self.scl_range[0], self.scl_range[1])


            self.particles.add(self.particle_type(self.pos, self.surface, life_time, (d_x, d_y), speed, angle, self.kill_dur, scale, self.base_alpha))

class FallEffect(ParticleEffect):
    def __init__(self, pos, amount, surface, life_time=(1, 1), gravity_direction = (0, 1), gravity_force = 40, direction = (0, -1), angle_offset = 0, speed_range=(0, 0), angle_range=(0, 0), scale_range=(1, 1), 
                 kill_duration=1, delay=0, sound=None, z_index=50):
        super().__init__(pos, amount, surface, FallingParticle, life_time, (0, 0), (0, 0), speed_range, angle_range, scale_range, kill_duration, delay, sound, z_index)
        self.gravity_direction = gravity_direction
        self.direction = Vector2(direction)
        self.angle_offset = angle_offset
        self.gravity_force = gravity_force


    def add_particules(self):
        for _ in range(self.amount):
            speed = self.s_range[0] if self.s_range[0] == self.s_range[1] else random.randint(self.s_range[0], self.s_range[1])
            angle = self.a_range[0] if self.a_range[0] == self.a_range[1] else random.randint(self.a_range[0], self.a_range[1])
            life_time = self.lf_range[0] if self.lf_range[0] == self.lf_range[1] else random.uniform(self.lf_range[0], self.lf_range[1])
            scale = self.scl_range[0] if self.scl_range[0] == self.scl_range[1] else random.uniform(self.scl_range[0], self.scl_range[1])
            
            if self.angle_offset != 0:
                dir_angle = random.uniform(-self.angle_offset, self.angle_offset)
                direction = self.direction.rotate(dir_angle)
            else:
                direction = self.direction

            self.particles.add(self.particle_type(self.pos, self.surface, life_time, direction, speed, angle, self.kill_dur, scale, self.gravity_direction, self.gravity_force))
