"""Menu configuration constants"""

# Menu content matching TMX banner positions
MENU_TEXT = {
    "main": {
        "title": {"text": "LUDO", "pos": (400, 125)},
        "buttons": [
            {"text": "Chơi game", "pos": (400, 400)},
            {"text": "Luật chơi", "pos": (400, 470)},
            {"text": "Nhà phát triển", "pos": (400, 540)},
            {"text": "Thoát", "pos": (400, 610)}
        ]
    },
    "rules": {
        "title": {"text": "Luật chơi", "pos": (400, 150)},
        "content": [
            {"text": "1. Mỗi người chơi có 4 quân cờ", "pos": (400, 300)},
            {"text": "2. Tung được 6 để đưa quân ra khỏi chuồng", "pos": (400, 340)},
            {"text": "3. Di chuyển quân theo số trên xúc xắc", "pos": (400, 380)},
            {"text": "4. Đá quân đối thủ khi đến ô có quân", "pos": (400, 420)},
            {"text": "5. Gặp sao sẽ được hiệu ứng đặc biệt", "pos": (400, 460)},
            {"text": "6. Đưa 4 quân về đích để chiến thắng", "pos": (400, 500)}
        ],
        "buttons": [
            {"text": "Trở về", "pos": (400, 610)}
        ]
    },
    "developers": {
        "title": {"text": "Nhà phát triển", "pos": (400, 150)},
        "content": [
            {"text": "Nhóm phát triển:", "pos": (400, 300)},
            {"text": "1. Nguyễn Văn A - Leader", "pos": (400, 340)},
            {"text": "2. Trần Thị B - Developer", "pos": (400, 380)},
            {"text": "3. Lê Văn C - Developer", "pos": (400, 420)},
            {"text": "4. Phạm Thị D - Designer", "pos": (400, 460)}
        ],
        "buttons": [
            {"text": "Trở về", "pos": (400, 610)}
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
        'size': 90,
        'color': (0, 0, 0)  # Black
    },
    'menu': {
        'size': 42,
        'color': (0, 0, 0)  # Black
    },
    'content': {
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
    'background': (0, 0, 0)    # Black for background
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