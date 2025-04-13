"""
Utilities package.

This package provides common utility functions and configurations used
throughout the game.

Modules:
    asset_loader.py: Centralized asset loading and caching
    constants.py: Game-wide constants and configurations
    event_handler.py: Event management system
    geometry.py: Geometric calculations and collision detection
    logger_config.py: Logging setup and configuration
    menu_config.py: Menu layouts and configurations

Classes:
    AssetLoader: Manages game asset loading and caching
    EventHandler: Handles game events and callbacks
    GameLogger: Configures and manages logging
    PathPositions: Board position calculations

The utils package serves as a foundation for the game's infrastructure,
providing essential services used by other packages.

Key Features:
- Centralized asset management
    * Image loading and caching
    * Font management
    * TMX map loading
    * Sprite sheet handling

- Event System
    * Custom game events
    * Event registration and handling
    * Event filtering and blocking
    * Continuous event processing

- Geometric Utilities
    * Point and vector operations
    * Collision detection
    * Path interpolation
    * Rectangle operations

- Logging System
    * Multiple log levels
    * File and console output
    * Module-specific loggers
    * Error tracking

- Configuration Management
    * Game constants
    * Menu layouts
    * Board positions
    * Color schemes
    * Sound settings

Usage Example:
    ```python
    from src.utils.asset_loader import get_asset_loader
    from src.utils.event_handler import get_event_handler
    from src.utils.logger_config import get_logger
    
    # Get singleton instances
    asset_loader = get_asset_loader()
    event_handler = get_event_handler()
    logger = get_logger(__name__)
    
    # Use utilities
    image = asset_loader.load_image('path/to/image.png')
    event_handler.trigger_game_event(GameEvent.GAME_START)
    logger.info("Game initialized")
    ```

The utils package emphasizes:
- Singleton patterns for global services
- Efficient resource management
- Clear error handling
- Type safety with annotations
- Comprehensive documentation
"""

from .asset_loader import AssetLoader, get_asset_loader
from .event_handler import EventHandler, GameEvent, get_event_handler
from .logger_config import GameLogger, get_logger
from .constants import PathPositions

__all__ = [
    'AssetLoader', 'get_asset_loader',
    'EventHandler', 'GameEvent', 'get_event_handler',
    'GameLogger', 'get_logger',
    'PathPositions'
]