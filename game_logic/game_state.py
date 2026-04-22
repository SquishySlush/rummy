# -*- coding: utf-8 -*-
"""
Created on Sun Mar  8 15:38:39 2026

@author: Faisal Mustafa
"""
from game_logic.card import Card
from game_logic.deck import Deck
from game_logic.ruleset import Ruleset
from game_logic.discard_pile import Discard_pile
from game_logic.validator import Validator
from game_logic.utils import Moves, quicksort

from enum import Enum

class GameStatus(Enum):
    LOBBY = "Lobby"
    IN_PROGRESS = "In Progress"
    GAME_OVER = "Game Over"
    PAUSED = "Paused"

class GameState:
    def __init__(self, player, ruleset=None, seed=None):
        
        self.ruleset = ruleset or Ruleset()
        self.game_state = GameStatus.LOBBY
        
        self.players = [player] #list of player objects, initally just the user who makes the lobby

        self.deck = None
        self.discard_pile = None
        self.table_melds = []
        self.winner = None
        self.current_required_meld_score = self.ruleset.min_initial_meld_score
        self.seed = seed or None
        
        self.current_player_index = 0
    
    def update_ruleset(self, new_ruleset):
        if self.game_state != GameStatus.LOBBY:
            return False, "Can't Change Rules After Game Began"
        
        self.ruleset = new_ruleset
        return True, "Rules Updated"
    
    def add_player(self, new_player):
        if self.game_state == GameStatus.LOBBY:
            if len(self.players) < self.ruleset.max_players:
                self.players.append(new_player)
            else:
                return "Game Has Begun"

    
    def ready(self, player):
        player.ready = True

    def start_game(self, ruleset):
        if self.game_state != GameStatus.LOBBY:
            return False, "Game Already Started"
        for player in self.players:
            if not player.ready:
                return False, "Not All Players Ready"
        #Initialises the game and deals cards
        new_ruleset = Ruleset.from_dict(ruleset)
        self.update_ruleset(new_ruleset)
        self.game_state = GameStatus.IN_PROGRESS
        
        #Shuffles the deck
        self.deck = Deck(self.ruleset, self.seed)
        self.deck.shuffle()
        
        self.discard_pile = Discard_pile()
        
        for player in self.players:
            for i in range(self.ruleset.initial_hand_size):
                player.hand.add_card(self.deck.draw()) #Draws cards from the deck until it reaches the initial hand size
        
        #Puts first card into the discard pile
        self.discard_pile.add_card(self.deck.draw())
        
        return True, "Game Started"
    
    def pause_game(self):
        self.game_state = GameStatus.PAUSED
    
    def return_current_player(self):
        return self.players[self.current_player_index]
    
    def next_turn(self):
        self.current_player_index = (self.current_player_index+1) % len(self.players)
        #Adds one, but wraps around to 0 due to taking the modulus of the amount of playeres
    
    def draw_from_deck(self, player):
        
        valid, error = Validator.validate_draw(self.deck.peek, self.deck, player.has_drawn)
        
        if valid:
            player.add_card(self.deck.draw())
            player.has_drawn = True
            return True, None
        else:
            return valid, error
        
    def draw_from_discard_pile(self, player):
        valid, error = Validator.validate_draw_discard(self.discard_pile.peek(), self.discard_pile, player.has_drawn, player.has_melded, player.ruleset)
        if valid:
            card = self.discard_pile.draw_top_card()
            player.add_card(card)
            player.has_drawn = True
            player.drawn_from_discard_pile = card
            return valid, None
        else:
            return valid, error
                
                
    def play_stored_melds(self, player):
            
        success, error_or_stored_melds = Validator.validate_play_melds(player.current_stored_melds, player.has_melded, self.ruleset, self.current_required_meld_score)
        
        if not success:
            return success, error_or_stored_melds
                
        for meld in player.stored_melds:
            for card in meld.cards:
                player.hand.remove_card(card)
        
        self.table_melds += player.current_stored_melds
        
        self.update_required_meld_score(player.return_stored_meld_score(self.ruleset))
        
        player.completed_stored_melds += player.current_stored_melds
        
        player.reset_current_stored_melds()
        
        return success, error_or_stored_melds
        
    def discard(self, player, card):
        
        valid, error = Validator.validate_discard(card, player.hand.cards, self.discard_pile, player.has_drawn, player.has_drawn_from_discard, self.ruleset)
        
        if valid:
            player.hand.remove_card(card)
            self.discard_pile.add_card(card)
            self.next_turn()
            return True, None
        else:
            return False, error
    
    def lay_off(self, player, card, meld):
        
        valid, error = Validator.validate_lay_off(card, meld, self.ruleset)
        
        if valid:
            player.hand.remove_card(card)
            meld.add_card(card)
            return True, None
        else:
            return False, error
        
    def update_required_meld_score(self, score):
        if self.ruleset.initial_meld_increment:
            if self.current_required_meld_score < score:
                self.current_required_meld_score = score
    
    def game_end(self, winning_player):
        
        deadwoods = []
        for player in self.players:
            if player != winning_player:
                deadwood = player.hand.calculate_deadwood(self.ruleset)
                player.add_to_score(self.ruleset, -deadwood)
                deadwoods.append(player, deadwood)
                
        winning_player.add_to_score(self.ruleset, self.ruleset.winner_deadwood)
        deadwoods.append(winning_player, self.ruleset.winner_deadwood)
        
        if self.ruleset.scoring_method == 'negative':
            deadwoods = quicksort(deadwoods, key=lambda x: x[1])
        else:
            deadwoods = quicksort(deadwoods, key=lambda x: x[1], reverse=True)
        
        placement_results = {}
        
        for place, (player, score) in enumerate(deadwoods):
            placement_results[place + 1] = (player, score)
        
        
    
    def check_win_condition(self, player):
        if player.hand.is_empty():
            self.game_state = GameStatus.GAME_OVER
            self.winner = player
            return self.winner
        else:
            return None
        
    
    def return_game_state(self):
        return self.game_state
    
    def return_winner(self):
        return self.winner
    
    def get_player_by_id(self, player_id):
        for player in self.players:
            if player.player_id == player_id:
                return player
        return None
    
    def _select_card(self, player, card):
        player.select_card(card)

    def deselect_all(self, player):
        player.deselect_all()

    def _deselect_card(self, player, card):
        player.deselect_card(card)
    
    def _get_card_from_dcit(self, card_dict):
        return Card.from_dict(card_dict, self.ruleset)
    
    def apply_move(self, move):
        move_type = Moves[move["move_type"]]
        player = self.get_player_by_id(move["user_id"])
        
        if move_type == Moves.Draw_Deck:
            return self.draw_from_deck(player)
        
        elif move_type == Moves.Draw_Discard:
            return self.draw_from_discard_pile(player)
        
        elif move_type == Moves.Discard:
            card = self._get_card_from_dcit(move["card"])
            valid, error = self.discard(player, card)
            if not valid:
               return False, error
            self.check_win_condition(player)
            return True, None
        
        elif move_type == Moves.Store_Meld:
            return player.store_meld(self.ruleset)
        
        elif move_type == Moves.Meld:
            return self.play_stored_melds(player)
        
        elif move_type == Moves.Lay_Off:
            card = self._get_card_from_dcit(move["card"])
            meld = self.table_melds[move["meld_index"]]
            return self.lay_off(player, card, meld)
        
        elif move_type == Moves.Deck_Shuffle:
            self.deck.shuffle()
            return True, None
        
        elif move_type == Moves.Store_Card:
            self._select_card(player)
            return True, None
        
        elif move_type == Moves.Deselect_all:
            self.deselect_all(player)
        
        elif move_type == Moves.Sort_Rank:
            player.sort_rank()
            return True, None
        
        elif move_type == Moves.Sort_Suit:
            player.sort_suit()
            return True, None

        else:
            return False, "Unknown Move"