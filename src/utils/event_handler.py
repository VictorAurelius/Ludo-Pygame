"""
Event handling utility module providing common event management functionality.
"""

import pygame
from typing import Dict, List, Callable, Optional, Any, Set
from enum import Enum, auto
import logging

logger = logging.getLogger(__name__)

class GameEvent(Enum):
    """Game-specific event types"""
    GAME_START = auto()
    GAME_PAUSE = auto()
    GAME_RESUME = auto()
    GAME_QUIT = auto()
    TURN_START = auto()
    TURN_END = auto()
    PAWN_MOVE = auto()
    PAWN_CAPTURE = auto()
    DICE_ROLL = auto()
    PLAYER_WIN = auto()
    STAR_EFFECT = auto()
    MENU_CHANGE = auto()
    SOUND_TOGGLE = auto()

class EventHandler:
    """Handles game events and callbacks"""
    
    def __init__(self):
        self._pygame_handlers: Dict[int, List[Callable]] = {}
        self._game_handlers: Dict[GameEvent, List[Callable]] = {}
        self._continuous_handlers: List[Callable] = []
        self._blocked_events: Set[int] = set()
        
    def add_pygame_handler(self, event_type: int, handler: Callable) -> None:
        """
        Add a handler for a pygame event
        
        Args:
            event_type: Pygame event type
            handler: Callback function for the event
        """
        if event_type not in self._pygame_handlers:
            self._pygame_handlers[event_type] = []
        self._pygame_handlers[event_type].append(handler)

    def add_game_handler(self, event_type: GameEvent, handler: Callable) -> None:
        """
        Add a handler for a game event
        
        Args:
            event_type: Game event type
            handler: Callback function for the event
        """
        if event_type not in self._game_handlers:
            self._game_handlers[event_type] = []
        self._game_handlers[event_type].append(handler)

    def add_continuous_handler(self, handler: Callable) -> None:
        """
        Add a handler that runs every frame
        
        Args:
            handler: Callback function to run each frame
        """
        self._continuous_handlers.append(handler)

    def remove_pygame_handler(self, event_type: int, handler: Callable) -> None:
        """Remove a pygame event handler"""
        if event_type in self._pygame_handlers:
            try:
                self._pygame_handlers[event_type].remove(handler)
            except ValueError:
                pass

    def remove_game_handler(self, event_type: GameEvent, handler: Callable) -> None:
        """Remove a game event handler"""
        if event_type in self._game_handlers:
            try:
                self._game_handlers[event_type].remove(handler)
            except ValueError:
                pass

    def remove_continuous_handler(self, handler: Callable) -> None:
        """Remove a continuous handler"""
        try:
            self._continuous_handlers.remove(handler)
        except ValueError:
            pass

    def block_event(self, event_type: int) -> None:
        """Block a pygame event type from being processed"""
        self._blocked_events.add(event_type)

    def unblock_event(self, event_type: int) -> None:
        """Unblock a pygame event type"""
        self._blocked_events.discard(event_type)

    def trigger_game_event(self, event_type: GameEvent, **kwargs: Any) -> None:
        """
        Trigger a game event
        
        Args:
            event_type: Type of game event to trigger
            **kwargs: Additional data to pass to handlers
        """
        if event_type in self._game_handlers:
            for handler in self._game_handlers[event_type]:
                try:
                    handler(**kwargs)
                except Exception as e:
                    logger.error(f"Error in game event handler: {e}")

    def update(self) -> bool:
        """
        Process all pending events
        
        Returns:
            bool: False if quit event received, True otherwise
        """
        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type not in self._blocked_events:
                if event.type in self._pygame_handlers:
                    for handler in self._pygame_handlers[event.type]:
                        try:
                            if handler(event) is False:
                                return False
                        except Exception as e:
                            logger.error(f"Error in pygame event handler: {e}")
        
        # Run continuous handlers
        for handler in self._continuous_handlers:
            try:
                if handler() is False:
                    return False
            except Exception as e:
                logger.error(f"Error in continuous handler: {e}")
                
        return True

    @staticmethod
    def get_mouse_pos() -> tuple[int, int]:
        """Get current mouse position"""
        return pygame.mouse.get_pos()

    @staticmethod
    def get_mouse_pressed() -> tuple[bool, bool, bool]:
        """Get current mouse button states"""
        return pygame.mouse.get_pressed()

    @staticmethod
    def get_keys_pressed() -> List[bool]:
        """Get current keyboard state"""
        return pygame.key.get_pressed()

# Global event handler instance
_event_handler = None

def get_event_handler() -> EventHandler:
    """Get or create the global event handler instance"""
    global _event_handler
    if _event_handler is None:
        _event_handler = EventHandler()
    return _event_handler