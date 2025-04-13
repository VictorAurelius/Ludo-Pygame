"""
Pawn entity module handling pawn movement and animations in the game.
"""

import pygame
from pygame.locals import *
import os
import xml.etree.ElementTree as ET

from src.utils.constants import (
    TILE_SIZE, MAP_WIDTH, MAP_HEIGHT,
    RED_FINISH_POSITIONS, BLUE_FINISH_POSITIONS,
    YELLOW_FINISH_POSITIONS, GREEN_FINISH_POSITIONS,
    PAWN_GROUPS, ANIMATION_PATHS
)

def load_animations_from_tileset(tileset_path):
    """Load and parse animation data from a tileset file"""
    animations = {}
    if not os.path.exists(tileset_path):
        return animations
        
    try:
        # Parse tileset XML
        tree = ET.parse(tileset_path)
        root = tree.getroot()
        
        # Get tileset dimensions
        tilewidth = int(root.get('tilewidth', 0))
        tileheight = int(root.get('tileheight', 0))
        
        # Load spritesheet image
        image_element = root.find('image')
        if image_element is not None:
            image_path = image_element.get('source')
            base_dir = os.path.dirname(tileset_path)
            image_path = os.path.normpath(os.path.join(base_dir, image_path))
            
            if os.path.exists(image_path):
                spritesheet = pygame.image.load(image_path).convert_alpha()
                
                # Process each tile's animation
                for tile_elem in root.findall('tile'):
                    tile_id = int(tile_elem.get('id', 0))
                    
                    # Get animation name from properties
                    prop_elem = tile_elem.find('properties/property[@name="animation_name"]')
                    if prop_elem is not None:
                        animation_name = prop_elem.get('value')
                        
                        if animation_name:
                            animation_elem = tile_elem.find('animation')
                            if animation_elem is not None:
                                animation_frames = []
                                
                                # Process each frame
                                for frame_elem in animation_elem.findall('frame'):
                                    frame_id = int(frame_elem.get('tileid', 0))
                                    duration = int(frame_elem.get('duration', 100))
                                    
                                    # Calculate frame position in spritesheet
                                    columns = int(root.get('columns', 1))
                                    frame_x = (frame_id % columns) * tilewidth
                                    frame_y = (frame_id // columns) * tileheight
                                    
                                    # Extract frame from spritesheet
                                    frame_image = pygame.Surface((tilewidth, tileheight), pygame.SRCALPHA)
                                    frame_image.blit(spritesheet, (0, 0),
                                                   pygame.Rect(frame_x, frame_y, tilewidth, tileheight))
                                    
                                    animation_frames.append((frame_image, duration))
                                
                                if animation_frames:
                                    animations[animation_name] = animation_frames
    except Exception as e:
        print(f"Error loading animation from tsx: {e}")
    
    return animations

def scale_finish_dict(finish_dict, scale):
    """Scale finish position coordinates by the given factor"""
    return {k: ((v[0] * scale) - 13, (v[1] * scale) - 13) for k, v in finish_dict.items()}

class Pawn(pygame.sprite.Sprite):
    """
    Pawn sprite class representing a game piece that can move on the board
    and animate based on its state and movement.
    """
    
    def __init__(self, surf, dict_positions, startpos, number):
        """
        Initialize a pawn
        
        Args:
            surf: Surface for the pawn sprite
            dict_positions: Dictionary of board positions
            startpos: Starting position tuple (x, y)
            number: Pawn number (1-4)
        """
        super().__init__()
        self.surf = surf
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        
        # Position and movement attributes
        self.counter = 0  # Current position counter
        self.dict = dict_positions
        self.number = number
        self.startpos = startpos
        self.rect = self.surf.get_rect(center=startpos)
        
        # State flags
        self.activepawn = (number == 1)  # First pawn starts active
        self.king = False
        self.kingPawn = 0
        
        # Teleport attributes
        self.teleporting = False
        self.teleport_phase = None
        self.teleport_target = None
        
        # Animation attributes
        self.is_move = False
        self.animation_path = []
        self.animation_index = 0
        self.animation_speed = 1
        self.current_state = "stand_left"
        self.frame_index = 0
        self.last_frame_update = pygame.time.get_ticks()
        self.animations = {}
        self.frame_delay = 100
        
        # Finish state
        self.has_reached_finish = False
        self.finish_position = None

    def move(self, dice, statekeeper):
        """Move the pawn according to dice roll"""
        old_counter = self.counter
        self.counter += dice
        
        if self.counter in (96, 97):
            self._handle_finish(statekeeper)
        elif self.counter > 97:
            self.counter -= dice
        
        # Setup animation for movement
        self.setup_animation_path(old_counter, self.counter)
        self.is_move = True
        self.animation_index = 0
        self.last_frame_update = pygame.time.get_ticks()
        
        statekeeper.reset_counterlist_status()

    def _handle_finish(self, statekeeper):
        """Handle pawn reaching finish position"""
        self.kingPawn += 1
        
        # Find pawn's player and color
        player_color = None
        for player in statekeeper.players:
            if self in player.pawnlist:
                player_color = player.color
                if not self.has_reached_finish:
                    player.pawns_home += 1
                break
        
        # Get finish positions for color
        finish_positions = {
            "Red": RED_FINISH_POSITIONS,
            "Blue": BLUE_FINISH_POSITIONS,
            "Yellow": YELLOW_FINISH_POSITIONS,
            "Green": GREEN_FINISH_POSITIONS
        }.get(player_color)
        
        if finish_positions:
            scaled_positions = scale_finish_dict(finish_positions, TILE_SIZE)
            if self.number in scaled_positions:
                self.finish_position = scaled_positions[self.number]
                self.has_reached_finish = True
        
        self.activepawn = False
        self.king = True

    def start_teleport(self, target_pos):
        """Start teleport animation to target position"""
        self.teleporting = True
        self.teleport_phase = "starting"
        self.teleport_target = target_pos
        self.current_state = "teleport_starting"
        self.frame_index = 0
        self.last_frame_update = pygame.time.get_ticks()
        
        # Determine direction after teleport
        self.teleport_direction = "right" if target_pos[0] > self.rect.center[0] else "left"

    def setup_animation_path(self, start_pos, end_pos):
        """Setup path for smooth movement animation"""
        self.animation_path = []
        self.direction_changes = []
        steps_per_square = 10
        
        # Get current direction from state
        parts = self.current_state.split('_')
        prev_direction = parts[-1] if len(parts) > 1 else "left"
        last_known_horizontal_direction = prev_direction
        
        for pos in range(start_pos + 1, end_pos + 1):
            current_pos = self.rect.center if pos == start_pos + 1 else self.dict[pos-1]
            target_pos = self.dict[pos]
            
            # Determine movement direction
            dx = target_pos[0] - current_pos[0]
            dy = target_pos[1] - current_pos[1]
            
            if abs(dx) > abs(dy):
                direction = "right" if dx > 0 else "left"
                last_known_horizontal_direction = direction
            else:
                direction = last_known_horizontal_direction
            
            # Create intermediate steps
            for step in range(1, steps_per_square + 1):
                progress = step / steps_per_square
                x = current_pos[0] + (target_pos[0] - current_pos[0]) * progress
                y = current_pos[1] + (target_pos[1] - current_pos[1]) * progress
                self.animation_path.append((x, y))
                self.direction_changes.append(direction)
        
        if self.direction_changes:
            self.current_state = f"walk_{self.direction_changes[0]}"

    def update_animation(self):
        """Update pawn animation state"""
        if self.teleporting:
            self._update_teleport_animation()
        elif self.is_move:
            self._update_movement_animation()
        elif self.current_state in self.animations:
            self._update_standing_animation()

    def _update_teleport_animation(self):
        """Update teleport animation state"""
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_frame_update > self.frame_delay:
            animation_key = f"teleport_{self.teleport_phase}"
            
            if animation_key in self.animations:
                num_frames = len(self.animations[animation_key])
                self.frame_index += 1
                
                if self.frame_index >= num_frames:
                    if self.teleport_phase == "starting":
                        self.rect.center = self.teleport_target
                        self.teleport_phase = "end"
                        self.current_state = "teleport_end"
                        self.frame_index = 0
                    else:
                        self.teleporting = False
                        self.teleport_phase = None
                        self.current_state = f"stand_{self.teleport_direction}"
                        self.frame_index = 0
                        self.just_finished_animation = True
                else:
                    self._update_sprite_frame(animation_key)
                
                self.last_frame_update = current_time

    def _update_movement_animation(self):
        """Update movement animation state"""
        if self.animation_index < len(self.animation_path):
            current_time = pygame.time.get_ticks()
            
            if not hasattr(self, 'last_animation_time'):
                self.last_animation_time = current_time
            
            if current_time - self.last_animation_time > self.animation_speed * 10:
                if self.animation_index < len(self.direction_changes):
                    direction = self.direction_changes[self.animation_index]
                    walk_state = f"walk_{direction}"
                    
                    if self.current_state != walk_state:
                        self.current_state = walk_state
                        self.frame_index = 0
                
                self.rect.center = self.animation_path[self.animation_index]
                self.animation_index += 1
                self.last_animation_time = current_time
            
            if self.current_state in self.animations:
                self._update_sprite_animation()
        else:
            self._finish_movement_animation()

    def _update_standing_animation(self):
        """Update standing animation state"""
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_frame_update > self.frame_delay:
            num_frames = len(self.animations[self.current_state])
            self.frame_index = (self.frame_index + 1) % num_frames
            self._update_sprite_frame(self.current_state)
            self.last_frame_update = current_time

    def _update_sprite_frame(self, animation_key):
        """Update sprite with current animation frame"""
        frame_data = self.animations[animation_key][self.frame_index]
        self.surf = frame_data[0]
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        old_center = self.rect.center
        self.rect = self.surf.get_rect(center=old_center)

    def _finish_movement_animation(self):
        """Handle completion of movement animation"""
        self.is_move = False
        if self.has_reached_finish and self.finish_position:
            self.start_teleport(self.finish_position)
            self.has_reached_finish = False
        else:
            self.just_finished_animation = True
            if hasattr(self, 'direction_changes') and self.direction_changes:
                self.current_state = f"stand_{self.direction_changes[-1]}"
            else:
                self.current_state = "stand_left"
            self.frame_index = 0

    def load_animations(self, tileset_path):
        """Load animations from tileset file"""
        self.animations = load_animations_from_tileset(tileset_path)

    def update_pawn_state(self, active_player, next_player):
        """Update pawn states after a move"""
        next_pawn_index = self.number % 4
        active_player.pawnlist[next_pawn_index].activepawn = True
        self.set_next_player_pawn(next_player)

    def set_next_player_pawn(self, next_player):
        """Set active pawn for next player"""
        for pawn in next_player.pawnlist:
            if pawn.activepawn:
                pawn.activepawn = False
                next_pawn_index = pawn.number % 4
                next_player.pawnlist[next_pawn_index].activepawn = True
                break
