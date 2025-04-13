"""Game constants"""

import pygame

# Window dimensions
WINDOW_WIDTH = 925
WINDOW_HEIGHT = 725

# Game states
GAME_STATE_MENU = "menu"
GAME_STATE_PLAYING = "playing"
GAME_STATE_PAUSED = "paused"
GAME_STATE_TRANSITION = "transition"

# Board dimensions
TILE_SIZE = 25 
MAP_WIDTH = 29
MAP_HEIGHT = 29

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
COLORS = {
    'Red': (255, 0, 0),
    'Blue': (0, 0, 255),
    'Yellow': (255, 255, 0),
    'Green': (0, 255, 0),
    'error_bg': (255, 200, 200, 200),     # Light red with alpha
    'error_text': (200, 0, 0),            # Dark red
    'error_detail': (100, 0, 0),          # Darker red
    'text': (0, 0, 0),                    # Black text
    'active_input': (240, 240, 240)       # Light gray for input highlight
}

# Button coordinates
ROLL_BUTTON = (735, 290, 180, 50)
TITLE_BUTTON = (745, 10, 160, 40)
TITLE_RANKING_BUTTON = (400, 400, 200, 50)
YES_BUTTON = (410, 260, 60, 30)
NO_BUTTON = (530, 260, 90, 30)
SOUND_BUTTON = (875, 10, 40, 40)

# Asset paths
DICE_IMAGES = [f'assets/images/img/{i}_block.png' for i in range(1, 7)]

# Board and piece images
PAWN_IMAGES = {
    'Blue': 'assets/images/img/BluePawn.png',
    'Green': 'assets/images/img/GreenPawn.png',
    'Red': 'assets/images/img/RedPawn.png',
    'Yellow': 'assets/images/img/YellowPawn.png'
}

# Animation tileset paths
ANIMATION_PATHS = {
    'Blue': 'assets/maps/mapfinal/WBlue_Animation.tsx',
    'Red': 'assets/maps/mapfinal/WBlue_Animation.tsx',
    'Yellow': 'assets/maps/mapfinal/WBlue_Animation.tsx',
    'Green': 'assets/maps/mapfinal/WBlue_Animation.tsx'
}

BOARD_IMAGE = 'assets/images/img/LudoBoard-01.png'
STAR_IMAGE = 'assets/images/img/Star.png'

# Star settings
STAR_COUNT = 15
STAR_EFFECTS = {
    'ROLL_AGAIN': 1,
    'TELEPORT': 2,
    'DIE': 0
}

# Restricted positions for star placement
RESTRICTED_POSITIONS = [
    1, 25, 49, 73,  # Starting positions
    93, 94, 95, 96, 97, 98, 99, 100,  # Home positions
    101, 102, 103, 104, 105, 106, 107, 108  # Home positions
]

# Board positions
BOARD_POSITIONS = {
    1: (4, 11), 2: (5, 11), 3: (6, 11), 4: (7, 11), 5: (8, 11),
    6: (9, 11), 7: (10, 11), 8: (11, 11), 9: (11, 10), 10: (11, 9),
    11: (11, 8), 12: (11, 7), 13: (11, 6), 14: (11, 5), 15: (11, 4),
    16: (11, 3), 17: (12, 3), 18: (13, 3), 19: (14, 3), 20: (15, 3),
    21: (16, 3), 22: (17, 3), 23: (18, 3), 24: (19, 3), 25: (19, 4),
    26: (19, 5), 27: (19, 6), 28: (19, 7), 29: (19, 8), 30: (19, 9),
    31: (19, 10), 32: (19, 11), 33: (20, 11), 34: (21, 11), 35: (22, 11),
    36: (23, 11), 37: (24, 11), 38: (25, 11), 39: (26, 11), 40: (27, 11),
    41: (27, 12), 42: (27, 13), 43: (27, 14), 44: (27, 15), 45: (27, 16),
    46: (27, 17), 47: (27, 18), 48: (27, 19), 49: (26, 19), 50: (25, 19),
    51: (24, 19), 52: (23, 19), 53: (22, 19), 54: (21, 19), 55: (20, 19),
    56: (19, 19), 57: (19, 20), 58: (19, 21), 59: (19, 22), 60: (19, 23),
    61: (19, 24), 62: (19, 25), 63: (19, 26), 64: (19, 27), 65: (18, 27),
    66: (17, 27), 67: (16, 27), 68: (15, 27), 69: (14, 27), 70: (13, 27),
    71: (12, 27), 72: (11, 27), 73: (11, 26), 74: (11, 25), 75: (11, 24),
    76: (11, 23), 77: (11, 22), 78: (11, 21), 79: (11, 20), 80: (11, 19),
    81: (10, 19), 82: (9, 19), 83: (8, 19), 84: (7, 19), 85: (6, 19),
    86: (5, 19), 87: (4, 19), 88: (3, 19), 89: (3, 18), 90: (3, 17),
    91: (3, 16), 92: (3, 15), 93: (4, 15), 94: (5, 15), 95: (6, 15),
    96: (7, 15), 97: (15, 4), 98: (15, 5), 99: (15, 6), 100: (15, 7),
    101: (26, 15), 102: (25, 15), 103: (24, 15), 104: (23, 15),
    105: (15, 26), 106: (15, 25), 107: (15, 24), 108: (15, 23),
    109: (3, 14), 110: (3, 13), 111: (3, 12), 112: (3, 11)
}

# Finish positions for each color
RED_FINISH_POSITIONS = {
    1: (9, 13), 2: (10, 13), 3: (12, 13), 4: (13, 13)
}

BLUE_FINISH_POSITIONS = {
    1: (13, 9), 2: (14, 9), 3: (16, 9), 4: (17, 9)
}

YELLOW_FINISH_POSITIONS = {
    1: (17, 13), 2: (18, 13), 3: (20, 13), 4: (21, 13)
}

GREEN_FINISH_POSITIONS = {
    1: (13, 17), 2: (14, 17), 3: (16, 17), 4: (17, 17)
}

# TMX configuration
TMX_CONFIG = {
    'main_menu': {
        'path': 'assets/UI/main_menu.tmx',
        'required_layers': ['ban', 'button'],
        'button_positions': {
            'play': (250, 300),
            'rules': (250, 375),
            'developers': (250, 450),
            'quit': (250, 525),
        }
    },
    'sp_menu': {
        'path': 'assets/UI/sp_menu.tmx',
        'required_layers': ['ban', 'bong'],
        'button_positions': {
            'back': (50, 600),
            'ok': (300, 600)
        }
    }
}

# Button positions
BUTTON_POSITIONS = {
    "play": (250, 300, 250, 50),      # Wider buttons to match TMX
    "rules": (250, 375, 250, 50),     # Adjusted vertical spacing
    "developers": (250, 450, 250, 50),
    "quit": (250, 525, 250, 50),
    "ok": (300, 600, 200, 50),
    "back": (50, 600, 200, 50)
}

# Button text
BUTTON_TEXT = {
    "play": "Chơi",
    "rules": "Luật chơi",
    "developers": "Nhà phát triển",
    "quit": "Thoát",
    "ok": "Đồng ý",
    "back": "Quay lại"
}

# Game rules
GAME_RULES = [
    "",
    "1. Mỗi người chơi có 4 quân cờ",
    "2. Tung 2 con xúc xắc để di chuyển quân",
    "3. Cần tung được tổng 2 con xúc xắc >= 10 để đưa",
    "    quân vào bàn cờ",
    "4. Quân có thể đá quân địch về chuồng nếu đứng cùng",
    "    ô với quân địch",
    "5. Người chơi phải đưa tất cả quân về đích để thắng",
    "6. Quân di chuyển số ô bằng tổng 2 con xúc xắc",
    "(Nếu khoảng cách từ quân đến đích nhỏ hơn 1 so với",
    "  tổng số xúc xắc thì quân đó vẫn có thể về đích)"
]

# Sprite groups for pawns
PAWN_GROUPS = {
    'Red': pygame.sprite.Group(),
    'Blue': pygame.sprite.Group(),
    'Yellow': pygame.sprite.Group(),
    'Green': pygame.sprite.Group(),
    'All': pygame.sprite.Group()
}