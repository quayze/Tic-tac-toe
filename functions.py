import pygame
from settings import *
import random

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


def generate_nine_slice(width = 0, height = 0, color = (255, 255, 255), pixel_size = 6):

    corner = load_image('nine_slice_corner', NineSliceConfig.CORNER_IMAGE)
    corner = resize(corner, pixel_size)

    corner_width = corner.get_width()
    corner_height = corner.get_height()
    if width < corner_width * 2:
        width = corner_width * 2
    if height < corner_height * 2:
        height = corner_height * 2
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    

    surface.blit(corner, (0,0))
    surface.blit(pygame.transform.flip(corner, True, False), (width - corner_width, 0))
    surface.blit(pygame.transform.flip(corner, False, True), (0, height - corner_height))
    surface.blit(pygame.transform.flip(corner, True, True), (width - corner_width, height - corner_height))


    horizontal_edge = pygame.Surface((width - corner_width*2, corner_height)).convert()
    horizontal_edge.fill((255, 255, 255))
    vertical_edge = pygame.Surface((corner_width, height - corner_height*2)).convert()
    vertical_edge.fill((255, 255, 255))


    surface.blit(horizontal_edge , (corner_width, 0))
    surface.blit(horizontal_edge, (corner_width, height - corner_height))
    surface.blit(vertical_edge, (0, corner_height))
    surface.blit(vertical_edge, (width - corner_width, corner_height))
    
    center_piece = pygame.Surface((width - corner_width*2, height - corner_height*2)).convert()
    center_piece.fill((255, 255, 255))
    surface.blit(center_piece, (corner_width, corner_height))

    surface.fill(color, special_flags= pygame.BLEND_RGBA_MULT)

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
    
    else:
        return get_image(markers, MarkerConfig.MARKER_SIZE, MarkerConfig.MARKER_SIZE)