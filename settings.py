WIDTH = 1920
HEIGHT = 1080

FPS = 60

PIXEL_SIZE = 10
TEXT_FONT = 'assets/FreakyFont.otf'

class MarkerConfig:
    MARKER_SIZE = 13
    MARKERS_SHEET = 'assets/textures/markers.png'
    MARKERS_TYPE = ['cross', 'round']

class CaseConfig:
    CASE_SHEET = 'assets/textures/cases.png'
    CASE_SIZE = 19
    RARITY_PERCENTAGE = {
        'common' : 0.5,
        'rare' : 0.2,
        'legendary' : 0.05
    }

class NineSliceConfig:
    CORNER_IMAGE = 'assets/textures/corner.png'

class TableConfig:
    OFFSET = 20
    WINNING_COMBINATION = [
        [0, 1, 2],  # ligne haute
        [3, 4, 5],  # ligne milieu
        [6, 7, 8],  # ligne basse
        [0, 3, 6],  # colonne gauche
        [1, 4, 7],  # colonne milieu
        [2, 5, 8],  # colonne droite
        [0, 4, 8],  # diagonale
        [2, 4, 6],  # diagonale
    ]

class InterfacesConfig:
    MAKER_CONTAINER_OFFSET = 80
    PLAYER_INV_OFFSET = 50
    PLAYER_INV_HEIGHT = 200
    MARKER_CONTAINER_WIDTH = 200
    PLAYER_BALANCE_WIDTH = 400
    PLAYER_INV_WIDTH = 700


class ItemConfig:
    ITEM_SIZE = 100