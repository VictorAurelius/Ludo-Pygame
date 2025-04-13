"""Game controller module for managing game flow and state"""

import pygame
import sys
import gc
import os
from src.core.main_board import MainBoard
from src.utils.constants import WINDOW_WIDTH, WINDOW_HEIGHT
from src.ui.sound_manager import get_sound_manager
from src.entities.States import Statekeep

class GameController:
    def __init__(self):
        """Initialize the game controller"""
        pygame.init()
        # Get screen info for centering window
        info = pygame.display.Info()
        screen_width = info.current_w
        screen_height = info.current_h
        
        # Calculate window position to center it
        pos_x = (screen_width - WINDOW_WIDTH) // 2
        pos_y = (screen_height - WINDOW_HEIGHT) // 2
        
        # Set window position
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{pos_x},{pos_y}"
        
        self.sound_manager = get_sound_manager()

    def run_game(self):
        """Main game control loop"""
        while True:
            try:
                # Initialize and run main board to get player names
                menu = MainBoard()
                player_names = menu.run()
                
                if player_names:
                    try:
                        # Clean up modules for fresh game state
                        self._cleanup_modules()
                        
                        # Import main module for game session
                        import main
                        
                        # Run game with player names
                        result = main.main(player_names)
                        
                        if result is False:  # Player wants to exit completely
                            pygame.quit()
                            sys.exit()
                        elif result == "restart":  # Start new game
                            continue
                        # If result is None, loop continues to show main menu
                    except Exception as e:
                        print(f"Error reloading game: {e}")
                        continue  # Return to main menu on error
                else:
                    # Exit if no player names (user quit)
                    pygame.quit()
                    sys.exit()
            except Exception as e:
                print(f"Error: {e}")
                # Continue loop on error to avoid closing application

    def _cleanup_modules(self):
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
        
        # Run garbage collection to free memory
        gc.collect()

def main():
    """Entry point for game controller"""
    controller = GameController()
    controller.run_game()

if __name__ == "__main__":
    main()