"""
Player entity module handling player state and actions.
"""

import random
from typing import List, Optional

from src.utils.logger_config import get_logger
from src.utils.event_handler import get_event_handler, GameEvent
from src.utils.asset_loader import get_asset_loader

logger = get_logger(__name__)

class Player:
    """
    Player class representing a game player with their pawns and state.
    Manages player turns, dice rolls, and pawn movements.
    """
    
    def __init__(self, name: str, color: str, pawns: List['Pawn']):
        """
        Initialize a player
        
        Args:
            name: Player name
            color: Player color (Red, Blue, Yellow, Green)
            pawns: List of pawns belonging to this player
        """
        self.name = name
        self.color = color
        self.pawnlist = pawns
        
        # State tracking
        self.times_kicked = 0
        self.pawns = 0
        self.pawns_home = 0
        self.active = False
        self.turn = False
        
        # Dice state
        self.dice1 = 0
        self.dice2 = 0
        
        # Player flags
        self.player_number = None
        self._init_player_flags()
        
        # Event handler
        self.event_handler = get_event_handler()
        
        # References to be set later
        self.statekpr = None
        self.active_player = None
        self.next_player = None
        
        logger.info(f"Initialized {color} player: {name}")

    def _init_player_flags(self) -> None:
        """Initialize player number flags"""
        for i in range(1, 5):
            flag_name = f'Player{i}'
            if self.name == flag_name:
                self.player_number = i
                setattr(self, flag_name, True)
            else:
                setattr(self, flag_name, False)

    def set_statekeeper(self, statekeeper: 'Statekeep') -> None:
        """
        Set statekeeper references
        
        Args:
            statekeeper: Game state manager
        """
        self.statekpr = statekeeper
        self.players = statekeeper.players
        
        # Set player reference based on number
        if self.player_number:
            player_attrs = {
                1: 'playerRed',
                2: 'playerBlue',
                3: 'playerYellow',
                4: 'playerGreen'
            }
            if self.player_number in player_attrs:
                self.player = getattr(statekeeper, player_attrs[self.player_number])
                logger.debug(f"Set statekeeper for {self.color} player")

    def update_self(self) -> None:
        """Update player state from statekeeper"""
        if self.player_number:
            active_attrs = {
                1: ('redActive', 'redTurn'),
                2: ('blueActive', 'blueTurn'),
                3: ('yellowActive', 'yellowTurn'),
                4: ('greenActive', 'greenTurn')
            }
            
            if self.player_number in active_attrs:
                active_attr, turn_attr = active_attrs[self.player_number]
                self.active = getattr(self.statekpr, active_attr)
                self.turn = getattr(self.statekpr, turn_attr)

    def update_statekeeper(self) -> None:
        """Update statekeeper with current player state"""
        if self.player_number:
            state_attrs = {
                1: ('redActive', 'redTurn'),
                2: ('blueActive', 'blueTurn'),
                3: ('yellowActive', 'yellowTurn'),
                4: ('greenActive', 'greenTurn')
            }
            
            if self.player_number in state_attrs:
                active_attr, turn_attr = state_attrs[self.player_number]
                setattr(self.statekpr, active_attr, self.active)
                setattr(self.statekpr, turn_attr, self.turn)
        
        # Update active and next player references
        self.statekpr.active_player = self.active_player
        self.statekpr.next_player = self.next_player

    def update_active_and_next(self) -> None:
        """Update active and next player references"""
        self.active_player = self.statekpr.active_player
        self.next_player = self.set_next_player()

    def set_next_player(self) -> 'Player':
        """
        Determine the next player in turn order
        
        Returns:
            Player: Next player in sequence
        """
        current_index = self.players.index(self.active_player)
        next_index = (current_index + 1) % len(self.players)
        return self.players[next_index]

    def dice_roll(self) -> int:
        """
        Roll two dice and return total
        
        Returns:
            int: Sum of both dice rolls
        """
        self.dice1 = random.randint(1, 6)
        self.dice2 = random.randint(1, 6)
        total = self.dice1 + self.dice2
        
        # Trigger dice roll event
        self.event_handler.trigger_game_event(
            GameEvent.DICE_ROLL,
            player=self,
            dice1=self.dice1,
            dice2=self.dice2,
            total=total
        )
        
        logger.debug(f"{self.color} rolled {self.dice1} + {self.dice2} = {total}")
        return total

    def move_out_onto_board(self) -> None:
        """Attempt to move a pawn from start onto the board"""
        roll = self.dice_roll()
        if roll >= 10:
            self.pawns += 1
            self.active = True
            self.update_statekeeper()
            
            # Trigger pawn activation event
            self.event_handler.trigger_game_event(
                GameEvent.PAWN_MOVE,
                player=self,
                pawn_activated=True
            )
            
            self.move()
            logger.debug(f"{self.color} moved pawn onto board")

    def turn(self) -> None:
        """Handle player's turn"""
        self.event_handler.trigger_game_event(
            GameEvent.TURN_START,
            player=self
        )
        
        self.update_active_and_next()
        if self.pawns < 1:
            self.move_out_onto_board()
        else:
            self.move()
            
        self.event_handler.trigger_game_event(
            GameEvent.TURN_END,
            player=self
        )

    def move(self) -> None:
        """Move the currently active pawn"""
        distance = self.dice_roll()
        
        for pawn in self.pawnlist:
            if pawn.active_pawn:
                pawn.move(distance, self.statekpr)
                pawn.update_pawn_state(self.active_player, self.next_player)
                
                # Trigger pawn movement event
                self.event_handler.trigger_game_event(
                    GameEvent.PAWN_MOVE,
                    player=self,
                    pawn=pawn,
                    distance=distance
                )
                break
        
        self.update_statekeeper()

    @property
    def has_won(self) -> bool:
        """Check if player has won"""
        return self.pawns_home >= 4
