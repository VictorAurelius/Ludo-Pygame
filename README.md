# Ludo Game

A Python implementation of the classic Ludo board game with modern features and clean architecture.

## Project Structure

```
src/
├── core/              # Core game logic
│   ├── __init__.py
│   ├── game_controller.py  # Main game controller
│   └── main_board.py      # Game board management
│
├── entities/          # Game entities
│   ├── __init__.py
│   ├── Pawns.py      # Pawn movement and animation
│   ├── Players.py    # Player management
│   ├── Stars.py      # Special effects items
│   └── States.py     # Game state management
│
├── ui/               # User interface components
│   ├── __init__.py
│   ├── alert_manager.py   # In-game notifications
│   ├── menu_manager.py    # Menu system
│   └── sound_manager.py   # Audio management
│
├── utils/            # Utility modules
│   ├── __init__.py
│   ├── asset_loader.py    # Asset management
│   ├── constants.py       # Game constants
│   ├── event_handler.py   # Event system
│   ├── geometry.py        # Geometric calculations
│   ├── logger_config.py   # Logging setup
│   └── menu_config.py     # Menu configuration
│
└── main.py          # Game entry point
```

## Key Features

- Modern Pythonic code with type hints
- Event-driven architecture
- Centralized asset management
- Flexible menu system
- Advanced animation system
- Comprehensive logging
- Error handling with user-friendly messages

## Dependencies

- Python 3.8+
- Pygame
- PyTMX

## Core Components

### Game Controller
The game controller (`game_controller.py`) manages the overall game flow and coordinates between different components. It handles:
- Game initialization
- State transitions
- Main game loop
- Error handling

### Entity System
The entity system consists of several key classes:
- `Player`: Manages player state and turns
- `Pawn`: Handles piece movement and animation
- `Star`: Implements special board effects
- `Statekeep`: Manages game state

### UI System
The UI system provides:
- Menu management with transitions
- Alert system for notifications
- Sound effects and music
- Error screens

### Utility Modules
Utility modules provide common functionality:
- Asset loading and caching
- Event handling
- Geometric calculations
- Logging configuration

## Event System

The game uses an event-driven architecture with these main event types:
- Game state events (start, pause, quit)
- Turn events (start, end)
- Pawn events (move, capture)
- UI events (menu changes, alerts)

## Asset Management

Assets are managed centrally through the `AssetLoader` class, which handles:
- Image loading and caching
- Font management
- TMX map loading
- Animation sprites

## Configuration

Game configuration is managed through:
- `constants.py`: Game constants
- `menu_config.py`: Menu layouts and text
- Logger configuration
- Sound settings

## Usage Example

```python
from src.core.game_controller import GameController

def main():
    controller = GameController()
    controller.run_game()

if __name__ == "__main__":
    main()
```

## Error Handling

The game includes comprehensive error handling:
- User-friendly error messages
- Detailed logging
- Graceful fallbacks
- State recovery

## Logging

Logging is configured through `logger_config.py` and provides:
- Different log levels (DEBUG, INFO, etc.)
- File and console output
- Module-specific loggers
- Formatted output

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests if needed
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.