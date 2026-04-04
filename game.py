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
        self.screen = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
        pygame.display.set_caption('Tic Tac Toe')
        self.clock = pygame.time.Clock()

        self.player = Player(name= 'JOUEUR', markers_type= 'cross', color_theme= 'red')
        self.guest = Player(name= 'GUEST', markers_type= 'round', color_theme= 'blue')
        self.screen_manager = ScreenManager()
        self.effects_manager = EffectsManager(self)
        self.sound_manager = SoundManager()

        self.new_run()


    def run(self):

        self.start_time = pygame.time.get_ticks()

        while True:
            self.clock.tick(FPS)
            self.delta_time = (pygame.time.get_ticks() - self.start_time)/1000
            self.start_time = pygame.time.get_ticks()

            self.screen.fill((50, 0, 50))

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
            self.render_game()


            resized_screen = pygame.transform.scale(self.screen.copy(), (window_width, window_height))
            self.display.blit(resized_screen, (0, 0))

            
            pygame.display.flip()


    def new_run(self):
        self.session = GameSession(self.player, self.guest, self)
        self.tic_tac_toe = TicTacToe(self.session, self)
        self.shop = Shop(self.session, self)
        self.inventories = self.session.inventories.values()
        self.state = 'play'

    def next_phase(self):
        if self.state == 'play':
            self.state = 'shop'
            self.shop.open()

        elif self.state == 'shop':
            self.state = 'play'
            self.tic_tac_toe.reset()
        





    def handle_mouse(self):
        for inv in self.inventories:
            inv.handle_mouse(self.mouse_pos)

        if self.state == 'play':
            self.tic_tac_toe.handle_input(self.mouse_pos)

        elif self.state == 'shop':
            self.shop.handle_mouse(self.mouse_pos)



        if pygame.mouse.get_pressed()[2]:
            surf = get_marker('cross')
            self.add_effect(
                FallEffect(
                    self.mouse_pos, amount= 20, surface= surf, scale_range= (3, 3),
                    speed_range= (800, 1800), angle_offset= 30, angle_range= (-180, 180)
                )
            )
            





    def run_game(self):
        for inv in self.inventories:
            inv.update(self.delta_time)
        if self.state == 'play':
            self.tic_tac_toe.update(self.delta_time)
        elif self.state == 'shop':
            self.shop.update(self.delta_time)  




    def render_game(self):
        self.screen_manager.draw(self.screen)


    

    def add_object(self, object):
        self.screen_manager.add_object(object)

    def remove_object(self, object):
        self.screen_manager.add_removed_object(object)

    def add_effect(self, effect):
        self.effects_manager.add_effect(effect)

    def play_sound(self, sound_path):
        self.sound_manager.play(sound_path)