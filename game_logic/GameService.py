# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 19:14:42 2026

@author: Faisal Mustafa
"""

from game_state import GameState, GameStatus
from player import Player
from hand import Hand

class GameService:
    def __init__(self, db_service):
        self.active_games = {}
        self.active_players = {}
        self.db = db_service
    
    def create_game(self, user_id, ruleset, seed):
        player, error = self.get_active_player(user_id)
        if player is None:
            return False, error
        success, game_id = self.db.create_game(ruleset, seed)
        if not success:
            return False, "could Not Create Game"
        game = GameState(player, ruleset)
        self.active_games[game_id] = game
        return game_id, None
    
    def add_player(self, game_id):
        new_player, error = self.get_active_player(user_id)
        if new_player is None:
            return False, error
        game = self.active_games[game_id]
        if game.game_state != "Lobby":
            return False, "Game Not Available"
            
        return True, game.add_player(new_player)
        
    def start_game(self, game_id):
        game = self.active_games[game_id]
        
        self.db.start_game(game.ruleset, game.deck.seed)
        
        for player in game.players:
            self.db.add_player_to_game(player.user_id, game_id, "Player")
        
        return game.start_game()
    
    def pause_game(self, game_id):
        game = self.active_games[game_id]
        
        self.db.pause_game()
        game.pause_game(game_id)
        del self.active_games[game_id]
    
    def load_paused_game(self, game_id, user_id):
        player, error = self.get_active_player(user_id)
        if player is None:
            return False, error
        
        row, error = self.db.get_game_status(game_id)
        
        if row is None:
            return error
        if row["status"] != "Paused":
            return "Game is not paused"
        
        history, error = self.db.get_player_history(player.player_id)
        if not history:
            return False, error
        if not any(row["game_id"] == game_id for row in history):
            return False, "Player Does Not Belong to This Game"
    
        
        ruleset, _ = self.db.get_ruleset(game_id)
        seed, _ = self.db.get_seed(game_id)
        
        game = GameState(player, ruleset, seed)
        self.active_games[game_id] = game
        return True, "Game Loaded"
    
    def rejoin_game(self, game_id, user_id):
        player, error = self.get_active_player(user_id)
        if player is None:
            return False, error
        
        history, error = self.db.get_player_history(player.player_id)
        if not history:
            return False, error
        
        game_ids = [row["game_id"] for row in history]
        
        if game_id not in game_ids:
            return False, "Player Doesn't Belong to This Game"

        return self.add_player(player, game_id)
    
    def resume_game(self, game_id):
        game = self.active_games[game_id]
        
        moves, error = self.db.get_moves(game_id)
        
        if not moves:
            return False, error
        
        for move in moves:
            game.apply_move(move)
        
        return True, "Game Resumed"
    
    def apply_move(self, 
                   game_id, 
                   user_id, 
                   move_type, 
                   card=None, 
                   cards=None, 
                   meld_index=None):
        
        
        game = self.active_games[game_id]
        
        move = {
            "move_type" : move_type,
            "user_id" : user_id,
            "card" : card,
            "cards" : cards,
            "meld_index" : meld_index
            }
        
        success, error = game.apply_move(move)
        
        if success:
            self.db.add_move(game_id, user_id, move['move_type'], card, cards, meld_index)
            if game.return_game_state() == GameStatus.GAME_OVER:
                self.end_game(game_id)
                
        return success, error
    
    def end_game(self, game_id):
        game = self.active_games[game_id]
        if game is None:
            return False, "Game Not Found"
        
        results = game.game_end(game.winner)
        
        for place, (player, score) in results.items():
            self.db.record_game_result(player.player_id, game_id, place, score)
            
        del self.active_games[game_id]
        return True, results
        
    def get_game_state(self, game_id, user_id):

        player, error = self.get_active_player(user_id)
        if player is None:
            return False, error
        
        game = self.active_games[game_id]
        
        game_status = game.game_state.value
        curent_player = game.return_current_player().player_id
        discard_top = game.discard_pile.peek().to_dict()
        deck_size = len(game.deck.cards)
        has_drawn = player.has_drawn
        has_melded = player.has_melded
        required_meld_score = game.current_required_meld_score
        winner = game.winner.player_id if game.winner else None
        
        hand = []
        for card in player.hand.cards:
            hand.append(card.to_dict())
        
        table_melds = []
        for meld in game.table_melds:
            meld_cards = []
            for card in meld.cards:
                meld.append(card.to_dict())
            table_melds.append(meld_cards)
        
        players = []
        for p in game.players:
            players.append({
                "player_id" : p.player_id,
                "username" : p.username,
                "hand_size" : len(p.hand.cards),
                "score" : p.score})
        
        state = {
            "game_status" : game_status,
            "curent_player" : curent_player,
            "discard_top" : discard_top,
            "deck_size" : deck_size,
            "has_drawn" : has_drawn,
            "has_melded" : has_melded,
            "required_meld_score" : required_meld_score,
            "hand" : hand,
            "table_melds" : table_melds,
            "players" : players,
            "winner" : winner}
        
        
        return state
    
    def get_active_player(self, user_id):
        player = self.active_players.get(user_id)
        if player is None:
            return None, "Player Not Found"
        return player, None

    def create_guest(self):
        success = False
        while not success:
            success, user = self.db.sign_up(f"Guest_{user_id}, None, None, True")
        hand = Hand()
        player = Player(user["user_id"], user["username"], hand)
        self.acive_players[user["user_id"]] = player
        return True


    def get_lobbies(self):
        return self.db.get_lobbies()
    
    def get_paused_game(self, user_id):
        return self.db.get_paused_games_by_user(user_id)
    
    def sign_up(self, username, password, email):
        return self.db.sign_up(username, password, email)
    
    def log_in(self, username, password):
        user, error = self.db.log_in(username, password)
        if user:
            hand = Hand()
            player = Player(user["user_id"], username, hand)
            self.active_players[user["user_id"]] = player
            return user, None
        return False, error

    def log_out(self, user_id, is_guest):
        user, _ = self.db.get_user_by_id(self.db, user_id)

        if user is None:
            return False, "No User To Log Out"
        if is_guest:
            self.db.delete_user()
        if user_id in self.active_players:
            del self.active_players[user_id]
        return True, "Logged Out"

    def delete_account(self, user_id):
        return self.db.delete_user(user_id)
    
    def change_password(self, user_id, old_password, new_password):
        return self.db.change_password(user_id, old_password, new_password)
    
    def change_username(self, user_id, new_username):
        return self.db.change_username(user_id, new_username)
    
    def send_friend_request(self, user_id, friend_id):
        return self.db.send_friend_request(user_id, friend_id)
    
    def accept_friend_request(self, user_id, friend_id):
        return self.db.accept_friend_request(user_id, friend_id)
    
    def reject_friend_request(self, user_id, friend_id):
        return self.db.reject_friend_request(user_id, friend_id)
    
    def get_friends(self, user_id):
        return self.db.get_friends(user_id)
    
    def get_pending_requests(self, user_id):
        return self.db.get_pending_requests(user_id)
    
    def get_player_history(self, user_id):
        return self.db.get_player_history(user_id)
    
    def get_player_current_game(self, player_id):
        for game_id, game in self.active_games.items():
            if any(p.player_id == player_id for p in game.players):
                return game_id
        return None