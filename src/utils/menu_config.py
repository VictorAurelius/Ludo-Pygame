"""Menu configuration constants"""

# Menu content matching TMX banner and button layer positions with offsets
MENU_TEXT = {
    "main": {
        "title": {"text": "LUDO", "pos": (409, 34)},  # Adjusted for banner offset (9, -91)
        "buttons": [
            {"text": "Play Game", "pos": (391, 297)},  # Adjusted for button offset (-9, -103)
            {"text": "Rules", "pos": (391, 367)},
            {"text": "Developers", "pos": (391, 437)},
            {"text": "Exit", "pos": (391, 507)}
        ]
    },
    "rules": {
        "title": {"text": "Rules", "pos": (409, 59)},  # Adjusted for banner offset
        "content": [
            {"text": "1. Each player has 4 pieces", "pos": (409, 209)},
            {"text": "2. Roll a 6 to move a piece out", "pos": (409, 249)},
            {"text": "3. Move pieces based on dice roll", "pos": (409, 289)},
            {"text": "4. Capture opponent's piece on the same spot", "pos": (409, 329)},
            {"text": "5. Special effects on star tiles", "pos": (409, 369)},
            {"text": "6. Bring all 4 pieces home to win", "pos": (409, 409)}
        ],
        "buttons": [
            {"text": "Back", "pos": (391, 507)}  # Adjusted for button offset
        ]
    },
    "developers": {
        "title": {"text": "Developers", "pos": (409, 59)},  # Adjusted for banner offset
        "content": [
            {"text": "Development Team:", "pos": (409, 209)},
            {"text": "1. Nguyen Van Kiet - Developer", "pos": (409, 289)},
            {"text": "2. Nguyen Tai Nhat - Developer", "pos": (409, 329)},
            {"text": "3. Vu Minh Quyet - Developer", "pos": (409, 369)}
        ],
        "buttons": [
            {"text": "Back", "pos": (391, 507)}  # Adjusted for button offset
        ]
    },
    "name_input": {
        "title": {"text": "Enter Player Names", "pos": (409, 59)},  # Adjusted for banner offset
        "buttons": [
            {"text": "Back", "pos": (391, 487)},  # Adjusted for button offset
            {"text": "Start", "pos": (491, 487)}   # Adjusted for button offset
        ]
    }
}

# Button click areas matched with TMX button layer positions
BUTTON_REGIONS = {
    "main": [
        {"rect": (311, 277, 160, 40), "action": "start_game"},  # Adjusted for button offset (-9, -103)
        {"rect": (311, 347, 160, 40), "action": "rules"},
        {"rect": (311, 417, 160, 40), "action": "developers"},
        {"rect": (311, 487, 160, 40), "action": "exit"}
    ],
    "rules": [
        {"rect": (291, 487, 200, 40), "action": "main"}  # Adjusted for button offset
    ],
    "developers": [
        {"rect": (291, 487, 200, 40), "action": "main"}  # Adjusted for button offset
    ],
    "name_input": [
        {"rect": (241, 467, 100, 40), "action": "main"},  # Adjusted for button offset
        {"rect": (441, 467, 100, 40), "action": "start"}  # Adjusted for button offset
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