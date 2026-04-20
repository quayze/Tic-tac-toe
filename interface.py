import pygame
from settings import *
from functions import *
from drawable import *
from pygame import Vector2 as V2
from button import *
from shadow import *
from effect import *
from swiper import *
from text import *

class Interface(Drawable):
    def __init__(self, game, base_pos, active_pos, width, height, color, center_color, z_index = 1):
        super().__init__(z_index)
        self.state = 'disable'
        self.surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA).convert_alpha()
        self.rect = self.surface.get_rect(center = base_pos)
        self.surf_image = generate_nine_slice(width, height, color, center_color= center_color)
        self.surf_rect = self.surf_image.get_rect(center = (self.surface.get_width()//2, self.surface.get_height()//2))
        self.game = game


        self.center = V2(WIDTH//2, HEIGHT//2)
        self.pos = V2(base_pos)
        self.base_pos = V2(base_pos)
        self.active_pos = V2(active_pos)

        self.shadow = Shadow(self.pos)
        self.shadow.set_image(self.surf_image)
        self.shadow.set_parallax(x_abs= 10, y_abs= 10)

        self.open_time = 0.5
        self.instant_close = True

        self.elements = [{}]
        self.page_buttons : list[Button] = []
        self.index = 0

    def handle_mouse(self, mouse_pos):
        mouse_pos = V2(mouse_pos) - V2(self.rect.topleft)
        for button in self.page_buttons:
            button.handle_mouse(mouse_pos)
        for element in self.browse_elements():
            if hasattr(element, 'handle_mouse'):
                element.handle_mouse(mouse_pos)

    def update(self, dt):
        self.shadow.update(self.rect.center)
        self.update_opening(dt)
        self.update_closing(dt)
        for element in self.browse_elements():
            element.update(dt)


    def draw(self, screen):
        self.shadow.draw(screen)
        self.surface.fill((0, 0, 0, 0))
        self.surface.blit(self.surf_image, self.surf_rect)
        for element in self.browse_elements():
            element.draw(self.surface)

        for button in self.page_buttons:
            button.draw(self.surface)

        screen.blit(self.surface, self.rect)

    def activate(self):
        if self.state == 'disable':
            self.state = 'open'
            self.game.add_object(self)
            self.start_pos = V2(self.pos)
            self.duration = self.open_time
            self.current_time = 0

    def desactivate(self):
        if self.state == "enable":
            if self.instant_close:
                self.state = "disable"
                self.pos = V2(self.base_pos)
                self.rect.center = self.pos
                self.game.remove_object(self)
                return

            self.state = 'close'
            self.start_pos = V2(self.pos)
            self.duration = self.open_time
            self.current_time = 0

    def update_opening(self, dt):
        if self.state == 'open':
            progression = self.current_time / self.duration
            self.pos = self.start_pos + (self.active_pos - self.start_pos) * ease_out_quart(progression)
            self.current_time += dt

            self.rect.center = self.pos
            if progression >= 1:
                self.pos = V2(self.active_pos)
                self.rect.center = self.pos
                self.state = "enable"

    def update_closing(self, dt):
        if self.state == 'close':
            progression = self.current_time / self.duration
            self.pos = self.start_pos + (self.base_pos - self.start_pos) * progression
            self.current_time += dt

            self.rect.center = self.pos
            if progression >= 1:
                self.pos = V2(self.base_pos)
                self.rect.center = self.pos
                self.state = "disable"

    def add_element(self, name, element, page = 0):
        if page >= len(self.elements):
            page = len(self.elements)
            self.elements.append({})

        if name not in self.elements[page]:
            self.elements[page][name] = element

    def add_page_button(self, page_index, title, color, width):
        init_pos = (self.surf_rect.left + (width//2) + 50)
        button = Button((init_pos + (width + 20) * page_index, self.surf_rect.top + 60), width, 70, color= color, text= title, pixel_size= 4)
        button.on_release = self._make_page_callback(page_index)

        self.page_buttons.append(button)

    def get_element(self, name):
        for page in self.elements:
            if name in page:
                return page[name]
            
        
    def is_closed(self):
        return self.state == 'disable'
    def is_open(self):
        return self.state == 'enable'
    
    def browse_elements(self):
        return self.elements[self.index].values()
    
    def change_page(self, page = 0):
        self.index = page if page < len(self.elements) else self.index

    def _make_page_callback(self, page_index):
        def callback():
            self.change_page(page_index)
        return callback



class GameInterface(Interface):
    def __init__(self, game, z_index = 1):
        self.screen_center = V2(WIDTH//2, HEIGHT//2)
        super().__init__(game, (-300, self.screen_center.y), (200, self.screen_center.y), 600, 500, (255, 255, 255), (100, 0, 100), z_index)
        self.add_element('skip_button', Button((self.center.x +100, self.center.y), 250, 30, (255, 200, 0), ['Skip turn'], 30))


class PlayInterface(Interface):
    def __init__(self, game, base_pos, active_pos, z_index = 1):
        self.screen_center = V2(WIDTH//2, HEIGHT//2)
        super().__init__(game, base_pos, active_pos, 1200, 800, (255, 255, 255), (100, 100, 100), z_index)
        self.add_element('play', Button((self.center.x, self.center.y+ 200), 300, 100, (0, 210, 80), ['Start'], 30, 4))
        self.add_element('back', Button((self.center.x, self.center.y + 320), 800, 60, (255, 210, 0), ['Back'], 30, 4))


        p1_maker_swiper = Swiper((self.center.x - 300, self.center.y + 50))
        for name in MarkerConfig.MARKERS_TYPE:
            p1_maker_swiper.add_element(name, SwiperImage(get_marker(name), 10))

        self.add_element('maker_selector_1', p1_maker_swiper)

        p2_maker_swiper = Swiper((self.center.x + 300, self.center.y + 50))
        for name in MarkerConfig.MARKERS_TYPE:
            p2_maker_swiper.add_element(name, SwiperImage(get_marker(name), 10))

        self.add_element('maker_selector_2', p2_maker_swiper)

        p1_color_swiper = Swiper((self.center.x - 300, self.center.y - 100))
        p2_color_swiper = Swiper((self.center.x + 300, self.center.y - 100))
        self.add_element('color_selector_1', p1_color_swiper)
        self.add_element('color_selector_2', p2_color_swiper)
        blue_surf = generate_nine_slice(100, 100, (0, 0, 255), pixel_size= 4)
        red_surf = generate_nine_slice(100, 100, (255, 0, 0), pixel_size= 4)
        green_surf = generate_nine_slice(100, 100, (0, 255, 0), pixel_size= 4)
        p1_color_swiper.add_element('blue', SwiperImage(blue_surf, 1))
        p1_color_swiper.add_element('red', SwiperImage(red_surf, 1))
        p1_color_swiper.add_element('green', SwiperImage(green_surf, 1))
        p2_color_swiper.add_element('blue', SwiperImage(blue_surf, 1))
        p2_color_swiper.add_element('red', SwiperImage(red_surf, 1))
        p2_color_swiper.add_element('green', SwiperImage(green_surf, 1))

        self.add_element('p1_text', AnimText('Player 1', 70, (self.center.x - 300, self.center.y - 230), auto_start= True))
        self.add_element('p2_text', AnimText('Player 2', 70, (self.center.x + 300, self.center.y - 230), auto_start= True))
        self.add_element('color', AnimText('Colors', 40, (self.center.x, self.center.y - 100)))
        self.add_element('marker', AnimText('Markers', 40, (self.center.x, self.center.y + 50)))

        self.add_element('2P_mode', AnimText('2 PLAYERS MODE', 70, (self.center.x, self.surf_rect.top - 80)))
        self.add_element('1P_mode', AnimText('1 PLAYER MODE', 70, (self.center.x, self.surf_rect.top - 80)), page= 1)

        self.add_page_button(0, ['2 players'], (200, 0 , 0), 400)
        self.add_page_button(1, ['Singleplayer'], (200, 0 , 0), 400)

    def get_p1_marker(self):
        selector : Swiper = self.get_element('maker_selector_1')
        return selector.get_active_name()
    
    def get_p2_marker(self):
        selector : Swiper = self.get_element('maker_selector_2')
        return selector.get_active_name()
    
    def get_p1_color(self):
        selector : Swiper = self.get_element('color_selector_1')
        return selector.get_active_name()
    
    def get_p2_color(self):
        selector : Swiper = self.get_element('color_selector_2')
        return selector.get_active_name()
    












    
    


    
