"""
Star entity module handling star effects and placement on the game board.
"""

import random
import pygame
from pygame.locals import *

from src.utils.constants import (
    TILE_SIZE, STAR_IMAGE, STAR_COUNT,
    STAR_EFFECTS, RESTRICTED_POSITIONS,
    BOARD_POSITIONS
)

class Star(pygame.sprite.Sprite):
    """
    Star sprite class representing bonus/penalty items on the board.
    Stars can provide various effects when a pawn lands on them.
    """
    
    def __init__(self, position):
        """
        Initialize a star
        
        Args:
            position (tuple): Grid position (x, y) for the star
        """
        super().__init__()
        self.surf = pygame.image.load(STAR_IMAGE)
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        
        # Convert grid position to pixel coordinates
        pixel_x = position[0] * TILE_SIZE - 13
        pixel_y = position[1] * TILE_SIZE - 13
        self.rect = self.surf.get_rect(center=(pixel_x, pixel_y))
        self.position = position

    def check_exact_collision(self, pawn):
        """
        Check if a pawn has landed exactly on this star's position
        
        Args:
            pawn: The pawn to check collision with
            
        Returns:
            bool: True if pawn is on the same grid position as star
        """
        pawn_x = (pawn.rect.center[0] + 13) // TILE_SIZE
        pawn_y = (pawn.rect.center[1] + 13) // TILE_SIZE
        return (pawn_x, pawn_y) == (self.position[0], self.position[1])

    def apply_effect(self, pawn, statekeeper):
        """
        Apply a random effect to the pawn that landed on the star
        
        Args:
            pawn: The pawn to apply the effect to
            statekeeper: The game state keeper
            
        Returns:
            str: Description of the effect applied
        """
        effect = random.randint(0, 2)
        
        if effect == STAR_EFFECTS['ROLL_AGAIN']:
            return "roll_again"
            
        elif effect in (STAR_EFFECTS['TELEPORT'], STAR_EFFECTS['DIE']):
            if effect == STAR_EFFECTS['DIE']:
                # Send pawn back to start
                self._send_pawn_home(pawn, statekeeper)
                return "died"
            else:
                # Teleport to random valid position
                if self._teleport_pawn(pawn, statekeeper):
                    return "teleported"
        
        return "no_effect"

    def _send_pawn_home(self, pawn, statekeeper):
        """Send a pawn back to its starting position"""
        pawn.counter = 0
        pawn.rect.center = pawn.startpos
        
        # Find and update the pawn's owner
        for player in statekeeper.players:
            if pawn in player.pawnlist:
                player.pawns -= 1
                break

    def _teleport_pawn(self, pawn, statekeeper):
        """
        Teleport a pawn to a random valid position
        
        Returns:
            bool: True if teleport was successful
        """
        valid_positions = self._get_valid_positions(pawn, statekeeper)
        
        if valid_positions:
            new_pos = random.choice(valid_positions)
            pawn.counter = new_pos
            pawn.rect.center = pawn.dict[new_pos]
            return True
            
        return False

    def _get_valid_positions(self, pawn, statekeeper):
        """Get list of valid positions a pawn can teleport to"""
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

def create_stars():
    """
    Create and place stars on the board
    
    Returns:
        pygame.sprite.Group: Group containing all created stars
    """
    # Get available positions for stars
    available_positions = []
    for pos, coord in BOARD_POSITIONS.items():
        if pos not in RESTRICTED_POSITIONS:
            available_positions.append(coord)
    
    # Select random positions for stars
    star_positions = random.sample(available_positions, STAR_COUNT)
    
    # Create star sprites
    stars = pygame.sprite.Group()
    for pos in star_positions:
        star = Star(pos)
        stars.add(star)
        
    return stars

# Create the global stars group
stars = create_stars()