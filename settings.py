WIDTH = 1920
HEIGHT = 1080

FPS = 60

PIXEL_SIZE = 10
TEXT_FONT = 'assets/FreakyFont.otf'

class MarkerConfig:
    MARKER_SIZE = 13
    MARKERS_SHEET = 'assets/textures/markers.png'
    MARKERS_TYPE = ['cross', 'round']

class SquareConfig:
    CASE_SHEET = 'assets/textures/squares.png'
    CASE_SIZE = 19
    # RARITY SETTINGS
    RARITY_WEIGHTS = {
        'common' : 60,
        'rare' : 20,
        'legendary' : 5,
        'null' : 0
    }
    RARITY_COLORS = {
        'common' : (0, 100, 255),
        'rare' : (255, 0, 0),
        'legendary' : (255, 150, 0),
        'null' : (0, 0, 0)
    }
    BUY_PRICE = {
        'common' : 5,
        'rare' : 10,
        'legendary' : 25,
        'null' : 0
    }
    SELL_PRICE = {
        'common' : 2,
        'rare' : 5,
        'legendary' : 15,
        'null' : 0
    }

class NineSliceConfig:
    CORNER_IMAGE = 'assets/textures/nineSlice/corner.png'
    EMPTY_CORNER = 'assets/textures/nineSlice/emptyCorner.png'
    PIXEL_SIZE = 6

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
    PLAYER_INV_HEIGHT = 250
    MARKER_CONTAINER_WIDTH = 200
    PLAYER_BALANCE_WIDTH = 400
    PLAYER_INV_WIDTH = 700


class ItemConfig:
    ITEM_SIZE = 100

class PopupConfig:
    TEXT_SIZE = 30
    TITLE_SIZE = 60

class ShadowConfig:
    DEFAULT = {'x_mult' : 0.05, 'y_abs' : 20}
    STRONG = {'x_mult' : 0.10, 'y_abs' : 60}
    MINIMAL = {'x_mult' : 0.01, 'y_abs' : 10}
    BOTTOM = {'y_abs' : 10}



class ColorThemes:
    BLUE = {
        'm_container' : (60, 60, 255),
        'money_ui' : (0, 255, 200),
        'case_inv' : (30, 30, 180)
    }
    RED = {
        'm_container' : (180, 30, 30),
        'money_ui' : (255, 180, 0),
        'case_inv' : (150, 0, 0)
    }

class PartConfig:
    BULLET = 'assets/textures/particles/bullet.png'
    Q_MARK_SQUARE = 'assets/textures/particles/questionSquare.png'
    GHOST = 'assets/textures/particles/ghost.png'
    REWIND = 'assets/textures/particles/rewind.png'
    COIN = 'assets/textures/particles/coin.png'
    SHOOT = 'assets/textures/particles/shoot.png'
    WIN_CHECK = 'assets/textures/particles/winCheck.png'

class SFX:
    GUN = 'assets/sounds/gun.mp3'
    CASH = 'assets/sounds/cashOut.mp3'
    EXPLOSION = 'assets/sounds/explosion.mp3'
    POP = 'assets/sounds/pop.mp3'
    BREAKING = 'assets/sounds/break.mp3'
    TELEPORTATION = 'assets/sounds/teleport.mp3'
    SCRATCH = 'assets/sounds/scratch.mp3'
    SHUFFLE = 'assets/sounds/shuffle.mp3'
    COIN_DROP = 'assets/sounds/coinDrop.mp3'
    LIGHTNING = 'assets/sounds/lightning.mp3'
    DEATH = 'assets/sounds/death.mp3'
    WIN = 'assets/sounds/win.mp3'
    POWER_UP = 'assets/sounds/powerUp.mp3'
    LASER = 'assets/sounds/laser.mp3'