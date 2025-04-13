"""
Game state management module handling game flow and player states.
"""

import pygame
from src.entities.Players import Player
from src.entities.Pawns import (
    redPawn as RedPawnList,
    bluePawn as BluePawnList,
    yellowPawn as YellowPawnList,
    greenPawn as GreenPawnList
)

class Statekeep:
    """
    Manages the game state, player turns, and active status of all game elements.
    Acts as a central state manager for the game.
    """
    
    def __init__(self):
        """Initialize game state manager"""
        # Game state flags
        self.gamestart = False
        self.firsturn = False
        
        # Initialize turn states
        self.redTurn = True
        self.blueTurn = False
        self.yellowTurn = False
        self.greenTurn = False
        self.turnlist = [self.redTurn, self.blueTurn, self.yellowTurn, self.greenTurn]
        
        # Initialize active states
        self.redActive = True
        self.blueActive = False
        self.yellowActive = False
        self.greenActive = False
        self.activelist = [self.redActive, self.blueActive, self.yellowActive, self.greenActive]
        
        # Initialize pawn groups
        self.redpawns = RedPawnList
        self.bluepawns = BluePawnList
        self.yellowpawns = YellowPawnList
        self.greenpawns = GreenPawnList
        
        # Initialize counter tracking
        self.redcounters = []
        self.bluecounters = []
        self.yellowcounters = []
        self.greencounters = []
        
        # Create and initialize players
        self.players = self._init_players()
        self.playerRed, self.playerBlue, self.playerYellow, self.playerGreen = self.players
        
        # Set initial active players
        self.activeplayer = self.playerRed
        self.nextplayer = self.playerBlue
        self.display_player = None
        
        # Initialize counter status
        self.set_counterlist_status()

    def _init_players(self):
        """Initialize player objects with their respective pawns"""
        players = [
            Player('Player1', 'Red', self.redpawns),
            Player('Player2', 'Blue', self.bluepawns),
            Player('Player3', 'Yellow', self.yellowpawns),
            Player('Player4', 'Green', self.greenpawns)
        ]
        return players

    def start_game(self):
        """Initialize game state"""
        self.gamestart = True
        self.firstturn = True

    def set_counterlist_status(self):
        """Update pawn counter lists with current positions"""
        self._update_counter_list(self.redcounters, self.redpawns)
        self._update_counter_list(self.bluecounters, self.bluepawns)
        self._update_counter_list(self.yellowcounters, self.yellowpawns)
        self._update_counter_list(self.greencounters, self.greenpawns)

    def _update_counter_list(self, counter_list, pawns):
        """Helper method to update a single counter list"""
        counter_list.clear()
        for pawn in pawns:
            counter_list.append(pawn.counter)

    def reset_counterlist_status(self):
        """Reset and update all counter lists"""
        self.set_counterlist_status()

    def update_active_player(self):
        """Update the active player based on current state"""
        for i, is_active in enumerate(self.activelist):
            if is_active:
                self.activeplayer = self.players[i]
                break

    def update_player_turn(self):
        """Update current turn status"""
        for i, is_turn in enumerate(self.turnlist):
            if is_turn:
                self.currentTurn = self.players[i]
                break

    def update_players(self):
        """Update all players' status"""
        for player in self.players:
            player.update_self()

    def update(self):
        """Update all game state components"""
        self.reset_counterlist_status()
        self.update_active_player()
        self.update_player_turn()
        self.update_players()

    def move_player(self):
        """Handle player movement and turn progression"""
        if self.redTurn:
            self._handle_player_turn(self.playerRed, 'blue')
        elif self.blueTurn:
            self._handle_player_turn(self.playerBlue, 'yellow')
        elif self.yellowTurn:
            self._handle_player_turn(self.playerYellow, 'green')
        elif self.greenTurn:
            self._handle_player_turn(self.playerGreen, 'red')

    def _handle_player_turn(self, current_player, next_color):
        """Helper method to handle a single player's turn"""
        current_player.Turn()
        self._set_next_turn(next_color)

    def _set_next_turn(self, color):
        """Set the next player's turn"""
        self.redTurn = color == 'red'
        self.blueTurn = color == 'blue'
        self.yellowTurn = color == 'yellow'
        self.greenTurn = color == 'green'

    def update_display_player(self):
        """Update the currently displayed player"""
        self.display_player = {
            True: {
                'redTurn': self.playerRed,
                'blueTurn': self.playerBlue,
                'yellowTurn': self.playerYellow,
                'greenTurn': self.playerGreen
            }
        }[True].get(next(name for name, value in vars(self).items() 
                        if name.endswith('Turn') and value), self.display_player)

    def find_next_valid_player(self):
        """Find the next player who hasn't finished the game"""
        current_turns = {
            'redTurn': (self.playerBlue, self.playerYellow, self.playerGreen),
            'blueTurn': (self.playerYellow, self.playerGreen, self.playerRed),
            'yellowTurn': (self.playerGreen, self.playerRed, self.playerBlue),
            'greenTurn': (self.playerRed, self.playerBlue, self.playerYellow)
        }
        
        current_turn = next(name for name, value in vars(self).items() 
                          if name.endswith('Turn') and value)
        
        if current_turn in current_turns:
            next_players = current_turns[current_turn]
            for next_player in next_players:
                if next_player.pawns_home < 4:
                    self._set_next_turn(next_player.color.lower())
                    return
            
            # If no valid next player, keep current turn
            if current_turn == 'redTurn':
                self.redTurn = True
            elif current_turn == 'blueTurn':
                self.blueTurn = True
            elif current_turn == 'yellowTurn':
                self.yellowTurn = True
            elif current_turn == 'greenTurn':
                self.greenTurn = True