"""Menu configuration constants"""

# Menu content matching TMX banner positions
MENU_TEXT = {
    "main": {
        "title": {"text": "LUDO", "pos": (400, 125)},
        "buttons": [
            {"text": "Play Game", "pos": (400, 400)},
            {"text": "Rules", "pos": (400, 470)},
            {"text": "Developers", "pos": (400, 540)},
            {"text": "Exit", "pos": (400, 610)}
        ]
    },
    "rules": {
        "title": {"text": "Rules", "pos": (400, 150)},
        "content": [
            {"text": "1. Each player has 4 pieces", "pos": (400, 300)},
            {"text": "2. Roll a 6 to move a piece out", "pos": (400, 340)},
            {"text": "3. Move pieces based on dice roll", "pos": (400, 380)},
            {"text": "4. Capture opponent's piece on the same spot", "pos": (400, 420)},
            {"text": "5. Special effects on star tiles", "pos": (400, 460)},
            {"text": "6. Bring all 4 pieces home to win", "pos": (400, 500)}
        ],
        "buttons": [
            {"text": "Back", "pos": (400, 610)}
        ]
    },
    "developers": {
        "title": {"text": "Developers", "pos": (400, 150)},
        "content": [
            {"text": "Development Team:", "pos": (400, 300)},
            {"text": "1. Nguyen Van Kiet - Developer", "pos": (400, 380)},
            {"text": "2. Nguyen Tai Nhat - Developer", "pos": (400, 420)},
            {"text": "3. Vu Minh Quyet - Developer", "pos": (400, 460)}
        ],
        "buttons": [
            {"text": "Back", "pos": (400, 610)}
        ]
    },
    "name_input": {
        "title": {"text": "Enter Player Names", "pos": (400, 150)},
        "buttons": [
            {"text": "Back", "pos": (300, 590)},
            {"text": "Start", "pos": (500, 590)}
        ]
    }
}

# Button click areas matched with TMX button layer
BUTTON_REGIONS = {
    "main": [
        {"rect": (320, 380, 160, 40), "action": "start_game"},
        {"rect": (320, 450, 160, 40), "action": "rules"},
        {"rect": (320, 520, 160, 40), "action": "developers"},
        {"rect": (320, 590, 160, 40), "action": "exit"}
    ],
    "rules": [
        {"rect": (300, 590, 200, 40), "action": "main"}
    ],
    "developers": [
        {"rect": (300, 590, 200, 40), "action": "main"}
    ],
    "name_input": [
        {"rect": (250, 570, 100, 40), "action": "main"},
        {"rect": (450, 570, 100, 40), "action": "start"}
    ]
}

# Layer configurations with explicit ordering and properties
LAYER_CONFIG = {
    'water': {'order': 1, 'alpha': 255},
    'rock': {'order': 2, 'alpha': 255},
    'grass': {'order': 3, 'alpha': 255},
    'tree': {'order': 4, 'alpha': 255},
    'deco': {'order': 5, 'alpha': 255},
    'ban': {'order': 6, 'alpha': 255, 'use_offset': True},
    'button': {'order': 7, 'alpha': 255, 'use_offset': True},
    'bong': {'order': 8, 'alpha': 200, 'use_offset': True}
}

# Font configuration
FONTS = {
    'title': {
        'name': "notosans",
        'size': 90,
        'color': (0, 0, 0)  # Black
    },
    'menu': {
        'name': "notosans",
        'size': 42,
        'color': (0, 0, 0)  # Black
    },
    'content': {
        'name': "notosans",
        'size': 36,
        'color': (0, 0, 0)  # Black
    }
}

# Color configuration
COLORS = {
    'normal': (0, 0, 0),       # Black for normal text
    'hover': (255, 165, 0),    # Orange for hover
    'click': (220, 20, 60),    # Red for click
    'title': (0, 0, 0),        # Black for title
    'background': (0, 0, 0),   # Black for background
    'text': (255, 255, 255)    # White for text
}

# System fonts with Vietnamese support
SYSTEM_FONTS = [
    "arial",
    "segoeui",
    "tahoma",
    "calibri",
    "notosans",
    "roboto",
    "times new roman"
]