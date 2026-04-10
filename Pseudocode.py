# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 16:31:01 2026

@author: Faisal Mustafa
"""

FUNCTION quicksort(items)
    IF LENGTH(items) <= 1 THEN
        RETURN items
    
    pivot <-- POP(items)
    items_greater <-- []
    items_lesser <-- []
    
    FOR item IN ITEMS
        IF item > pivot THEN
            items_greater.APPEND(item)
        ELSE
            items_lesser.APPEND(item)
    
    RETURN quicksort(items_lesser) + pivot + quicksort(items_greater)
    

FUNCTION validate_set(cards, ruleset)
    
    IF ruleset.max_meld_size_set IS NOT NONE 
    AND LENGTH(meld) > ruleset.max_meld_size_set THEN
        RETURN FALSE, "Meld Too Large"
    IF LENTH(cards) < ruleset.min_meld_size THEN
        RETURN FALSE, "Meld Too Small"
    
    
    suits <-- empty list
    ranks <-- empty list
    
    FOR card IN cards
        IF NOT ruleset.is_wild(card) THEN
            ADD card.rank TO ranks
            ADD card.suit TO suits
    
    IF NOT ruleset.allow_wild_only_melds AND LENGTH(ranks) == 0 THEN
        RETURN FALSE, "Meld Contains Only Wild Cards"
    
    IF LENGTH(SET(ranks)) != 1 THEN
        RETURN FALSE, "Different Ranks In Set"
    
    IF LENGTH(SET(suits)) != LENGTH(suits) THEN
        RETURN FALSE, "Multiple of the Same Suits in 1 Set"

    RETURN TRUE, cards



FUNCTION validate_run(cards, ruleset)
    
    IF ruleset.max_meld_size_run IS NOT NONE 
    AND LENGTH(meld) > ruleset.max_meld_size_run THEN
    
        RETURN FALSE, "Meld Too Large"
        
    IF LENTH(cards) < ruleset.min_meld_size THEN
    
        RETURN FALSE, "Meld Too Small"
    
    wilds, non_wilds <-- split_wilds(cards)
    
    IF NOT ruleset.allow_wild_only_melds AND LENGTH(ranks) == 0 THEN
        RETURN FALSE, "Meld Contains Only Wild Cards"
    
    suits <-- empty list
    indices <-- empty list
    
    FOR card IN non_wilds
        ADD card.suit TO suits
        ADD card.return_rank_index() TO indices
    
    indices <-- quicksort(indices)
    
    IF LENGTH(SET(suits)) != 1 THEN
        RETURN FALSE, "Multiples Suits in 1 Run"
    
    IF LENGTH(SET(indices)) != LENGTH(indices) THEN
        RETURN FALSE, "Multiples of the Same Ranks"
    
    IF ruleset.ace_low OR ruleset.ace_both THEN
    
        min_index <-- MINIMUM(indices)
        max_index <-- MAXIMUM(indices)
        span <-- max_index - min_index + 1
        gaps <-- span - LENGTH(non_wilds)
    
        IF gaps <= LENGTH(wilds) THEN
            RETURN TRUE
    
        has_ace <-- FALSE
        has_king <-- FALSE
    
    FOR index IN indices
        IF index == 0 THEN
            has_ace <-- TRUE, cards
        ELSE IF index == 12 THEN
            has_king == TRUE
            
            
    IF ruleset.ace_high OR ruleset.ace_both THEN
            
        adjusted_indices = []
        FOR index IN indices
            IF index == 0 THEN
                ADD 13 TO adjusted_indices
            ELSE
                ADD index TO adjusted_indices
            
        adjusted_indices = quicksort(adjusted_indices)
            
        min_index <-- MINIMUM(adjusted_indices)
        max_index <-- MAXIMUM(adjusted_indices)
        span <-- max_index - min_index + 1
        gaps <-- span - LENGTH(non_wilds)
            
        IF gaps <= LENGTH(wilds) THEN
            RETURN TRUE, cards
            
        IF ruleset.ace_wrap_around AND has_king THEN
           low_indices <-- empty list    
           high_indices <-- empty list
            
           FOR index IN indices
               IF index < 5 THEN
                   ADD index TO low_indices
               ELSE IF index >= 10 THEN
                   ADD index TO high_indices
                
               IF LENGTH(low_indices) > 0 AND LENGTH(high_indices) >0 THEN
                   low_span <-- MAX(low_indices) - MIN(low_indices)
                   high_span <-- MAX(high_indices) - MIN(high_indices)
                    
                   total_gaps <-- (low_span - LENGTH(low_indices))
                   + (high_span - LENGTH(high_indices))
                   
                   IF total_gaps <= LENGTH(wilds) THEN
                       RETURN TRUE, cards

    RETURN FALSE, "Invalid Run"




#Assume function create_card, with inputs rank, suit, and ruleset

FUNCTION create_deck(ruleset)
    
    cards <-- empty list
    
    FOR deck <-- 1 IN RANGE(ruleset.num_decks)
        FOR rank IN rank_index
            IF rank NOT IN ruleset.wilds THEN
                FOR suit IN Suit
                    card <-- create_card(rank, suit, ruleset)
                    ADD card TO cards
    
    FOR wild, num_wild IN ruleset.wilds
        FOR i <-- 1 IN RANGE(num_wild)
            card <-- create_card(wild, NONE, ruleset)
            ADD card TO cards

FUNCTION shuffle(cards)

    FOR i FROM last index OF card DOWN TO 1
        roll = random integer between 0 and i (inclusive)
        SWAP cards[i] WITH cards[roll]

FUNCTION sort_suit(cards)
    
    hearts_cards <-- empty list
    clubs_cards <-- empty list
    diamonds_cards <-- empty list
    spades_cards <-- empty list
    
    FOR card IN cards
        IF card.suit IS hearts THEN
            ADD card TO hearts_cards
        ELSE IF card.suit IS clubs THEN
            ADD card TO clubs_cards
        ELSE IF card.suit IS diamonds THEN
            ADD card TO diamonds_cards
        ELSE IF card,suit IS spades THEN
            ADD card TO spades_cards
    
    RETURN sort_rank(hearts_cards) + sort_rank(clubs_cards)
    + sort_rank(diamonds_cards) + sort_rank(spades_cards)
    
    
    
FUNCTION split_wilds(cards, ruleset)

    wilds <-- empty list
    non_wilds <-- empty list
    
    FOR card IN cardds
    
    IF ruleset.is_wild(card) THEN
        ADD card TO wilds
    ELSE
        ADD card TO non_wilds
    
    RETURN wilds, non_wilds
    
    


    FUNCTION wild_assignment_set(cards, ruleset)

    wilds, non_wilds <-- split_wilds(cards, ruleset)
    
    non_wild_suits <-- empty list
    
    FOR card IN non_wilds
        ADD card.suit TO non_wild_suits
    
    missing_suits <-- empty list
    
    FOR suit IN Suit
        IF suit NOT IN non_wild_suits THEN
            ADD suit TO missing_suits
    
    
    FOR i <-- 1 TO LENGTH(wilds)
        wild_assignments[wild] <-- {
            SCORE : non_wilds[0].return_value(),
            RANK_INDEX : non_wilds[0].return_rank_index(),
            RANK : non_wilds[0].rank,
            SUIT : missing_suits[i]
            }
    
FUNCTION wild_assignment_run(cards, ruleset)

    wilds, non_wilds <-- split_wilds(cards, ruleset)
    
    indices <-- empty list
    
    FOR card IN non_wilds
        ADD card.return_rank_index() TO indices
        
    indices <-- quicksort(indices)
    
    range_indeces <-- FIRST(indices) TO LAST(indices)
    
    missing_indices <-- empty list
    
    FOR index IN range_indices
        IF index NOT IN indices THEN
            ADD index TO missing_indices
    
    assigned_wilds <-- empty list
    
    FOR wild, missing_index IN ZIP(wilds, missing_indices)
        wild_assignments[wild] <-- {
            SCORE : score of missing_index rank,
            RANK_INDEX : missing_index,
            RANK : rank of missing_index,
            SUIT : suit used in the run}
        ADD wild TO assigned_wilds
    
    FOR wild IN assigned_wilds
        REMOVE wild FROM wilds
    
    IF LENGTH(wilds) > 0 THEN
        FOR i <-- 0 TO LENGTH(wilds) - 1
            offset <-- MIN(indices) - (LENTH(wilds) - i)
            wild_assignments[wilds[i] <-- {
                SCORE : Score of Rank at the offset,
                RANK_INDEX : offset,
                RANK : Rank of offset index,
                SUIT : suit used in the run}
        


FUNCTION validate_play_melds(melds, has_melded, ruleset, required_score)
    
    IF LENGTH(melds) == 0:
        RETURN FALSE, "No Melds"
    
    IF NOT has_melded THEN
        total_score <-- 0
        
        FOR meld IN melds
            total_score <-- total_score + meld.return_meld_value(ruleset)
        IF total_score < required-score THEN
            RETURN FALSE, "Minimum Score Not Met"
    
    RETURN TRUE, NONE


FUNCTION validate_lay_off(card, meld, ruleset, has_melded)
    test_cards <-- meld.cards + [card]
    
    valid, error = validate_meld(test_cards, ruleset)
    
    IF ruleset.require_melding_to_lay_off AND NOT has_melded THEN
        RETURN FALSE, "You Require To Have Melded To Lay Off"
    
    IF valid THEN
        meld.add_card(card)
        RETURN TRUE, NONE
    RETURN FALSE, "Card Doesn't Fit in Meld"
    

FUNCTION validate_discard(card, cards, has_drawn, drawn_from_discard, ruleset):
    IF card NOT IN cards THEN
        RETURN FALSE, "Card Not in Hand"
    
    IF NOT has_drawn THEN
        RETURN FALSE, "Must First Draw a Card"
    
    IF ruleset.prevent_discard_same_card AND drawn_from_discard == card THEN
        RETURN FALSE, "Cannot Discard Card Immedietly Drawn From Discard Pile"
    
    RETURN TRUE, NONE



FUNCTION validate_draw(deck, has_drawn)
    IF deck.is_empty() THEN
        RETURN FALSE, "Deck is Empty"
    IF has_drawn THEN
        RETURN FALSE, "Player has Drawn"
    
    RETURN TRUE, NONE

FUNCTION validate_draw_discard(card, discard_pile, has_drawn, has_melded, ruleset)
    IF discard_pile.empty THEN
        RETURN FALSE, "Discard Pile is Empty"
    IF has_drawn THEN
        RETURN FALSE, "Player Has Drawn Card"
    IF card NOT IN discard_pile THEN
        RETURN FALSE, "Card isn't in Discard Pile"
    
    IF ruleset.require_melding_to_draw_from_disc AND NOT has_melded THEN
        RETURN FALSE, "Melding Required to Draw from Discard Pile"
    
    RETURN TRUE, NONE

FUNCTION ruleset_validation(
    config,
    key,
    default,
    expected_value,
    allowed_values,
    min_value,
    max_value)

    value <-- config[key] IF key EXISTS, ELSE default
    
    IF value IS NOT NONE AND value IS NOT OF expected_tupe THEN
        RETURN default
    
    IF allowed_values IS NOT NONE AND value NOT IN allowed_values THEN
        RETURN default
    
    IF min_value IS NOT NONE AND value < min_value THEN
        RETURN default
        
    IF max_value IS NOT NONE AND value > max_value THEN
        RETURN default
    
    RETURN value






















































