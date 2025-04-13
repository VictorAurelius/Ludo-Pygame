"""
Star entity module handling bonus/penalty items on the game board.
"""

import random
import pygame
from pygame.locals import RLEACCEL
from typing import Dict, List, Optional, Tuple, Any

from src.utils.logger_config import get_logger
from src.utils.asset_loader import get_asset_loader
from src.utils.event_handler import get_event_handler, GameEvent
from src.utils.geometry import Point
from src.utils.constants import (
    TILE_SIZE, BOARD_POSITIONS, RESTRICTED_POSITIONS,
    STAR_IMAGE, STAR_COUNT
)

from src.entities.States import Statekeep
from src.entities.Pawns import Pawn
logger = get_logger(__name__)

class Star(pygame.sprite.Sprite):
    """Star sprite representing bonus/penalty items on the board"""
    
    def __init__(self, position: Tuple[int, int]):
        """
        Initialize a star
        
        Args:
            position: Grid position (x, y) for the star
        """
        super().__init__()
        
        # Load star image
        asset_loader = get_asset_loader()
        self.surf = asset_loader.load_image(STAR_IMAGE)
        if self.surf is None:
            logger.error("Failed to load star image")
            self.surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
            
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        
        # Convert grid position to pixel coordinates
        pixel_x = position[0] * TILE_SIZE - 13
        pixel_y = position[1] * TILE_SIZE - 13
        self.rect = self.surf.get_rect(center=(pixel_x, pixel_y))
        self.position = position
        
        # Event handling
        self.event_handler = get_event_handler()
        
        logger.debug(f"Created star at position {position}")

    def check_exact_collision(self, pawn: 'Pawn') -> bool:
        """
        Check if a pawn has landed exactly on this star's position
        
        Args:
            pawn: The pawn to check collision with
            
        Returns:
            bool: True if pawn is on the same grid position as star
        """
        pawn_x = (pawn.rect.center[0] + 13) // TILE_SIZE
        pawn_y = (pawn.rect.center[1] + 13) // TILE_SIZE
        return (pawn_x, pawn_y) == self.position

    def apply_effect(self, pawn: 'Pawn', statekeeper: 'Statekeep') -> str:
        """
        Apply a random effect to the pawn that landed on the star
        
        Args:
            pawn: The pawn to apply the effect to
            statekeeper: The game state keeper
            
        Returns:
            str: Description of the effect applied
        """
        effect = random.randint(0, 2)
        effect_result = "no_effect"
        
        try:
            if effect == 1:  # Roll again
                effect_result = "roll_again"
                self._trigger_effect_event(pawn, "roll_again")
                
            elif effect == 2:  # Teleport
                effect_result = self._handle_teleport(pawn, statekeeper)
                
            else:  # Send home
                effect_result = self._handle_send_home(pawn, statekeeper)
                
        except Exception as e:
            logger.error(f"Error applying star effect: {e}")
            effect_result = "error"
            
        return effect_result

    def _handle_teleport(self, pawn: 'Pawn', statekeeper: 'Statekeep') -> str:
        """
        Handle teleport effect
        
        Args:
            pawn: Pawn to teleport
            statekeeper: Game state keeper
            
        Returns:
            str: Effect result
        """
        valid_positions = self._get_valid_positions(pawn, statekeeper)
        
        if valid_positions:
            new_pos = random.choice(valid_positions)
            old_pos = pawn.counter
            pawn.counter = new_pos
            pawn.rect.center = pawn.dict[new_pos]
            
            self._trigger_effect_event(pawn, "teleport",
                                     old_pos=old_pos, new_pos=new_pos)
            return "teleported"
            
        return "no_effect"

    def _handle_send_home(self, pawn: 'Pawn', statekeeper: 'Statekeep') -> str:
        """
        Handle send home effect
        
        Args:
            pawn: Pawn to send home
            statekeeper: Game state keeper
            
        Returns:
            str: Effect result
        """
        old_pos = pawn.rect.center
        pawn.counter = 0
        pawn.rect.center = pawn.startpos
        
        # Update player state
        for player in statekeeper.players:
            if pawn in player.pawnlist:
                player.pawns -= 1
                self._trigger_effect_event(pawn, "died",
                                         player=player, old_pos=old_pos)
                break
                
        return "died"

    def _get_valid_positions(self, pawn: 'Pawn',
                           statekeeper: 'Statekeep') -> List[int]:
        """
        Get list of valid positions for teleport
        
        Args:
            pawn: The pawn to move
            statekeeper: Game state keeper
            
        Returns:
            List[int]: List of valid position indices
        """
        valid_positions = []
        
        for pos in range(1, 97):
            can_move = True
            new_pos = pawn.dict[pos]
            
            # Check if position is occupied
            for player in statekeeper.players:
                for other_pawn in player.pawnlist:
                    if other_pawn != pawn and other_pawn.rect.center == new_pos:
                        can_move = False
                        break
                if not can_move:
                    break
                    
            if can_move:
                valid_positions.append(pos)
                
        return valid_positions

    def _trigger_effect_event(self, pawn: 'Pawn', effect: str,
                            **kwargs: Any) -> None:
        """
        Trigger star effect event
        
        Args:
            pawn: Affected pawn
            effect: Effect type
            **kwargs: Additional event data
        """
        self.event_handler.trigger_game_event(
            GameEvent.STAR_EFFECT,
            pawn=pawn,
            effect=effect,
            position=self.position,
            **kwargs
        )

def create_stars() -> pygame.sprite.Group:
    """
    Create and place stars on the board
    
    Returns:
        pygame.sprite.Group: Group containing all created stars
    """
    # Get available positions
    available_positions = []
    for pos, coord in BOARD_POSITIONS.items():
        if pos not in RESTRICTED_POSITIONS:
            available_positions.append(coord)
    
    # Debug log for available positions and STAR_COUNT
    logger.debug(f"Available positions: {len(available_positions)}")
    logger.debug(f"STAR_COUNT: {STAR_COUNT}")
    
    # Select random positions for stars
    if len(available_positions) < STAR_COUNT:
        logger.error("Not enough available positions to place stars.")
        return pygame.sprite.Group()  # Return empty group to avoid crash
    star_positions = random.sample(available_positions, STAR_COUNT)
    
    # Create star sprites
    stars = pygame.sprite.Group()
    for pos in star_positions:
        try:
            star = Star(pos)
            stars.add(star)
            logger.debug(f"Created star at position {pos}")
        except Exception as e:
            logger.error(f"Failed to create star at {pos}: {e}")
    
    logger.info(f"Created {len(stars)} stars")
    return stars

# Create global stars group
stars = create_stars()