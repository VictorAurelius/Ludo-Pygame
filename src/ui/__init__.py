"""
User interface package.

This package contains all UI-related components for managing game interface,
menus, alerts, and sound effects.

Modules:
    alert_manager.py: In-game notification system
    menu_manager.py: Menu system and navigation
    sound_manager.py: Audio playback and management

Classes:
    AlertManager: Manages in-game notifications and alerts
    MenuManager: Handles menu rendering and interaction
    SoundManager: Controls game audio and effects

The UI package provides a comprehensive interface layer between the game
logic and the player. It handles all user interaction, feedback, and
presentation aspects of the game.

Features:
- Menu system with multiple screens
- Animated transitions
- In-game notifications and alerts
- Sound effects and background music
- Error message display
- Input handling and validation
- Customizable UI elements

The package uses the event system to coordinate with game logic and
maintains a consistent visual style across all game screens.

Design Principles:
- Clear user feedback
- Smooth transitions
- Consistent styling
- Error resilience
- Accessibility considerations
- Performance optimization

The UI components use the utility modules for asset loading, event handling,
and configuration management to provide a cohesive user experience.
"""

from .alert_manager import AlertManager, get_alert_manager
from .menu_manager import MenuManager, get_menu_manager
from .sound_manager import SoundManager, get_sound_manager

__all__ = [
    'AlertManager', 'get_alert_manager',
    'MenuManager', 'get_menu_manager',
    'SoundManager', 'get_sound_manager'
]