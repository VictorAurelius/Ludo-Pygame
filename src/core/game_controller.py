"""
Game controller module managing overall game flow and state.
"""

import sys
import gc
import os
import pygame
from typing import Optional, List

from src.utils.logger_config import get_logger
from src.utils.event_handler import get_event_handler, GameEvent
from src.utils.asset_loader import get_asset_loader
from src.utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT

from src.core.main_board import MainBoard
from src.ui.sound_manager import get_sound_manager
from src.entities.States import Statekeep

logger = get_logger(__name__)

class GameController:
    """Controls the main game flow and state transitions"""
    
    def __init__(self):
        """Initialize the game controller and core systems"""
        try:
            self._init_pygame()
            self._init_managers()
            self._setup_event_handlers()
            logger.info("Game controller initialized successfully")
        except Exception as e:
            logger.critical(f"Failed to initialize game controller: {e}")
            raise

    def _init_pygame(self) -> None:
        """Initialize Pygame and set up the game window"""
        pygame.init()
        
        # Center window on screen
        info = pygame.display.Info()
        pos_x = (info.current_w - WINDOW_WIDTH) // 2
        pos_y = (info.current_h - WINDOW_HEIGHT) // 2
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{pos_x},{pos_y}"
        
        logger.info("Pygame initialized")

    def _init_managers(self) -> None:
        """Initialize game system managers"""
        self.event_handler = get_event_handler()
        self.sound_manager = get_sound_manager()
        self.asset_loader = get_asset_loader()
        
        # Preload essential assets
        self._preload_assets()

    def _preload_assets(self) -> None:
        """Preload commonly used game assets"""
        try:
            # Add any essential assets that should be loaded at startup
            logger.info("Essential assets loaded")
        except Exception as e:
            logger.error(f"Failed to preload assets: {e}")

    def _setup_event_handlers(self) -> None:
        """Set up event handlers for game events"""
        self.event_handler.add_pygame_handler(pygame.QUIT, self._handle_quit)
        self.event_handler.add_game_handler(GameEvent.GAME_START, self._handle_game_start)
        self.event_handler.add_game_handler(GameEvent.GAME_QUIT, self._handle_quit)

    def run_game(self) -> None:
        """Main game control loop"""
        logger.info("Starting game loop")
        
        while True:
            try:
                # Initialize and run main board to get player names
                menu = MainBoard()
                player_names = menu.run()
                
                if player_names:
                    self._handle_game_session(player_names)
                else:
                    logger.info("No player names received, exiting")
                    self._quit_game()
                    
            except Exception as e:
                logger.error(f"Error in game loop: {e}")
                continue  # Continue loop on error

    def _handle_game_session(self, player_names: List[str]) -> None:
        """
        Handle a game session
        
        Args:
            player_names: List of player names
        """
        try:
            # Clean up for new game
            self._cleanup_modules()
            
            # Trigger game start event
            self.event_handler.trigger_game_event(
                GameEvent.GAME_START,
                player_names=player_names
            )
            
            # Import and run main game
            import main
            result = main.main(player_names)
            
            self._handle_game_result(result)
            
        except Exception as e:
            logger.error(f"Error in game session: {e}")
            self.event_handler.trigger_game_event(GameEvent.GAME_QUIT)

    def _handle_game_result(self, result: Optional[str]) -> None:
        """
        Handle the result of a game session
        
        Args:
            result: Game result string or None
        """
        if result is False:
            logger.info("Player requested exit")
            self._quit_game()
        elif result == "restart":
            logger.info("Restarting game")
            self.event_handler.trigger_game_event(GameEvent.GAME_START)
        # None result continues to main menu

    def _cleanup_modules(self) -> None:
        """Clean up modules for fresh game state"""
        modules_to_clean = [
            'main',
            'src.entities.Players',
            'src.entities.Pawns',
            'src.entities.States',
            'src.entities.Stars',
            'src.ui.alert_manager'
        ]
        
        for module in modules_to_clean:
            if module in sys.modules:
                del sys.modules[module]
                logger.debug(f"Cleaned up module: {module}")
        
        # Run garbage collection
        gc.collect()
        logger.debug("Memory cleanup completed")

    def _handle_quit(self, *args) -> bool:
        """Handle quit event"""
        logger.info("Quit event received")
        self._quit_game()
        return False

    def _handle_game_start(self, **kwargs) -> None:
        """Handle game start event"""
        logger.info("Starting new game")
        self.sound_manager.play_sound('start_game')

    def _quit_game(self) -> None:
        """Clean up and quit the game"""
        logger.info("Shutting down game")
        pygame.quit()
        sys.exit()

def main():
    """Entry point for game controller"""
    try:
        controller = GameController()
        controller.run_game()
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()