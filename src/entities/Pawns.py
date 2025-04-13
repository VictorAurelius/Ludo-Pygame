"""
Pawn entity module representing game pieces and their movement.
"""

import pygame
from pygame.locals import RLEACCEL
from typing import Dict, Tuple, Optional, List

from src.utils.logger_config import get_logger
from src.utils.asset_loader import get_asset_loader
from src.utils.event_handler import get_event_handler, GameEvent
from src.utils.geometry import (
    interpolate_points, normalize_vector,
    distance, Point
)
from src.utils.constants import (
    TILE_SIZE, RED_FINISH_POSITIONS, BLUE_FINISH_POSITIONS,
    YELLOW_FINISH_POSITIONS, GREEN_FINISH_POSITIONS,
    PathPositions, SPRITE_GROUPS, ANIMATION_PATHS
)

logger = get_logger(__name__)

class Pawn(pygame.sprite.Sprite):
    """
    Pawn sprite representing a game piece that can move on the board
    and animate based on its state and movement.
    """
    
    def __init__(self, surface: pygame.Surface, path_positions: Dict[int, Tuple[int, int]],
                 start_pos: Tuple[int, int], number: int):
        """
        Initialize a pawn
        
        Args:
            surface: Initial pawn surface
            path_positions: Dictionary of board positions for this pawn
            start_pos: Starting position
            number: Pawn number (1-4)
        """
        super().__init__()
        self.surf = surface
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        
        # Movement properties
        self.counter = 0
        self.dict = path_positions
        self.number = number
        self.startpos = start_pos
        self.rect = self.surf.get_rect(center=start_pos)
        
        # State flags
        self.active_pawn = (number == 1)
        self.king = False
        self.king_pawn = 0
        
        # Animation properties
        self.is_move = False
        self.animation_path: List[Point] = []
        self.animation_index = 0
        self.animation_speed = 1
        self.current_state = "stand_left"
        self.frame_index = 0
        self.last_frame_update = pygame.time.get_ticks()
        self.animations = {}
        self.frame_delay = 100
        
        # Finish state
        self.has_reached_finish = False
        self.finish_position: Optional[Tuple[int, int]] = None
        
        # Event handler
        self.event_handler = get_event_handler()
        
        logger.debug(f"Initialized pawn {number} at position {start_pos}")

    def move(self, dice: int, statekeeper: 'Statekeep') -> None:
        """
        Move the pawn according to dice roll
        
        Args:
            dice: Number of spaces to move
            statekeeper: Game state manager
        """
        old_counter = self.counter
        self.counter += dice
        
        if self.counter in (96, 97):
            self._handle_finish(statekeeper)
        elif self.counter > 97:
            self.counter -= dice
            logger.debug(f"Pawn {self.number} move cancelled: would exceed path")
            return
            
        # Set up movement animation
        self._setup_movement(old_counter)
        logger.debug(f"Pawn {self.number} moving {dice} spaces from {old_counter} to {self.counter}")
        
        statekeeper.reset_counterlist_status()
        
        # Trigger movement event
        self.event_handler.trigger_game_event(
            GameEvent.PAWN_MOVE,
            pawn=self,
            old_pos=old_counter,
            new_pos=self.counter
        )

    def _handle_finish(self, statekeeper: 'Statekeep') -> None:
        """
        Handle pawn reaching finish position
        
        Args:
            statekeeper: Game state manager
        """
        self.king_pawn += 1
        
        # Find pawn's player and color
        for player in statekeeper.players:
            if self in player.pawnlist:
                color = player.color
                if not self.has_reached_finish:
                    player.pawns_home += 1
                    logger.info(f"{color} pawn {self.number} reached home")
                break
        else:
            logger.error(f"Could not find player for pawn {self.number}")
            return
            
        # Get finish positions for color
        finish_positions = {
            "Red": RED_FINISH_POSITIONS,
            "Blue": BLUE_FINISH_POSITIONS,
            "Yellow": YELLOW_FINISH_POSITIONS,
            "Green": GREEN_FINISH_POSITIONS
        }.get(color)
        
        if finish_positions and self.number in finish_positions:
            self.finish_position = PathPositions.scale_position(
                finish_positions[self.number]
            )
            self.has_reached_finish = True
            
        self.active_pawn = False
        self.king = True

    def _setup_movement(self, start_pos: int) -> None:
        """
        Set up movement animation path
        
        Args:
            start_pos: Starting position on path
        """
        self.setup_animation_path(start_pos, self.counter)
        self.is_move = True
        self.animation_index = 0
        self.last_frame_update = pygame.time.get_ticks()

    def setup_animation_path(self, start_pos: int, end_pos: int) -> None:
        """
        Create animation path between positions
        
        Args:
            start_pos: Starting position
            end_pos: Ending position
        """
        self.animation_path = []
        self.direction_changes = []
        steps_per_square = 10
        
        current_pos = self.rect.center
        last_direction = "left"
        
        for pos in range(start_pos + 1, end_pos + 1):
            next_pos = self.dict[pos]
            
            # Get movement direction
            dx = next_pos[0] - current_pos[0]
            dy = next_pos[1] - current_pos[1]
            
            # Determine primary movement direction
            if abs(dx) > abs(dy):
                direction = "right" if dx > 0 else "left"
                last_direction = direction
            else:
                direction = last_direction
            
            # Create interpolated points
            points = interpolate_points(
                current_pos,
                next_pos,
                steps_per_square
            )
            
            self.animation_path.extend(points)
            self.direction_changes.extend([direction] * len(points))
            
            current_pos = next_pos
        
        if self.direction_changes:
            self.current_state = f"walk_{self.direction_changes[0]}"

    def update_animation(self) -> None:
        """Update pawn animation state"""
        current_time = pygame.time.get_ticks()
        
        if self.is_move:
            self._update_movement_animation(current_time)
        elif self.current_state in self.animations:
            self._update_standing_animation(current_time)

    def _update_movement_animation(self, current_time: int) -> None:
        """
        Update movement animation
        
        Args:
            current_time: Current game time
        """
        if self.animation_index >= len(self.animation_path):
            self._finish_movement()
            return
            
        if not hasattr(self, 'last_animation_time'):
            self.last_animation_time = current_time
            
        time_since_last = current_time - self.last_animation_time
        if time_since_last > self.animation_speed * 10:
            # Update position
            self.rect.center = self.animation_path[self.animation_index]
            
            # Update direction
            if self.animation_index < len(self.direction_changes):
                direction = self.direction_changes[self.animation_index]
                walk_state = f"walk_{direction}"
                
                if self.current_state != walk_state:
                    self.current_state = walk_state
                    self.frame_index = 0
            
            self.animation_index += 1
            self.last_animation_time = current_time
            
        # Update walking animation
        if self.current_state in self.animations:
            self._update_animation_frame(current_time)

    def _update_standing_animation(self, current_time: int) -> None:
        """
        Update standing animation
        
        Args:
            current_time: Current game time
        """
        if current_time - self.last_frame_update > self.frame_delay:
            num_frames = len(self.animations[self.current_state])
            self.frame_index = (self.frame_index + 1) % num_frames
            
            frame_data = self.animations[self.current_state][self.frame_index]
            self._update_sprite_surface(frame_data[0])
            
            self.last_frame_update = current_time

    def _update_sprite_surface(self, new_surface: pygame.Surface) -> None:
        """
        Update sprite surface maintaining position
        
        Args:
            new_surface: New surface to use
        """
        old_center = self.rect.center
        self.surf = new_surface
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=old_center)

    def _finish_movement(self) -> None:
        """Handle completion of movement"""
        self.is_move = False
        
        if self.has_reached_finish and self.finish_position:
            self.rect.center = self.finish_position
            self.has_reached_finish = False
            
            # Trigger finish event
            self.event_handler.trigger_game_event(
                GameEvent.PAWN_MOVE,
                pawn=self,
                finished=True
            )
            
        if hasattr(self, 'direction_changes') and self.direction_changes:
            self.current_state = f"stand_{self.direction_changes[-1]}"
        else:
            self.current_state = "stand_left"
            
        self.frame_index = 0

    def _update_animation_frame(self, current_time: int) -> None:
        """
        Update animation frame
        
        Args:
            current_time: Current game time
        """
        if current_time - self.last_frame_update > self.frame_delay:
            num_frames = len(self.animations[self.current_state])
            self.frame_index = (self.frame_index + 1) % num_frames
            
            frame_data = self.animations[self.current_state][self.frame_index]
            self._update_sprite_surface(frame_data[0])
            
            self.last_frame_update = current_time

    def load_animations(self, tileset_path: str) -> None:
        """
        Load animations from tileset
        
        Args:
            tileset_path: Path to tileset file
        """
        asset_loader = get_asset_loader()
        self.animations = asset_loader.load_sprite_sheet(
            tileset_path,
            (TILE_SIZE, TILE_SIZE),
            (255, 255, 255)  # White colorkey
        )
        logger.debug(f"Loaded animations from {tileset_path}")
