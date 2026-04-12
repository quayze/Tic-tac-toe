import pygame
from settings import *
import math
import random
import json

def perfect_rezize(image : pygame.Surface, width = None, height = None):
    if width is not None:
        height = image.get_height() * width / image.get_width()
        image = pygame.transform.scale(image, (width, height))
    elif height is not None:
        width = image.get_width() * height / image.get_height()
        image = pygame.transform.scale(image, (width, height))
    return image

def resize(image, size):
    resized_image = pygame.transform.scale(image, (image.get_width()* size, image.get_height() * size))
    return resized_image




assests_dict = {}
def load_image(image_name, image_path : str):
    """Récupère une une image du dictionnaire de référence ou l'ajoute"""
    if image_name not in assests_dict:
        image = pygame.image.load(image_path).convert_alpha()
        assests_dict[image_name] = image
    return assests_dict[image_name]

def add_image(image_name, image):
    if image_name not in assests_dict:
        assests_dict[image_name] = image



def get_image(sprite_sheet, width, height, frame_x = 0, frame_y = 0):
    image = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    image.blit(sprite_sheet, (0, 0), ((frame_x* width), (frame_y* height), width, height))
    return image

font_cache = {}
def get_font(size):
    """Récupère la police d'écriture"""
    if size not in font_cache:
        font_cache[size] = pygame.font.Font(TEXT_FONT, size)
        
    return font_cache[size]


def generate_nine_slice(width = 0, height = 0, color = (255, 255, 255), pixel_size = NineSliceConfig.PIXEL_SIZE, center_color = None, center_alpha = 255):

    center_color = color if center_color is None else center_color

    corner = load_image('empty_nine_slice_corner', NineSliceConfig.EMPTY_CORNER)
    corner = resize(corner, pixel_size)
    corner.fill(color, special_flags= pygame.BLEND_RGBA_MULT)

    corner_width = corner.get_width()
    corner_height = corner.get_height()
    if width < corner_width * 2:
        width = corner_width * 2
    if height < corner_height * 2:
        height = corner_height * 2
    surface = pygame.Surface((width, height), pygame.SRCALPHA)

    center_piece = pygame.Surface((width - pixel_size*4, height - pixel_size*4), pygame.SRCALPHA).convert_alpha()
    center_piece.fill(center_color)
    center_piece.set_alpha(center_alpha)
    surface.blit(center_piece, (pixel_size*2, pixel_size*2))
    

    surface.blit(corner, (0,0))
    surface.blit(pygame.transform.flip(corner, True, False), (width - corner_width, 0))
    surface.blit(pygame.transform.flip(corner, False, True), (0, height - corner_height))
    surface.blit(pygame.transform.flip(corner, True, True), (width - corner_width, height - corner_height))


    horizontal_edge = pygame.Surface((width - corner_width*2, 2*pixel_size)).convert()
    horizontal_edge.fill(color)
    vertical_edge = pygame.Surface((2 * pixel_size, height - corner_height*2)).convert()
    vertical_edge.fill(color)
    surface.blit(horizontal_edge , (corner_width, 0))
    surface.blit(horizontal_edge, (corner_width, height - 2*pixel_size))
    surface.blit(vertical_edge, (0, corner_height))
    surface.blit(vertical_edge, (width - 2*pixel_size, corner_height))

    return surface




def get_text_surface(text_input, size = 100, color = (255, 255, 255)):
    font : pygame.font.Font = get_font(size=size)
    text_input = str(text_input)
    text_surface = font.render(text_input, True, color)
    return text_surface



def get_color(interface, color_theme):
    if color_theme == 'blue':
        return ColorThemes.BLUE[interface]
    elif color_theme == 'red':
        return ColorThemes.RED[interface]
    
    

#recupère une image en fonction d'un type
def get_marker(marker_type):
    markers = load_image('marker', MarkerConfig.MARKERS_SHEET)
    if marker_type == 'cross':
        return get_image(markers, MarkerConfig.MARKER_SIZE, MarkerConfig.MARKER_SIZE)
    
    elif marker_type == 'round':
        return get_image(markers, MarkerConfig.MARKER_SIZE, MarkerConfig.MARKER_SIZE, frame_x= 1)
    
    elif marker_type == 'donut':
        return get_image(markers, MarkerConfig.MARKER_SIZE, MarkerConfig.MARKER_SIZE, frame_x= 2)
    
    elif marker_type == 'nugget_guy':
        return get_image(markers, MarkerConfig.MARKER_SIZE, MarkerConfig.MARKER_SIZE, frame_x= 3)
    
    elif marker_type == 'cat':
        return get_image(markers, MarkerConfig.MARKER_SIZE, MarkerConfig.MARKER_SIZE, frame_x= 4)
    
    elif marker_type == 'death_star':
        return get_image(markers, MarkerConfig.MARKER_SIZE, MarkerConfig.MARKER_SIZE, frame_x= 0, frame_y=1)
    
    elif marker_type == 'vert_cross':
        return get_image(markers, MarkerConfig.MARKER_SIZE, MarkerConfig.MARKER_SIZE, frame_x= 1, frame_y=1)
    
    elif marker_type == 'sword':
        return get_image(markers, MarkerConfig.MARKER_SIZE, MarkerConfig.MARKER_SIZE, frame_x= 2, frame_y=1)
    
    elif marker_type == 'sun':
        return get_image(markers, MarkerConfig.MARKER_SIZE, MarkerConfig.MARKER_SIZE, frame_x= 3, frame_y=1)
    
    elif marker_type == 'pointer':
        return get_image(markers, MarkerConfig.MARKER_SIZE, MarkerConfig.MARKER_SIZE, frame_x= 4, frame_y=1)
    
    else:
        return get_image(markers, MarkerConfig.MARKER_SIZE, MarkerConfig.MARKER_SIZE)
    

def get_text_dimensions(text, size, type = 'height'):
    font : pygame.font.Font = get_font(size)
    if type == 'height':
        return font.size(text)[1]
    else:
        return font.size(text)[0]
    


squares_data = None
def get_square_data(square_class_name):
    global squares_data
    if squares_data is None:
        with open('data/squares_data.json', 'r') as f:
            squares_data = json.load(f)
    return squares_data.get(square_class_name, {
        "name": square_class_name,
        "description": "",
        "rarity": "common"
    })

def get_all_squares_data():
    global squares_data
    if squares_data is None:
        with open('data/squares_data.json', 'r') as f:
            squares_data = json.load(f)
    return squares_data


def get_warp_text(text : str, size, width, color = (255, 255, 255)):
    final_surfaces = []


    elements = text.split(' ')
    offset = 10
    height = 0
    current_string = ''
    for txt in elements:
        test_string = current_string + txt + ' '
        if get_text_dimensions(test_string, size, 'width') > width:
            txt_surf = get_text_surface(current_string.strip(), size, color)
            txt_rect = txt_surf.get_rect(midtop = (width//2, height))
            final_surfaces.append([txt_surf, txt_rect])
            height += txt_rect.height + offset
            current_string = txt + ' '
        else:
           current_string = test_string

    txt_surf = get_text_surface(current_string.strip(), size, color)
    txt_rect = txt_surf.get_rect(midtop = (width//2, height))
    final_surfaces.append([txt_surf, txt_rect])
    height += txt_rect.height

    surface = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    for text_info in final_surfaces:
        surface.blit(text_info[0], text_info[1])

    return surface


def generate_round(pixel_size = 10, radius = 100, color = (255, 255, 255)):


    scaled_radius = radius // pixel_size if pixel_size <= radius else radius

    surface = pygame.Surface((scaled_radius*2, scaled_radius*2), pygame.SRCALPHA).convert_alpha()
    pygame.draw.circle(surface, color, (scaled_radius, scaled_radius), scaled_radius)
    surface = pygame.transform.scale(surface, (radius * 2, radius * 2))

    return surface

def rand(tuple_int, int_mode = False):
    if isinstance(tuple_int, int) or isinstance(tuple_int, float):
        return tuple_int
    else:
        lo, hi = tuple_int
        if lo >= hi:
            return lo
        else:
            if int_mode:
                return random.randint(lo, hi)
            else:
                return random.uniform(lo, hi)


    

def ease_out_back(t, s=1.70158):
    return 1 + (s + 1) * (t - 1)**3 + s * (t - 1)**2

def ease_out_bounce(t):
    n1 = 7.5625
    d1 = 2.75

    if (t < 1 / d1) :
        return n1 * t * t
    
    elif (t < 2 / d1) :
        t -= 1.5 / d1
        return n1 * t * t + 0.75
    
    elif (t < 2.5 / d1) :
        t -= 2.25 / d1
        return n1 * t * t + 0.9375
    
    else :
        t -= 2.625 / d1
        return n1 * t * t + 0.984375
    
def ease_out_elastic(t: float, weakness = 20) -> float:
    c4 = (2 * math.pi) / 3

    if t == 0:
        return 0
    if t == 1:
        return 1

    return pow(2, -weakness * t) * math.sin((t * 10 - 0.75) * c4) + 1

def ease_out_quart(t):
    return 1 - pow(1 - t, 4)


