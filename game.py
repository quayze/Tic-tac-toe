import pygame, sys
from settings import *
from tic_tac_toe import *
from shop import *
from player_interface import *
from game_managers import *
from effect import *
from particles import *

class Game:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        self.display = pygame.display.set_mode((info.current_w, info.current_h))
        self.background_screen = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
        self.screen = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
        pygame.display.set_caption('Tic Tac Toe')
        self.clock = pygame.time.Clock()
        

        self.player = Player(name= 'JOUEUR', markers_type= 'pointer', color_theme= 'red')
        self.guest = Player(name= 'GUEST', markers_type= 'sun', color_theme= 'blue')
        self.screen_manager = ScreenManager()
        self.effects_manager = EffectsManager(self)
        self.sound_manager = SoundManager()


        self.new_run()


        self.temp = False
        self.screen_offset = [0, 0]
        self.shake_trauma = 0


    def run(self):

        self.start_time = pygame.time.get_ticks()

        while True:
            self.clock.tick(FPS)
            self.delta_time = (pygame.time.get_ticks() - self.start_time)/1000
            self.start_time = pygame.time.get_ticks()

            self.screen.fill((0, 0, 0, 0))
            self.background_screen.fill((50, 0, 50))
            

            window_width, window_height = self.display.get_size()
            window_height = (self.display.get_width()*HEIGHT)/ WIDTH

            mouse_pos_x, mouse_pos_y  = pygame.mouse.get_pos()
            scale_x, scale_y = WIDTH/window_width, HEIGHT/window_height, 

            self.mouse_pos = (
                mouse_pos_x * scale_x,
                mouse_pos_y * scale_y
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            self.effects_manager.update(self.delta_time)
            
            self.handle_mouse()
            self.run_game()

            self.screen_manager.draw_background(self.background_screen)
            self.screen_manager.draw(self.screen)
            self.update_shake()

            resized_background = pygame.transform.scale(self.background_screen, (window_width, window_height))
            resized_screen = pygame.transform.scale(self.screen, (window_width, window_height))
            self.display.blit(resized_background, (0, 0))
            self.display.blit(resized_screen, self.screen_offset)

            
            pygame.display.flip()


    def new_run(self):
        self.session = GameSession(self.player, self.guest, self)
        self.tic_tac_toe = TicTacToe(self.session, self)
        self.shop = Shop(self.session, self)
        self.inventories = self.session.inventories.values()
        self.tic_tac_toe.start_playing()
        self.state = 'play'

    def next_phase(self):
        if self.state == 'play':
            self.state = 'shop'
            self.shop.open()

        elif self.state == 'shop':
            self.state = 'play'
            self.tic_tac_toe.start_playing()
        
    def handle_mouse(self):
        for inv in self.inventories:
            inv.handle_mouse(self.mouse_pos)

        if self.state == 'play':
            self.tic_tac_toe.handle_mouse(self.mouse_pos)

        elif self.state == 'shop':
            self.shop.handle_mouse(self.mouse_pos)

        if pygame.mouse.get_pressed()[2] and not self.temp:
            self.temp = True
            surf = get_marker('death_star')
            surf = resize(surf, PIXEL_SIZE)
            self.add_effect(
                LightningEffect(self.mouse_pos, 10, (255, 230, 0), (255, 150, 0), sound= None)  
            )

        elif not pygame.mouse.get_pressed()[2]:
            self.temp = False

    def update_shake(self):
        if self.shake_trauma <= 0:
            if self.screen_offset != [0, 0]: self.screen_offset = [0, 0]
            return
        
        self.shake_trauma -= self.delta_time
        intensity = (self.shake_trauma / self.max_trauma) ** 2
        self.screen_offset[0] = random.uniform(self.shake_offset_x[0], self.shake_offset_x[1]) * intensity
        self.screen_offset[1] = random.uniform(self.shake_offset_y[0], self.shake_offset_y[1]) * intensity


    def run_game(self):
        for inv in self.inventories:
            inv.update(self.delta_time)
        if self.state == 'play':
            self.tic_tac_toe.update(self.delta_time)
        elif self.state == 'shop':
            self.shop.update(self.delta_time)  
        
    def add_object(self, object):
        self.screen_manager.add_object(object)

    def remove_object(self, object):
        self.screen_manager.add_removed_object(object)

    def add_effect(self, effect):
        self.effects_manager.add_effect(effect)

    def play_sound(self, sound_path):
        self.sound_manager.play(sound_path)

    def effects_finished(self):
        return self.effects_manager.effects == [] and self.effects_manager.waiting_effects == []
    
    def add_screen_shake(self, duration, offset_x = (-20, 20), offset_y = (-20, 20)):
        self.shake_trauma = duration
        self.max_trauma = duration
        self.shake_offset_x = offset_x
        self.shake_offset_y = offset_y