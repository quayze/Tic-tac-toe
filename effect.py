
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
        if not self.starting:
            return False
        return True
        
    def update_timer(self, dt):
        if self.delay > 0:
            self.delay -= dt
    
    def draw(self, screen):
        if not self.starting:
            return False
        return True
    
class SoundEffect(Effect):
    def __init__(self, sound_path = None, delay=0):
        super().__init__((0,0), delay, sound_path, 0)

    def start(self, game):
        self.starting = True
        self.play_audio(game)
        

    def update(self, dt):
        if not super().update(dt):
            return 
        
        if self.sound_played:
            self.kill()

class GameEffect(Effect):
    def __init__(self, delay=0):
        super().__init__((0, 0), delay, None, 0)

    def start(self, game):
        self.kill()

class MultipleEffect(Effect):
    def __init__(self, pos, delay=0, sound=None, z_index=50):
        super().__init__(pos, delay, sound, z_index)
        self.effects : list[Effect] = []

    def add_effect(self, effect : Effect):
        self.effects.append(effect)

    def get_effect_list(self):
        return self.effects

    def start(self, game):
        for effect in self.effects:
            game.add_effect(effect)
        self.effects.clear()
        self.play_audio(game)
        self.kill()

        
class ParticleEffect(Effect):
    def __init__(self, pos, amount, surface : pygame.Surface, particle_type : Particle = Particle,
                 life_time = 1, direction_x = (-1, 1), direction_y = (-1, 1), speed = 0, angle = 0, scale = 1,
                 kill_duration = 1,  delay=0, sound=None, z_index=50, alpha = 255, death_effect = None):
        super().__init__(pos, delay, sound, z_index)
        self.amount = amount
        self.surface = surface
        self.lf_range = life_time
        self.s_range = speed
        self.a_range = angle
        self.d_x_range = direction_x
        self.d_y_range = direction_y
        self.scl_range = scale
        self.kill_dur = kill_duration
        self.alpha = alpha
        self.death_eff = death_effect or TimedDeath

        self.particle_type = particle_type
        self.particles = pygame.sprite.Group()

    def start(self, game):
        super().start(game)
        self.add_particles()
        

    def add_particles(self):
        for _ in range(self.amount):
            speed = rand(self.s_range, True)
            angle = rand(self.a_range, True)
            life_time = rand(self.lf_range)
            d_x = rand(self.d_x_range)
            d_y = rand(self.d_y_range)
            scale = rand(self.scl_range)
            alpha = rand(self.alpha, True)


            self.particles.add(self.particle_type(self.pos, self.surface, life_time, (d_x, d_y), speed, angle, self.kill_dur, scale, alpha, self.death_eff))
            

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

class RotateEffect(ParticleEffect):
    def __init__(self, pos, amount, surface, life_time=1, direction_x=(-1, 1), 
                 direction_y=(-1, 1), speed=0, angle=0, scale=1, 
                 kill_duration=1, delay=0, sound=None, z_index=50, alpha=255, death_effect=None, rotation_speed = 360):
        
        super().__init__(pos, amount, surface, RotatingParticle, life_time, direction_x, direction_y, speed, 
                         angle, scale, kill_duration, delay, sound, z_index, alpha, death_effect)
        self.rotation_speed = rotation_speed
        
    def add_particles(self):
        for _ in range(self.amount):
            speed = rand(self.s_range, True)
            angle = rand(self.a_range, True)
            life_time = rand(self.lf_range)
            d_x = rand(self.d_x_range)
            d_y = rand(self.d_y_range)
            scale = rand(self.scl_range)
            alpha = rand(self.alpha, True)
            rotation_speed = rand(self.rotation_speed, True)


            self.particles.add(self.particle_type(self.pos, self.surface, life_time, (d_x, d_y), speed, angle, self.kill_dur, scale, alpha, self.death_eff, rotation_speed))
        


class BloodEffect(ParticleEffect):
    def __init__(self, pos, direction = (1, 0), amount = 500, angle_offset = 30, delay=0, z_index=50):
        surface = pygame.Surface((10, 10), pygame.SRCALPHA).convert_alpha()
        surface.fill((255, 0, 0))
        sound = None
        amount = amount
        life_time = (0.5, 1)
        kill_duration = 1
        direction_x= (0, 0)
        direction_y= (0, 0)
        speed=(400, 800)
        angle=(-180, 180)
        scale=(0.5, 1.5)
        super().__init__(pos, amount, surface, SlowDownParticle, life_time, direction_x, direction_y, speed, 
                         angle, scale, kill_duration, delay, sound, z_index, death_effect= FadeDeath)
        self.angle_offset = angle_offset
        self.direction = Vector2(direction)
        self.time_inactive = (0.7, 1)

    def add_particles(self):
        for _ in range(self.amount):
            speed = rand(self.s_range, True)
            angle = rand(self.a_range, True)
            life_time = rand(self.lf_range)

            dir_angle = random.uniform(-self.angle_offset, self.angle_offset)
            direction = self.direction.rotate(dir_angle)

            time_inactive = random.uniform(self.time_inactive[0], self.time_inactive[1])

            scale = rand(self.scl_range)
            full_time_speed = life_time / 3


            self.particles.add(self.particle_type(self.pos, self.surface, life_time, direction, speed, angle, 
                                                  self.kill_dur, scale, full_speed_time = full_time_speed, time_before_despawn = time_inactive,
                                                  death_behavior = self.death_eff))

class TargetEffect(ParticleEffect):
    def __init__(self, pos, amount, surface, target : tuple, adaptative_angle = False,
                 life_time=1, angle=0, scale=1, 
                 kill_duration=0, delay=0, sound=None, z_index=50, alpha = (255, 255), death_effect = None):
        self.target = target
        self.adaptative_angle = adaptative_angle
        super().__init__(pos, amount, surface, TargetParticle, life_time, (0, 0), (0, 0), (0, 0), angle, 
                         scale, kill_duration, delay, sound, z_index, alpha, death_effect)


    def add_particles(self):
        for _ in range(self.amount):
            if self.adaptative_angle:
                direction = Vector2(self.target) - Vector2(self.pos)
                angle = direction.angle_to((0, -1))
            else:
                angle = rand(self.a_range, True)

            life_time = rand(self.lf_range)
            scale = rand(self.scl_range)
            alpha = rand(self.alpha, True)

            self.particles.add(self.particle_type(self.pos, self.surface, life_time, angle = angle, kill_duration= self.kill_dur, 
                 scaling= scale, alpha = alpha, death_behavior = self.death_eff, target_pos = self.target))
            


class FallEffect(ParticleEffect):
    def __init__(self, pos, amount, surface, life_time=1, gravity_direction = (0, 1), gravity_force = 40, direction = (0, -1), angle_offset = 0, speed=0, angle=0, scale=1, 
                 kill_duration=1, delay=0, sound=None, z_index=50, alpha = (255, 255)):
        super().__init__(pos, amount, surface, FallingParticle, life_time, 0, 0, speed, angle, 
                         scale, kill_duration, delay, sound, z_index, alpha)
        self.gravity_direction = gravity_direction
        self.direction = Vector2(direction)
        self.angle_offset = angle_offset
        self.gravity_force = gravity_force


    def add_particles(self):
        for _ in range(self.amount):
            speed = rand(self.s_range, True)
            angle = rand(self.a_range, True)
            life_time = rand(self.lf_range)
            scale = rand(self.scl_range)
            alpha = rand(self.alpha, True)
            
            if self.angle_offset != 0:
                dir_angle = random.uniform(-self.angle_offset, self.angle_offset)
                direction = self.direction.rotate(dir_angle)
            else:
                direction = self.direction

            self.particles.add(self.particle_type(self.pos, self.surface, life_time, direction, speed, angle, self.kill_dur, 
                                                  scale, alpha, self.death_eff, self.gravity_direction, self.gravity_force))


class ExplosionEffect(ParticleEffect):
    def __init__(self, pos, amount, life_time=1, speed=0,
                 color = (255, 255, 255), scale= 1, final_speed = 50,
                 kill_duration = 1, delay=0, z_index=50):
        

        surface = generate_round(pixel_size= 5, radius=  scale * 5, color= color)

        sound = None
        direction_x= (-1, 1)
        direction_y= (-1, 1)
        angle=(0, 0)
        alpha = (255, 255)
        self.final_speed = final_speed


        super().__init__(pos, amount, surface, SlowDownParticle, life_time, direction_x, direction_y, 
                         speed, angle, scale, kill_duration, delay, 
                         sound, z_index, alpha, ScaleDeath)

    def add_particles(self):
        for _ in range(self.amount):
            speed = rand(self.s_range, True)
            angle = rand(self.a_range, True)
            life_time = rand(self.lf_range)
            kill_time = rand(self.kill_dur)

            d_x = rand(self.d_x_range)
            d_y = rand(self.d_y_range)


            full_time_speed = life_time / 4


            self.particles.add(self.particle_type(self.pos, self.surface, life_time, (d_x, d_y), speed, angle, 
                                                  kill_time, full_speed_time = full_time_speed,
                                                  death_behavior = self.death_eff, final_speed = self.final_speed))
            


class FullExplosionEffect(MultipleEffect):
    def __init__(self, pos, delay=0, z_index=50):
        sound = SFX.EXPLOSION
        super().__init__(pos, delay, sound, z_index)
        self.add_effect(ExplosionEffect(pos, amount= 20, speed= (1000, 1200), 
                                        life_time= (0.6, 1), scale= 3,color= (0, 0, 0), z_index=self.z))
        
        self.add_effect(ExplosionEffect(pos, amount= 20, speed= (1000, 1200), 
                                        life_time= (0.6, 1), scale= 3,color= (255, 255, 255), z_index=self.z))

        self.add_effect(ExplosionEffect(pos, amount= 40, speed= (400, 1000), 
                                        life_time= (0.5, 0.8), scale= 8, color= (255, 150, 0), z_index=self.z))
        
        self.add_effect(ExplosionEffect(pos, amount= 80, speed= (400, 1000), 
                                        life_time= (0.4, 0.8), scale= 8, color= (255, 30, 0), z_index=self.z))
        

class CompressEffect(ParticleEffect):
    def __init__(self, pos, amount, surface, life_time=(1, 1), 
                 angle=(0, 0), scale=(1, 1), kill_duration=1, delay=0, sound=None, 
                 z_index=50, alpha=(255, 255), death_effect=None, distance = (0, 200), adaptative_angle = False):
        
        super().__init__(pos, amount, surface, TargetParticle, life_time, (0, 0), (0, 0),
                          (0, 0), angle, scale, kill_duration, delay, 
                          sound, z_index, alpha, death_effect)
        
        self.adaptative_angle = adaptative_angle
        self.dist_range = distance

    def add_particles(self):
        for _ in range(self.amount):
            
            distance = rand(self.dist_range, True)
            vector = Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
            vector = vector.normalize() if vector.length() != 0 else vector

            init_pos = self.pos +  vector * distance



            if self.adaptative_angle:
                direction = Vector2(self.pos) - Vector2(init_pos)
                angle = direction.angle_to((0, -1))
            else:
                angle = rand(self.a_range, True)

            life_time = rand(self.lf_range)
            scale = rand(self.scl_range)
            alpha = rand(self.alpha, True)

            self.particles.add(self.particle_type(init_pos, self.surface, life_time, angle = angle, kill_duration= self.kill_dur, 
                 scaling= scale, alpha = alpha, death_behavior = self.death_eff, target_pos = self.pos))
        

        
class BreakEffect(MultipleEffect):
    def __init__(self, pos, surface : pygame.Surface, delay=0, sound=None, z_index=50, intensity = 700):
        super().__init__(pos, delay, sound, z_index)
        surf_mid_x, surf_mid_y = surface.get_size()
        surf_mid_x, surf_mid_y = surf_mid_x//2, surf_mid_y//2

        topleft = pygame.Surface((surf_mid_x, surf_mid_y), pygame.SRCALPHA).convert_alpha()
        topleft.blit(surface, (0, 0))
        tl_pos = pos[0] - surf_mid_x//2, pos[1] - surf_mid_y//2

        topright = pygame.Surface((surf_mid_x, surf_mid_y), pygame.SRCALPHA).convert_alpha()
        topright.blit(surface, (-surf_mid_x, 0))
        tr_pos = pos[0] + surf_mid_x//2, pos[1] - surf_mid_y//2

        bottomleft = pygame.Surface((surf_mid_x, surf_mid_y), pygame.SRCALPHA).convert_alpha()
        bottomleft.blit(surface, (0, -surf_mid_y))
        bl_pos = pos[0] - surf_mid_x//2, pos[1] + surf_mid_y//2

        bottomright = pygame.Surface((surf_mid_x, surf_mid_y), pygame.SRCALPHA).convert_alpha()
        bottomright.blit(surface, (-surf_mid_x, -surf_mid_y))
        br_pos = pos[0] + surf_mid_x//2, pos[1] + surf_mid_y//2



        self.add_effect(FallEffect(tl_pos, 1, topleft, 1, speed= (intensity - 300, intensity), 
                                   direction= (-1, -2), angle_offset= 20, z_index=self.z))
        self.add_effect(FallEffect(tr_pos, 1, topright, 1, speed= (intensity - 300, intensity), 
                                   direction= (1, -2), angle_offset= 20, z_index=self.z))
        self.add_effect(FallEffect(bl_pos, 1, bottomleft, 1, speed= (intensity - 400, intensity - 200), 
                                   direction= (-1, -1), angle_offset= 20, z_index=self.z))
        self.add_effect(FallEffect(br_pos, 1, bottomright, 1, speed= (intensity - 400, intensity - 200), 
                                   direction= (1, -1), angle_offset= 20, z_index=self.z))
        

class LightningEffect(MultipleEffect):
    def __init__(self, pos, thickness = 15, color_center = (255, 255, 255), color_border = (255,255, 0),
                  sound = SFX.LIGHTNING, delay=0, z_index=50):
        super().__init__(pos, delay, sound, z_index)



        pixel_size = 5
        self.pos = Vector2(pos)
        last_pos = self.pos + Vector2(0, -250)
        lightning_surf = pygame.Surface((100, abs(self.pos.y - last_pos.y)), pygame.SRCALPHA).convert_alpha()

        init_pos = Vector2(lightning_surf.get_width()/2, lightning_surf.get_height())
        end_pos = Vector2(lightning_surf.get_width()/2, 0)
        
        
        
        distance_between_pt = (30, 70)

        all_points = []

        point = init_pos
        

        while point.y > end_pos.y:
            all_points.append(point.copy())
            point = Vector2(random.randint(20, lightning_surf.get_width() - 20), point.y - random.randint(*distance_between_pt))
            

        point = Vector2(random.randint(0, 100), end_pos.y)
        all_points.append(point)
        

        self.draw_bolt(all_points, lightning_surf, int(thickness* 1.5), color_border)
        self.draw_bolt(all_points, lightning_surf, thickness, color_center)

        lightning_surf = resize(lightning_surf, pixel_size)

        center = self.pos.x, (self.pos.y - lightning_surf.get_height()//2)
        self.add_effect(ParticleEffect(
            center, 1, lightning_surf, life_time= (1.2, 1.2), death_effect= FadeDeath
        ))
        self.add_effect(ExplosionEffect(self.pos, 40, scale= 2, speed= (200,400), life_time= (0.8, 1.2), color = (color_center), final_speed= 20))
        self.add_effect(ExplosionEffect(self.pos, 40, scale= 4, speed= (100,300), color= color_border, life_time= (0.5, 0.8), final_speed= 20))
        self.add_effect(ExplosionEffect(self.pos, 100, scale= 1, speed= (0,50), color= color_center, life_time= (1.5, 1.5), final_speed= 0))

        

    def draw_bolt(self, all_points, surface, thickness, color = (255, 255, 255)):
        last_point = None
        for point in all_points:
            if last_point == None:
                last_point = point
            else:
                pygame.draw.line(surface, color, last_point, point, thickness)
                last_point = point

class ScreenShakeEffect(GameEffect):
    def __init__(self, duration = 1, offset_x = 20, offset_y = 20, delay=0):
        super().__init__(delay)
        self.duration = duration

        self.offset_x = self.get_offset(offset_x)
        self.offset_y = self.get_offset(offset_y)

    def get_offset(self, offset):
        if isinstance(offset, tuple):
            if offset[0] <= 0 and offset[1] >= 0:
                return offset
            else:
                return (-(offset[0]), abs(offset[0]))

        elif isinstance(offset, int):
           return -abs(offset), abs(offset)
        
        else:
            return (-20, 20)

    def start(self, game):
        game.add_screen_shake(self.duration, self.offset_x, self.offset_y)
        return super().start(game)
    


class FlashEffect(ParticleEffect):
    def __init__(self, color = (255, 255, 255), duration = 1, alpha=255, 
                 spawn_duration = 0.1, kill_duration = 0, death_effect = None,
                delay=0, z_index = 0):
        surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA).convert_alpha()
        surface.fill(color)
        super().__init__((WIDTH//2, HEIGHT//2), 1, surface, FadeParticle, duration, 0, 0, 0, 0, 1, kill_duration, delay, None, z_index, alpha, death_effect)
        self.spawn_duration = spawn_duration

    def add_particles(self):
        for _ in range(self.amount):
            speed = rand(self.s_range, True)
            angle = rand(self.a_range, True)
            life_time = rand(self.lf_range)
            d_x = rand(self.d_x_range)
            d_y = rand(self.d_y_range)
            scale = rand(self.scl_range)
            alpha = rand(self.alpha, True)


            self.particles.add(self.particle_type(self.pos, self.surface, life_time, (d_x, d_y), speed, angle, self.kill_dur, scale, alpha, self.death_eff, self.spawn_duration))


class WinEffect(MultipleEffect):
    def __init__(self, first_pos, last_pos, overshoot = 0, delay=0, z_index=50):
        first_pos = Vector2(first_pos)
        last_pos = Vector2(last_pos)
        pos = (first_pos.x + last_pos.x)//2 , (first_pos.y + last_pos.y)//2
        sound = SFX.WIN
        super().__init__(pos, delay, sound, z_index)


        check_image = load_image('win_check', PartConfig.WIN_CHECK)
        end_piece = get_image(check_image, 13, 9)
        mid_piece = get_image(check_image, 13, 9, frame_x= 1)

        end_piece = resize(end_piece, NineSliceConfig.PIXEL_SIZE)
        mid_piece = resize(mid_piece, NineSliceConfig.PIXEL_SIZE)
        width = mid_piece.get_width()


        vector = last_pos - first_pos
        length = first_pos.distance_to(last_pos) + overshoot

        height = end_piece.get_height()
        mid_piece_height = max(0, length - height*2)

        mid_piece = pygame.transform.scale(mid_piece, (width, mid_piece_height))
        
        surface = pygame.Surface((width, length), pygame.SRCALPHA).convert_alpha()
        surface.blit(end_piece, (0, 0))
        surface.blit(pygame.transform.flip(end_piece, False, True), (0, mid_piece_height + height))
        surface.blit(mid_piece, (0, height))


        surface = pygame.transform.rotate(surface, vector.angle_to((0, -1)))

        self.add_effect(ParticleEffect(pos, 1, surface, life_time= 1, particle_type= GrowParticle, death_effect= ScaleDeath, kill_duration= 0.4))


class PlaceSquareEffect(MultipleEffect):
    def __init__(self, pos, rarity = 'common' ,delay=0, z_index=50):
        sound = SFX.POP
        super().__init__(pos, delay, sound, z_index)


        

        if rarity == 'legendary':
            self.add_effect(
                LightningEffect(self.pos, 10, (255, 230, 0), (255, 150, 0), sound= None)  
            )

            self.add_effect(ScreenShakeEffect(0.8, 30, 30))
            self.add_effect(SoundEffect(SFX.POWER_UP))

        else:
            self.add_effect(ExplosionEffect(self.pos, 40, scale= 4, speed= (100,300), 
                                        color= (255, 255, 255), life_time= (0.5, 0.8), final_speed= 10))
            self.add_effect(ExplosionEffect(self.pos, 40, scale= 2, speed= (200,400), 
                                        color= (255, 255, 255), life_time= (0.6, 0.9), final_speed= 10))
            self.add_effect(ScreenShakeEffect(0.5, 10, 10))

        

class GunEffect(MultipleEffect):
    def __init__(self, pos, target_pos, bullet, barrel_offset = (0, 0), smoke_color_1 = None, 
                 smoke_color_2 = None, break_effect = None, break_intensity = 700,
                  delay=0, sound=SFX.GUN, z_index=50):
        super().__init__(pos, delay, sound, z_index)

        barrel_pos = self.pos + Vector2(barrel_offset)

        if break_effect is not None:
            self.add_effect(BreakEffect(target_pos, break_effect, intensity= break_intensity))

        self.add_effect(BloodEffect(target_pos, direction= target_pos - self.pos))

        if smoke_color_2 is not None:
            self.add_effect(
                ExplosionEffect(
                barrel_pos, amount= 100, speed= (400, 700), scale= 2, final_speed= 10, 
                life_time= (0.2, 0.3), kill_duration= (0.6, 0.9), color= smoke_color_2
            ))

        if smoke_color_1 is not None:
            self.add_effect(
                ExplosionEffect(
                barrel_pos, amount= 100, speed= (500, 900), scale= 1, final_speed= 10, 
                life_time= (0.2, 0.3), kill_duration= (0.6, 0.9), color= smoke_color_1
            ))

        self.add_effect(
            TargetEffect(
            barrel_pos, amount= 1, surface= bullet, 
            target= target_pos, life_time= 0.15,
            adaptative_angle= True, kill_duration= 0.1, z_index= 51
        ))

        self.add_effect(ScreenShakeEffect(0.5, 25, 25))
        self.add_effect((FlashEffect((255, 255, 255), 0.2, 255, 0.05)))

class ArrowEffect(MultipleEffect):
    def __init__(self, first_pos, last_pos, size = 1, overshoot = 0, delay=0, z_index=50):
        first_pos = Vector2(first_pos)
        last_pos = Vector2(last_pos)
        pos = (first_pos.x + last_pos.x)//2 , (first_pos.y + last_pos.y)//2
        super().__init__(pos, delay, None, z_index)


        arrow_image = load_image('arrow', PartConfig.ARROW)
        end_piece = get_image(arrow_image, 9, 6)
        mid_piece = get_image(arrow_image, 9, 6, frame_x= 1)
        start_piece = get_image(arrow_image, 9, 6, frame_x= 2)


        end_piece = resize(end_piece, size)
        mid_piece = resize(mid_piece, size)
        start_piece = resize(start_piece, size)
        width = end_piece.get_width()


        vector = last_pos - first_pos
        length = first_pos.distance_to(last_pos) + overshoot

        height = end_piece.get_height()
        mid_piece_height = max(0, length - height*2)

        mid_piece = pygame.transform.scale(mid_piece, (width, mid_piece_height))
        
        surface = pygame.Surface((width, length), pygame.SRCALPHA).convert_alpha()
        surface.blit(end_piece, (0, 0))
        surface.blit(start_piece, (0, mid_piece_height + height))
        surface.blit(mid_piece, (0, height))


        surface = pygame.transform.rotate(surface, vector.angle_to((0, -1)))

        self.add_effect(ParticleEffect(pos, 1, surface, life_time= 1, particle_type= GrowParticle, death_effect= ScaleDeath, kill_duration= 0.3))