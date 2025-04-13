"""
Main board module managing game setup and state transitions.
"""

import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import pygame
from typing import List, Optional, Dict

from src.utils.logger_config import get_logger
from src.utils.asset_loader import get_asset_loader
from src.utils.event_handler import get_event_handler, GameEvent
from src.utils.geometry import rect_from_center
from src.utils.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT, COLORS
)
from src.ui.menu_manager import get_menu_manager

logger = get_logger(__name__)

class MainBoard:
    """
    Main board class handling game setup and state transitions.
    Delegates menu handling to MenuManager.
    """
    
    def __init__(self):
        """Initialize the main board"""
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Ludo King - Cờ Cá Ngựa")
        
        # Initialize managers
        self.asset_loader = get_asset_loader()
        self.event_handler = get_event_handler()
        self.menu_manager = get_menu_manager(self.screen)
        
        # Game state
        self.player_names: List[str] = ["", "", "", ""]
        self.active_input: int = 0
        self.current_screen: str = "main"
        
        try:
            self._initialize()
            logger.info("Main board initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize main board: {e}")
            self._handle_init_error(e)

    def _initialize(self) -> None:
        """Initialize game components"""
        # Set up event handlers
        self._setup_event_handlers()
        
        # Initialize menu system
        self.menu_manager.initialize()

    def _setup_event_handlers(self) -> None:
        """Set up event handlers"""
        self.event_handler.add_pygame_handler(pygame.QUIT, self._handle_quit)
        self.event_handler.add_game_handler(GameEvent.MENU_CHANGE, self._handle_menu_change)
        self.event_handler.add_game_handler(GameEvent.GAME_START, self._handle_game_start)

    def _handle_init_error(self, error: Exception) -> None:
        """
        Handle initialization errors
        
        Args:
            error: Exception that occurred
        """
        logger.error(f"Initialization error: {str(error)}")
        self.menu_manager.show_error_screen(
            title="Initialization Error",
            error_msg=str(error),
            help_messages=[
                "Failed to initialize game components.",
                "Please check the game logs for details.",
                "Try reinstalling the game if the issue persists."
            ]
        )

    def _handle_quit(self, event: pygame.event.Event) -> bool:
        """Handle quit event"""
        logger.info("Quit event received")
        return False

    def _handle_menu_change(self, screen: str) -> None:
        """Handle menu screen changes"""
        self.current_screen = screen
        logger.debug(f"Changed to screen: {screen}")

    def _handle_game_start(self, player_names: List[str]) -> None:
        """Handle game start event"""
        self.player_names = player_names
        logger.info(f"Starting game with players: {player_names}")

    def _handle_input(self) -> Optional[bool]:
        """
        Handle user input
        
        Returns:
            Optional[bool]: False to quit, None to continue
        """
        if not self.event_handler.update():
            return False
            
        # Let menu manager handle input first
        result = self.menu_manager.handle_input()
        if result is not None:
            return result
            
        return None

    def _update(self) -> None:
        """Update game state"""
        self.menu_manager.update()

    def _draw(self) -> None:
        """Draw current game state"""
        self.screen.fill(COLORS['background'])
        self.menu_manager.draw()
        pygame.display.flip()

    def run(self) -> Optional[List[str]]:
        """
        Main loop for the board
        
        Returns:
            Optional[List[str]]: List of player names or None if quit
        """
        logger.info("Starting main board loop")
        clock = pygame.time.Clock()
        running = True
        
        while running:
            clock.tick(60)
            
            # Handle input
            result = self._handle_input()
            if result is False:
                running = False
            elif isinstance(result, list):
                return result  # Player names
            
            # Update and draw
            self._update()
            self._draw()
        
        return None

def test_main_board():
    """Test function for MainBoard"""
    try:
        board = MainBoard()
        result = board.run()
        logger.info(f"Main board test completed. Result: {result}")
        return result
    except Exception as e:
        logger.error(f"Main board test failed: {e}")
        return None

if __name__ == "__main__":
    test_main_board()
