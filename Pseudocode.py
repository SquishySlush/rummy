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
    
    wilds <-- empty list
    non_wilds <-- empty list
    
    FOR card IN cards
        IF ruleset.is_wild(card) THEN
            ADD card TO wilds
        ELSE
            ADD card TO non_wilds
    
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
    
    
    
FUNCTION wild_assignment_set(ruleset, cards)

    wilds, non_wilds
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    