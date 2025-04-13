"""
Core game logic package.

This package contains the main game control and board management components.
It serves as the central coordination point for game flow and state management.

Modules:
    game_controller.py: Main game controller handling game flow and initialization
    main_board.py: Game board management and state transitions

Classes:
    GameController: Main game controller class
    MainBoard: Game board management class

The core package coordinates between different game components and manages the
main game loop, state transitions, and overall game flow.
"""

from .game_controller import GameController
from .main_board import MainBoard

__all__ = ['GameController', 'MainBoard']
