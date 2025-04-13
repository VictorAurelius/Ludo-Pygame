"""Game constants and configuration"""

import pygame
from typing import Dict, Tuple

# Window dimensions
WINDOW_WIDTH = 925
WINDOW_HEIGHT = 725

# Board dimensions
TILE_SIZE = 25 
MAP_WIDTH = 29
MAP_HEIGHT = 29

# Game states
GAME_STATE_MENU = "menu"
GAME_STATE_PLAYING = "playing"
GAME_STATE_PAUSED = "paused"
GAME_STATE_TRANSITION = "transition"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
COLORS = {
    'Red': (255, 0, 0),
    'Blue': (0, 0, 255),
    'Yellow': (255, 255, 0),
    'Green': (0, 255, 0),
    'error_bg': (255, 200, 200, 200),
    'error_text': (200, 0, 0),
    'error_detail': (100, 0, 0),
    'text': (0, 0, 0),  # Default black text color
    'active_input': (240, 240, 240),
    'background': (255, 255, 255)  # Default white background
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

PAWN_IMAGES = {
    'Blue': 'assets/images/img/BluePawn.png',
    'Green': 'assets/images/img/GreenPawn.png',
    'Red': 'assets/images/img/RedPawn.png',
    'Yellow': 'assets/images/img/YellowPawn.png'
}

# Board positions and paths
BOARD_IMAGE = 'assets/images/img/LudoBoard-01.png'
STAR_IMAGE = 'assets/images/img/Star.png'

# Finish positions for each color (in grid coordinates)
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

# Path positions for each color
class PathPositions:
    """Board path positions for each color"""
    @staticmethod
    def scale_position(pos: Tuple[int, int]) -> Tuple[int, int]:
        """Scale grid position to pixel coordinates"""
        return (pos[0] * TILE_SIZE - 13, pos[1] * TILE_SIZE - 13)

    @staticmethod
    def scale_dict(positions: Dict[int, Tuple[int, int]]) -> Dict[int, Tuple[int, int]]:
        """Scale a dictionary of positions"""
        return {k: PathPositions.scale_position(v) for k, v in positions.items()}

RED_PATH = {
    # Start path
    1: (4, 11), 2: (5, 11), 3: (6, 11), 4: (7, 11),
    # Main path
    5: (8, 11), 6: (9, 11), 7: (10, 11), 8: (11, 11),
    # Continue clockwise...
    # Home path
    93: (4, 15), 94: (5, 15), 95: (6, 15), 96: (7, 15)
}

BLUE_PATH = {
    # Start path
    1: (13, 4), 2: (13, 5), 3: (13, 6), 4: (13, 7),
    # Main path
    5: (13, 8), 6: (13, 9), 7: (13, 10), 8: (13, 11),
    # Continue clockwise...
    # Home path
    93: (15, 4), 94: (15, 5), 95: (15, 6), 96: (15, 7)
}

YELLOW_PATH = {
    # Start path
    1: (26, 13), 2: (25, 13), 3: (24, 13), 4: (23, 13),
    # Main path
    5: (22, 13), 6: (21, 13), 7: (20, 13), 8: (19, 13),
    # Continue clockwise...
    # Home path
    93: (26, 15), 94: (25, 15), 95: (24, 15), 96: (23, 15)
}

GREEN_PATH = {
    # Start path
    1: (13, 26), 2: (13, 25), 3: (13, 24), 4: (13, 23),
    # Main path
    5: (13, 22), 6: (13, 21), 7: (13, 20), 8: (13, 19),
    # Continue clockwise...
    # Home path
    93: (15, 26), 94: (15, 25), 95: (15, 24), 96: (15, 23)
}

# Animation settings
ANIMATION_PATHS = {
    'Blue': 'assets/maps/mapfinal/WBlue_Animation.tsx',
    'Red': 'assets/maps/mapfinal/WBlue_Animation.tsx',
    'Yellow': 'assets/maps/mapfinal/WBlue_Animation.tsx',
    'Green': 'assets/maps/mapfinal/WBlue_Animation.tsx'
}

# Sprite groups
SPRITE_GROUPS = {
    'Red': pygame.sprite.Group(),
    'Blue': pygame.sprite.Group(),
    'Yellow': pygame.sprite.Group(),
    'Green': pygame.sprite.Group(),
    'All': pygame.sprite.Group()
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

# Placeholder definitions for missing constants
BOARD_POSITIONS = {
    1: (0, 0), 2: (1, 0), 3: (2, 0), 4: (3, 0)  # Example positions
}
RESTRICTED_POSITIONS = [1, 2]  # Example restricted positions
STAR_COUNT = 3  # Example star count

# Placeholder definition for MAP_PATH
MAP_PATH = "assets/maps/mapfinal/mapludo.tmx"  # Example map path