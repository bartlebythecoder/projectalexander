def get_low_tot_from_string(low_string):
    sub_string = low_string.split(':')
    return sub_string[0]


def get_low_first_from_string(low_string):
    a_sub_string = low_string.split(':')
    b_sub_string = a_sub_string[1].split('-')
    c_sub_string = b_sub_string[0].split('.')
    return c_sub_string[1]
    
def get_low_all_from_string(low_string):
    #Gets the string of winning seats and two cards and send back the list of two cards
    a_sub_string = low_string.split(':')
    b_sub_string = a_sub_string[1].split('-')
    all_lows = []
    for each_low in b_sub_string:
        c_substring = each_low.split('.')
        all_lows.append(c_substring[1])
    return all_lows  
    
def get_low_winners_from_string(low_string):
    a_sub_string = low_string.split(':')
    b_sub_string = a_sub_string[1].split('-')
    all_lows = []
    for each_low in b_sub_string:
        c_substring = each_low.split('.')
        all_lows.append(c_substring[0])
    return all_lows      


def pick_five(num1,num2,list_board):
    temp_list_b = []
    temp_list_h = []
    temp_orig_h = []
    temp_list_b = list(set(list_board))
    temp_list_b.sort()
    temp_list_h = [num1,num2]
    temp_orig_h = [num1,num2]
    cards_total = 0
    for card in temp_list_b:
        if card not in temp_list_h and cards_total <= 5:
            temp_list_h.append(card)
            cards_total += 1
    if len(temp_list_h) < 5:
        final_five = []
    else: 
        final_five = temp_list_h[0:5]
        final_five.sort(reverse = True)
        final_five.append(temp_orig_h)
    # print('In pick_five def returning: ')
    # print(num1)
    # print(num2)
    # print(list_board)
    # print(final_five)
    return final_five
    
    
def find_low(board, hand):
    board = list(set(board))
    hand = list(set(hand))
    lowest_combo = []
    low_board = []
    for each_card in board: 
        if each_card <= 8: low_board.append(each_card)
    low_hand = []
    for each_card in hand:
        if each_card <= 8: low_hand.append(each_card)
    low_board.sort()
    low_hand.sort()
    
    final_five_list = []
    final_five_candidate = []
    if len(low_hand) < 2 or len(low_board) < 3:
#        print('Not enough low cards to make a five card low).')
        pass
    else:
        hand_index = []
        if len(low_hand) == 2: hand_index = [(0,1),]
        elif len(low_hand) == 3:  hand_index = [(0,1),(0,2),(1,2)]
        elif len(low_hand) == 4: hand_index = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)] 
        else: print('Problem with number of cards in hand ')
        for each_pair in hand_index:

            final_five_candidate = pick_five(low_hand[each_pair[0]],low_hand[each_pair[1]],low_board)
            if final_five_candidate != []:
                # print('A final five returned from pick_five: ')
                # print(final_five_candidate)
                final_five_list.append(final_five_candidate) 
#            else: print('Too many dups to make a low.')
 
        
        if len(final_five_list) > 0:
            final_five_list.sort()
            # print('The Final List for this player:')
            # print(final_five_list)
            lowest_combo = (final_five_list[0])
        else: 
            lowest_combo = []
#            print('Not enough low cards in any combination')
    return lowest_combo
        
    
def build_match_low(card_list):
    new_card_list = []
    card_list = list(set(card_list))
    card_list.sort()
    for a in card_list:
        if a <= 8:
            new_card_list.append(a)
    return new_card_list

def list_from_stack(hand):
    stack_list = [] 
    stach_card_value = ''
    stack_card_int = 0
    for x in hand:
        stack_card_value = x.value
        stack_card_int = low_ranks["values"][x.value]
        # print('New card from stack ' + stack_card_value + ": " + str(stack_card_int))
        stack_list.append(stack_card_int)
    return stack_list     

def string_to_low(string_hand):
   # Given a string of card values (no suits), convert to a list of low non-dup numbers 
    cards_in_string = len(string_hand)
    low_list = []
    for each_card in range(0,cards_in_string):
        low_value = low_ranks["values"][string_hand[each_card][0]]
 #       print(low_value)
        if low_value <= 8: 
            low_list.append(low_value)
    low_list = list(set(low_list))
    low_list.sort()
#    print(low_list)
    return low_list

def db_hand_to_low(db_string):
    # Given a hand using the DB string format (values and suits), convert to a list of low non-dup numbers
    low_response = []
    no_suit_string = ''
    for each_card in range(0,8,2):
        no_suit_string = no_suit_string + db_string[each_card]
    low_response = string_to_low(no_suit_string)
    return low_response
        

low_ranks = {
    "values":       {
        "A" :       1,
        "T" :       10,
        "J" :       11,
        "Q" :       12,
        "K" :       13,
        "King":     13,
        "Queen":    12,
        "Jack":     11,
        "Ten":      10,
        "Nine":     9,
        "Eight":    8,
        "Seven":    7,
        "Six":      6,
        "Five":     5,
        "Four":     4,
        "Three":    3,
        "Two":      2,
        "Ace":      1,
        "10":       10,
        "9":        9,
        "8":        8,
        "7":        7,
        "6":        6,
        "5":        5,
        "4":        4,
        "3":        3,
        "2":        2
    }
}                