"""
Game state management module handling game flow and player states.
"""

from typing import List, Optional
import logging

from src.utils.logger_config import get_logger
from src.utils.event_handler import get_event_handler, GameEvent
from src.utils.constants import SPRITE_GROUPS

logger = get_logger(__name__)

class Statekeep:
    """
    Manages game state, player turns, and active status of all game elements.
    Acts as a central state manager for the game.
    """
    
    def __init__(self):
        """Initialize game state manager"""
        # Game state flags
        self.gamestart = False
        self.firstturn = False
        
        # Player groups
        self.players: List[Player] = []
        self.redpawns = SPRITE_GROUPS['Red']
        self.bluepawns = SPRITE_GROUPS['Blue']
        self.yellowpawns = SPRITE_GROUPS['Yellow']
        self.greenpawns = SPRITE_GROUPS['Green']
        
        # Active status for players
        self.redActive = False
        self.blueActive = False
        self.yellowActive = False
        self.greenActive = False
        
        # Counter tracking
        self.redcounters: List[int] = []
        self.bluecounters: List[int] = []
        self.yellowcounters: List[int] = []
        self.greencounters: List[int] = []
        
        # Turn tracking
        self.turn_states = {
            'red': True,
            'blue': False,
            'yellow': False,
            'green': False
        }
        self.redTurn = False
        self.blueTurn = False
        self.yellowTurn = False
        self.greenTurn = False
        
        # Active state tracking
        self.active_states = {
            'red': True,
            'blue': False,
            'yellow': False,
            'green': False
        }
        
        # Initialize players and state
        self._init_players()
        self._init_state()
        
        # Event handler
        self.event_handler = get_event_handler()
        logger.info("Game state manager initialized")

    def _init_players(self) -> None:
        """Initialize player objects"""
        player_configs = [
            ('Player1', 'Red', self.redpawns),
            ('Player2', 'Blue', self.bluepawns),
            ('Player3', 'Yellow', self.yellowpawns),
            ('Player4', 'Green', self.greenpawns)
        ]
        
        for name, color, pawns in player_configs:
            from src.entities.Players import Player
            player = Player(name, color, pawns, self)
            self.players.append(player)
            setattr(self, f'player{color}', player)
        
        logger.debug("Players initialized")

    def _init_state(self) -> None:
        """Initialize game state"""
        self.activeplayer = self.players[0]  # Red starts
        self.nextplayer = self.players[1]    # Blue is next
        self.display_player = None
        
        # Set initial counters
        self.set_counterlist_status()
        logger.debug("Initial game state set")

    def start_game(self) -> None:
        """Initialize game state"""
        self.gamestart = True
        self.firstturn = True
        self.event_handler.trigger_game_event(GameEvent.GAME_START)
        logger.info("Game started")

    def set_counterlist_status(self) -> None:
        """Update pawn counter lists with current positions"""
        for color in ['red', 'blue', 'yellow', 'green']:
            counters = getattr(self, f'{color}counters')
            pawns = getattr(self, f'{color}pawns')
            counters.clear()
            counters.extend(pawn.counter for pawn in pawns)

    def reset_counterlist_status(self) -> None:
        """Reset and update all counter lists"""
        self.set_counterlist_status()

    def update_active_player(self) -> None:
        """Update active player based on current state"""
        for i, player in enumerate(self.players):
            if self.active_states[player.color.lower()]:
                self.activeplayer = player
                break
        logger.debug(f"Active player updated to {self.activeplayer.color}")

    def update_player_turn(self) -> None:
        """Update current turn status"""
        for i, player in enumerate(self.players):
            if self.turn_states[player.color.lower()]:
                self.currentTurn = player
                break

    def update_players(self) -> None:
        """Update all players' status"""
        for player in self.players:
            player.update_self()

    def update(self) -> None:
        """Update all game state components"""
        self.reset_counterlist_status()
        self.update_active_player()
        self.update_player_turn()
        self.update_players()

    def move_player(self) -> None:
        """Handle player movement and turn progression"""
        current_player = None
        next_color = None
        
        # Find current player and next color
        for color, is_turn in self.turn_states.items():
            if is_turn:
                current_player = getattr(self, f'player{color.capitalize()}')
                colors = list(self.turn_states.keys())
                next_index = (colors.index(color) + 1) % len(colors)
                next_color = colors[next_index]
                break
        
        if current_player:
            # Execute turn
            current_player.Turn()
            
            # Update turn states
            for color in self.turn_states:
                self.turn_states[color] = (color == next_color)
            
            # Trigger turn end event
            self.event_handler.trigger_game_event(
                GameEvent.TURN_END,
                player=current_player,
                next_color=next_color
            )
            
            logger.debug(f"Turn completed: {current_player.color} -> {next_color}")

    def update_display_player(self) -> None:
        """Update the currently displayed player"""
        for color, is_turn in self.turn_states.items():
            if is_turn:
                self.display_player = getattr(self, f'player{color.capitalize()}')
                break

    def find_next_valid_player(self) -> None:
        """Find the next player who hasn't finished the game"""
        current_color = None
        
        # Find current player color
        for color, is_turn in self.turn_states.items():
            if is_turn:
                current_color = color
                break
        
        if current_color:
            colors = list(self.turn_states.keys())
            current_index = colors.index(current_color)
            
            # Check next players in order
            for i in range(1, len(colors)):
                next_index = (current_index + i) % len(colors)
                next_color = colors[next_index]
                next_player = getattr(self, f'player{next_color.capitalize()}')
                
                if next_player.pawns_home < 4:
                    # Update turn states
                    for color in self.turn_states:
                        self.turn_states[color] = (color == next_color)
                    logger.debug(f"Next valid player: {next_color}")
                    return
            
            # If no valid player found, keep current
            logger.debug(f"No valid next player, keeping {current_color}")
            self.turn_states[current_color] = True

    @property
    def game_complete(self) -> bool:
        """Check if game is complete"""
        return all(player.pawns_home >= 4 for player in self.players)