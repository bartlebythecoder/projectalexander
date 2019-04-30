# -*- coding: utf-8 -*-
"""
Created on Sun Mar 17 17:26:49 2019

@author: sean
"""

from build_hand import list_from_stack, build_match_low
import pydealer




new_deck = pydealer.Deck()
new_deck.shuffle()
flop_find = ["AS","AD","AC"]
turn_find = ["6S"]
river_find = ["4D"]
flop = new_deck.get_list(flop_find)

turn = new_deck.get_list(turn_find)
river = new_deck.get_list(river_find)

#        print(board_text)
#        print(poker_high(board_text))

board_low_indicator = False # Will be turned TRUE if three non-dup cards come on the board  
board_full_list = []  # will be the integer values of all cards on the board
match_low = [] # will be a subset of board_full_list, non-dup list of integers 8 or lower
nut_low = []  # Will be the cards that make a nut low hand for this table
table_lows = []  # Will be a list of all lows at the table
low_hands_string  = ''

board = flop
board += turn
board += river
board_full_list = list_from_stack(board)
match_low = build_match_low(board_full_list) 
if len(match_low) >= 3: board_low_indicator = True
else: 
    match_low = []
    board_low_indicator = False
    
print(flop)
flop.sort()
print('sorted')
print(flop)
print(turn)
print(river)
print('-----------------------------')
print(board)
print(board_full_list)
print(match_low)
print(board_low_indicator)
        