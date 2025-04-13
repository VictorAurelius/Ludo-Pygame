"""Sound configuration and mappings"""

import os

# Sound file mappings
SOUND_FILES = {
    'click': 'click.wav',
    'hover': 'hover.wav',
    'transition': 'transition.wav',
    'start_game': 'start_game.wav',
    'win': 'win.wav',
}

# Sound directories to search in order
SOUND_DIRS = [
    os.path.join('assets', 'sounds'),
    os.path.join('assets_ver1', 'sounds'),
]

# Default sound settings
DEFAULT_VOLUME = 0.3
MAX_VOLUME = 1.0
MIN_VOLUME = 0.0

# Sound categories for group control
SOUND_CATEGORIES = {
    'ui': ['click', 'hover'],
    'game': ['transition', 'start_game', 'win'],
}

# Fallback sounds (if primary sound not found)
FALLBACK_SOUNDS = {
    'win': 'transition',
    'hover': 'click',
}