# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 09:06:53 2026

@author: Faisal
"""

from game_logic.utils import sort_rank, index_rank, Suit, rank_score, MeldTypes, split_wilds_non_wilds

class Meld:
    def __init__(self, cards, meld_type, ruleset):
        self.cards = cards
        self.meld_type = meld_type #2 Meld types, set or run.
        self.wild_assignments = {} #A dictionary of wild cards, with their rank_index and suit
        
        if self.meld_type == MeldTypes.RUN:
            if ruleset.allow_runs:
                self._wild_assignment_run(ruleset)
        else:
            if ruleset.allow_sets:
                self._wild_assignment_set(ruleset)
    
    def __repr__(self):
        for card in self.cards:
            card_strings  = [str(card) for card in self.cards] #Creates a list of str(card) from self.cards
        return ',' .join(card_strings)
        
    # def _wild_assignment_run(self, ruleset):
        
    #     wilds, non_wilds = self._split_meld(ruleset)
        
    #     #Creates a sorted list of the indices of non wild cards
    #     sorted_non_wilds = sort_rank(non_wilds)
    #     indices = []
    #     for  card in sorted_non_wilds:
    #         indices.append(card.return_rank_index())
        
    #     #Creates a  list of the expected indices of the non wild cards
    #     range_indexes = range(indices[0], indices[-1] +1)
        
    #     #Finds the missing indices between cards, such that a card, wild, card is accounted for.
    #     missing_indices = []
    #     for index in range_indexes:
    #         if index not in indices:
    #             missing_indices.append(index)
        
    #     #For each missing index and wild pair, create a dictionary of with the attributes of the card it is replacing
        
    #     #For wilds inbetween other cards
    #     assigned_wilds = []
        
    #     for wild, missing_index in zip(wilds, missing_indices):
    #         self.wild_assignments[wild] = {
    #             'score' : rank_score[index_rank[missing_index]],
    #             "rank_index": missing_index,
    #             "rank": index_rank[missing_index],
    #             "suit": sorted_non_wilds[0].suit}
    #         assigned_wilds.append(wild)
        
    #     for wild in assigned_wilds:
    #         wilds.remove(wild)
        
        
    #     #For wilds at the end or beginning of a list. Defualts to start of list.
    #     if len(wilds) > 0:
    #         for i, wild in enumerate(wilds):
    #             self.wild_assignments[wild] = {
    #                 'score' : rank_score[index_rank[min(indices) - (len(wilds) - i)]],
    #                 'rank_index': min(indices) - (len(wilds) - i),
    #                 'rank': index_rank[min(indices) - (len(wilds) - i)],
    #                 'suit': sorted_non_wilds[0].suit}
    
    
    # def _wild_assignment_set(self, ruleset):
    #     #Creates 2 lists, wild cards and non wilds

    #     wilds , non_wilds =  self._split_meld(ruleset)
        
    #     #Creates a list of all the suits that are representetd in the non_wilds
    #     non_wild_suits = []
        
    #     for card in non_wilds:
    #         non_wild_suits.append(card.suit)
        
        
    #     #Creates a list of the missing suits
    #     missing_suits = []
        
    #     for suit in Suit:
    #         if suit not in non_wild_suits:
    #             missing_suits.append(suit)
        
    #     #Matches wild card with one of the missing suits
    #     for i, wild in enumerate(wilds):
    #         self.wild_assignments[wild] = {
    #             'score' : non_wilds[0].return_value(),
    #             'rank_index' : non_wilds[0].return_rank_index(),
    #             'rank' : index_rank[non_wilds[0].return_rank_index()],
    #             'suit' : missing_suits[i]}
            
    
    
    # def return_card_value(self, card, ruleset):
    #     if ruleset.is_wild(card):
    #         return self.wild_assignments[card]['score']
        
    #     if card.rank == "Ace":
    #         if self.meld_type == "set":
    #             if ruleset.ace_both or ruleset.ace_high:
    #                 return ruleset.ace_high_score
    #             else:
    #                 return 1
        
    #         if self.meld_type == "run":
    #             if self._is_ace_high_in_run(card):
    #                 return ruleset.ace_high_score
    #             else:
    #                 return 1
        
    #     return card.return_value(ruleset)
    
    # def _is_ace_high_in_run(self, ace_card, ruleset):
    #     other_cards = [card for card in self.cards 
    #                    if card.rank != "Ace" and not ruleset.is_wild(card)]
        
    #     has_king = any(card.rank == "King" for card in other_cards)
        
    #     for wild in self.wild_assignments:
    #         if self.wild_assignments[wild]['rank'] == "King":
    #             has_king = True
    #             break
    #     return has_king
    
    
    def return_meld_value(self, ruleset):
        score = 0
        
        for card in self.cards:
           score += self.return_card_value(card, ruleset)
          
        return score
    def add_card(self, card):
        self.cards.append(card)
    
    def wild_card_comparison(self, card, wild, ruleset):
        if ruleset.allow_wild_replacement:
            wild_assignment = self.wild_assignments[wild]
            
            return card.rank == wild_assignment['rank'] and card.suit  == wild_assignment['suit']
        else:
            return False
    
    def replace_wild(self,  card, wild):
        self.cards.remove(wild)
        self.cards.append(card)
        
        if wild in self.wild_assignments:
            del self.wild_assignments[wild]
        
        return wild