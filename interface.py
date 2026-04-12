import pygame
from settings import *
from functions import *
from drawable import *
from pygame import Vector2 as V2
from button import *
from shadow import *
from effect import *
from swiper import *

class Interface(Drawable):
    def __init__(self, game, base_pos, active_pos, width, height, color, center_color):
        super().__init__(1)
        self.state = 'disable'
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
        self.rect = self.surface.get_rect(center = base_pos)
        self.surf_image = generate_nine_slice(width, height, color, center_color= center_color)
        self.game = game


        self.screen_center = V2(WIDTH//2, HEIGHT//2)
        self.center = V2(self.surface.get_width()//2, self.surface.get_height()//2)
        self.pos = V2(base_pos)
        self.base_pos = V2(base_pos)
        self.active_pos = V2(active_pos)

        self.shadow = Shadow(self.pos)
        self.shadow.set_image(self.surf_image)
        self.shadow.set_parallax(x_abs= 10, y_abs= 10)

        self.open_time = 0.5

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
        self.surface.blit(self.surf_image, (0, 0))
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
            if len(self.elements) == 1:
                self.add_page_button(0)

            page = len(self.elements)
            self.elements.append({})
            self.add_page_button(page)

        if name not in self.elements[page]:
            self.elements[page][name] = element

    def add_page_button(self, page_index):
        button = Button((100, 100 * (page_index + 1)), 150, 50, color= (200, 0, 0), text= [f'Page {page_index}'], pixel_size= 4)
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
    def __init__(self, game):
        self.screen_center = V2(WIDTH//2, HEIGHT//2)
        super().__init__(game, (-300, self.screen_center.y), (200, self.screen_center.y), 600, 500, (255, 255, 255), (100, 0, 100))
        self.add_element('skip_button', Button((300, self.center.y), 250, 30, (255, 200, 0), ['Skip turn'], 30))


class PlayInterface(Interface):
    def __init__(self, game, base_pos, active_pos):
        self.screen_center = V2(WIDTH//2, HEIGHT//2)
        super().__init__(game, base_pos, active_pos, 1200, 800, (255, 255, 255), (100, 100, 100))
        self.add_element('play', Button((self.center.x, self.center.y+ 200), 250, 100, (0, 210, 80), ['Start'], 30, 4))
        self.add_element('back', Button((self.center.x, self.center.y + 330), 500, 60, (255, 210, 0), ['Back'], 30, 4))


        cross = get_marker('cross')
        p1_maker_swiper = Swiper((self.center.x - 200, self.center.y), SwiperImage(cross, 10), 'cross')
        for name in MarkerConfig.MARKERS_TYPE[1:]:
            p1_maker_swiper.add_element(name, SwiperImage(get_marker(name), 10))

        self.add_element('maker_selector_1', p1_maker_swiper)

        p2_maker_swiper = Swiper((self.center.x + 200, self.center.y), SwiperImage(cross, 10), 'cross')
        for name in MarkerConfig.MARKERS_TYPE[1:]:
            p2_maker_swiper.add_element(name, SwiperImage(get_marker(name), 10))

        self.add_element('maker_selector_2', p2_maker_swiper)


    def get_p1_marker(self):
        selector : Swiper = self.get_element('maker_selector_1')
        return selector.get_active_name()
    
    def get_p2_marker(self):
        selector : Swiper = self.get_element('maker_selector_2')
        return selector.get_active_name()











    
    


    
