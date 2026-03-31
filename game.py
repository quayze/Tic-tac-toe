import pygame, sys
from settings import *
from tic_tac_toe import *
from player_interface import *
from screen_manager import ScreenManager
from effects_manager import *
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
            
            self.handle_input()
            self.run_game()
            self.render_game()


            resized_screen = pygame.transform.scale(self.screen.copy(), (window_width, window_height))
            self.display.blit(resized_screen, (0, 0))

            
            pygame.display.flip()


    def new_run(self):
        self.session = GameSession(self.player, self.guest, self)
        self.game = TicTacToe(self.session, self)
        self.inventories = self.session.inventories
        self.state = 'play'
        





    def handle_input(self):
        self.game.handle_input(self.mouse_pos)

        for inv in self.inventories.values():
            inv.handle_mouse(self.mouse_pos)

        if pygame.mouse.get_pressed()[1]:
            surface = get_marker('cat')
            surface = resize(surface, 3)
            self.add_effect(
                FallEffect(
                    self.mouse_pos, amount= 1, surface= load_image('q_mark_case', PartConfig.Q_MARK_SQUARE), scale_range= (PIXEL_SIZE, PIXEL_SIZE),
                    speed_range= (800, 1300), angle_offset= 30
                )
            )
            


    def run_game(self):
        if self.state == 'play':
            self.game.update(self.delta_time)
            for inv in self.inventories.values():
                inv.update(self.delta_time)

    def render_game(self):

        self.screen_manager.draw(self.screen)


    

    def add_object(self, object):
        self.screen_manager.add_object(object)

    def remove_object(self, object):
        self.screen_manager.add_removed_object(object)

    def add_effect(self, effect):
        self.effects_manager.add_effect(effect)
