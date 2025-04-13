"""
Player entity module handling player state and actions in the game.
"""

import random
from src.entities.Pawns import Pawn

class Player:
    """
    Player class representing a game player with their pawns and state.
    Manages player turns, dice rolls, and pawn movements.
    """
    
    def __init__(self, name, color, pawns):
        """
        Initialize a player
        
        Args:
            name (str): Player name
            color (str): Player color (Red, Blue, Yellow, Green)
            pawns (list): List of Pawn objects belonging to this player
        """
        # Basic properties
        self.name = name
        self.color = color
        self.pawnlist = pawns
        
        # Game state tracking
        self.times_kicked = 0  # Times pawns kicked by opponents
        self.pawns = 0  # Number of pawns in play
        self.pawns_home = 0  # Number of pawns that reached home
        self.active = False  # Whether player has pawns on board
        self.turn = False  # Whether it's player's turn
        
        # Dice state
        self.dice1 = 0
        self.dice2 = 0
        
        # Player identification flags
        self.Player1 = False
        self.Player2 = False
        self.Player3 = False
        self.Player4 = False
        
        # Set player number based on name
        self.set_player_number()
        
        # References to be set later
        self.Statekpr = None
        self.players = None
        self.Player = None
        self.activeplayer = None
        self.nextplayer = None

    def set_player_number(self):
        """Set player number flag based on name"""
        player_flags = {
            'Player1': 'Player1',
            'Player2': 'Player2',
            'Player3': 'Player3',
            'Player4': 'Player4'
        }
        if self.name in player_flags:
            setattr(self, player_flags[self.name], True)

    def set_statekeeper(self, statekeeper):
        """
        Set statekeeper references
        
        Args:
            statekeeper: StateKeeper instance managing game state
        """
        self.Statekpr = statekeeper
        self.players = statekeeper.players
        
        # Set player reference based on color
        player_refs = {
            True: {
                'Player1': 'playerRed',
                'Player2': 'playerBlue',
                'Player3': 'playerYellow',
                'Player4': 'playerGreen'
            }
        }
        
        for flag, attr in player_refs[True].items():
            if getattr(self, flag, False):
                self.Player = getattr(statekeeper, attr)
                break

    def update_self(self):
        """Update player state from statekeeper"""
        state_flags = {
            'Player1': ('redActive', 'redTurn'),
            'Player2': ('blueActive', 'blueTurn'),
            'Player3': ('yellowActive', 'yellowTurn'),
            'Player4': ('greenActive', 'greenTurn')
        }
        
        for flag, (active_attr, turn_attr) in state_flags.items():
            if getattr(self, flag, False):
                self.active = getattr(self.Statekpr, active_attr)
                self.turn = getattr(self.Statekpr, turn_attr)
                break

    def update_statekeeper(self):
        """Update statekeeper with current player state"""
        state_updates = {
            'Player1': ('redActive', 'redTurn'),
            'Player2': ('blueActive', 'blueTurn'),
            'Player3': ('yellowActive', 'yellowTurn'),
            'Player4': ('greenActive', 'greenTurn')
        }
        
        for flag, (active_attr, turn_attr) in state_updates.items():
            if getattr(self, flag, False):
                setattr(self.Statekpr, active_attr, self.active)
                setattr(self.Statekpr, turn_attr, self.turn)
                break
        
        # Update active and next player references
        self.Statekpr.activeplayer = self.activeplayer
        self.Statekpr.nextplayer = self.nextplayer

    def update_active_and_next(self):
        """Update active and next player references"""
        self.activeplayer = self.Statekpr.activeplayer
        self.nextplayer = self.set_next_player()

    def set_next_player(self):
        """Determine the next player in turn order"""
        current_index = self.players.index(self.activeplayer)
        next_index = (current_index + 1) % len(self.players)
        return self.players[next_index]

    def dice_roll(self):
        """
        Roll two dice and return total
        
        Returns:
            int: Sum of both dice rolls
        """
        self.dice1 = random.randint(1, 6)
        self.dice2 = random.randint(1, 6)
        total = self.dice1 + self.dice2
        print(f"Dice 1: {self.dice1}, Dice 2: {self.dice2}, Total: {total}")
        return total

    def move_out_onto_the_board(self):
        """Attempt to move a pawn from start onto the board"""
        roll = self.dice_roll()
        if roll >= 10:
            self.pawns += 1
            self.active = True
            self.update_statekeeper()
            self.move()

    def turn(self):
        """Handle player's turn"""
        self.update_active_and_next()
        if self.pawns < 1:
            self.move_out_onto_the_board()
        else:
            self.move()

    def move(self):
        """Move the currently active pawn"""
        distance = self.dice_roll()
        
        # Find and move active pawn
        active_pawn = next((pawn for pawn in self.pawnlist if pawn.activepawn), None)
        if active_pawn:
            active_pawn.move(distance, self.Statekpr)
            active_pawn.update_pawn_state(self.activeplayer, self.nextplayer)
        
        self.update_statekeeper()
