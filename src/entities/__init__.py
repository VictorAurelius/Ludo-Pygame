"""
Game entities package.

This package contains the core game entities that represent the game objects
and their behaviors.

Modules:
    Pawns.py: Pawn entity with movement and animation logic
    Players.py: Player entity managing player state and turns
    Stars.py: Star entity implementing special board effects
    States.py: Game state management and tracking

Classes:
    Pawn: Game piece with movement and animation capabilities
    Player: Player representation with turn management
    Star: Special board item providing effects
    Statekeep: Central game state manager

The entities package provides the core game objects that interact to create
the game mechanics. Each entity is responsible for managing its own state
and behavior while coordinating with others through the event system.

Key Features:
- Animated pawn movement
- Turn-based player management
- Special board effects
- Centralized state tracking

Each entity uses the event system to communicate state changes and coordinates
with other components through the game controller.
"""

from .Pawns import Pawn
from .Players import Player
from .Stars import Star, create_stars
from .States import Statekeep

__all__ = ['Pawn', 'Player', 'Star', 'create_stars', 'Statekeep']