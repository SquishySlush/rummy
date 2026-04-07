# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 15:38:39 2026

@author: Faisal Mustafa
"""

from game_logic.deck import Deck
from game_logic.ruleset import Ruleset
from game_logic.hand import Hand
from game_logic.discard_pile import Discard_pile
from game_logic.player import Player
from game_logic.validator import Validator


from enum import Enum

class GameStatus(Enum):
    LOBBY = "Lobby"
    IN_PROGRESS = "In Progress"
    GAME_OVER = "Game Over"

class GameState:
    def __init__(self, player_ids, player_names, ruleset=None):
        
        self.ruleset = ruleset or Ruleset()
        self.game_state = GameStatus.LOBBY
        
        self.players - [] #list of player objects
        for i, p_id in enumerate((player_ids)):
            player = Player(p_id, player_names[i], Hand())
            self.players.append(player)
        
        self.deck = None
        self.discard_pile = None
        self.table_melds = []
        self.winner = None
        
        self.current_player_index = 0
    
    def update_ruleset(self, new_ruleset):
        if self.game_state != GameStatus.LOBBY:
            return False, "Can't Change Rules After Game Began"
        
        self.ruleset = new_ruleset
        return True, "Rules Updated"
        
    def start_game(self):
        if self.status != GameStatus.LOBBY:
            return False, "Game Already Started"
        #Initialises the game and deals cards
        self.game_state = GameStatus.IN_PROGRESS
        
        #Shuffles the deck
        self.deck = Deck(self.ruleset)
        self.deck.shuffle()
        
        self.discard_pile = Discard_pile()
        
        for player in self.players:
            for i in range(self.ruleset.initial_hand_size):
                player.hand.add_card(self.deck.draw()) #Draws cards from the deck until it reaches the initial hand size
        
        #Puts first card into the discard pile
        self.discard_pile.add_card(self.deck.draw())
        
        return True, "Game Started"
    
    def return_current_player(self):
        return self.players[self.current_player_index]
    
    def next_turn(self):
        self.current_player_index = (self.current_player_index+1) % len(self.players)
        #Adds one, but wraps around to 0 due to taking the modulus of the amount of playeres
    
    def draw_from_deck(self, player):
        
        if self.deck.empty_check():
            self.deck.add_cards(self.discard_pile.split_discard_pile())
            self.deck.shuffle()
        
        card = self.deck.draw()
        player.hand.add_card(card)
        return True, f"Drew {card}"

    def draw_from_discard_pile(self, player):
        if self.discard_pile.is_empty():
            return False, "Discard Pile Empty"
        
        card = self.discard_pile.draw_top_card()
        player.hand.add_card(card)
        return True, f"Drew {card}"
    
    def check_win_condition(self, player):
        if player.hand.is_empty():
            self.game_state = GameStatus.GAME_OVER
            self.winner = player
    
    def is_game_over(self):
        return self.game_state
    
    def return_winner(self):
        return self.winner
    
            