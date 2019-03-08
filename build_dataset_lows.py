def build_dataset(d_name,d_hands,d_tables,d_desc,d_hero):
    import sqlite3
    from sqlite3 import Error
    import pydealer
    from build_hand import list_from_stack, build_match_low, find_low, pick_five, get_low_all_from_string, get_low_first_from_string, get_low_tot_from_string, low_ranks
    


    def create_tables(c,conn):
        sql_create_dataset = """CREATE TABLE dataset_""" + d_name + """ (
            table_no INTEGER PRIMARY KEY,
            flop TEXT,
            turn TEXT,
            river TEXT,
            hand_1 TEXT,
            hand_2 TEXT,
            hand_3 TEXT,
            hand_4 TEXT,
            hand_5 TEXT,
            hand_6 TEXT,
            hand_7 TEXT,
            hand_8 TEXT,
            hand_9 TEXT,
            hand_10 TEXT,
            low_board INTEGER,
            low_hands TEXT,
            nut_check INTEGER,
            the_rabbit TEXT
            );"""
        c.execute(sql_create_dataset) 


    def get_low_winners(h_list):
        low_winners = ''
        tot_lows = len(h_list)
        no_winners = 0
        if tot_lows <= 1:
#            low_winners = str(h_list[0][6]) + ':' + str(h_list[0][5][0]) + str(h_list[0][5][1]) + '.'    <= old string method
            low_winners = str(h_list[0][6]) + '.' + str(h_list[0][5][0]) + str(h_list[0][5][1])  + '-'
            no_winners = 1
        else:
            check_list = []
            compare_list = []
            compare_list = (h_list[0][0:5])
            for low_loop in h_list:
                check_list = low_loop[0:5]
                if check_list == compare_list:
                    low_winners = low_winners + str(low_loop[6]) + '.' + str(low_loop[5][0]) + str(low_loop[5][1]) + '-'
                    no_winners += 1
        low_winners = str(no_winners) + ':' + low_winners # adding the number of winners, still need to strip the trailing '-'
#        print('Before: '+low_winners)
        low_winners = low_winners[0:len(low_winners)-1]
#        print('After: '+low_winners)
       
    #    print ('low winners: ' + low_winners)
        return low_winners
        
    def nut_cracker(h_string,b_list):
        nut_answer = False
        nut_free = []
        wheel = [1,2,3,4,5]
        low_one = int(h_string[0])
        low_two = int(h_string[1])
        for nut_loop in range(1,6):
            if nut_loop not in b_list:
                nut_free.append(nut_loop)
        if len(nut_free) >= 2:
            if low_one == nut_free[0] and low_two == nut_free[1]: nut_answer = True
        elif len(nut_free) == 1:
            if low_one in nut_free or low_two in nut_free:
                if low_one in wheel and low_two in wheel: nut_answer = True
        elif len(nut_free) == 0:
            if low_one in wheel and low_two in wheel: nut_answer = True
        else: 
            nut_answer = False
            print('We have a nut problem')
        return(nut_answer)


    def add_to_dict(two_card_dict,two_cards,victory):
        if two_cards in two_card_dict:
            two_card_dict[two_cards] = two_card_dict[two_cards] + victory
#            print('Found ' + two_cards)
        else: 
#            print('Did not find ' + two_cards)
            two_card_dict[two_cards] = victory



    def add_to_low_dict(low_x,num_low_hands):
        victory = 0
        victory = 1/num_low_hands
#        print('In Dict function')
#        print(low_x, num_low_hands)
        low_list = get_low_all_from_string(low_x)
#        print(low_list)
        for this_low in low_list:
            add_to_dict(two_card_dict,this_low,victory)
            
    
          
    conn = sqlite3.connect('E:/Dropbox/Code/python/poker/omaha_eight.db')
    c = conn.cursor()
    create_tables(c,conn)

    new_deck = pydealer.Deck()
    new_deck.shuffle()
    hand_list = []
    new_card = pydealer.Stack()
    hero_hand = pydealer.Stack()
    hand = pydealer.Stack()
    flop = pydealer.Stack()
    turn = pydealer.Stack()
    river = pydealer.Stack()
    board = pydealer.Stack()
    rabbit_card = pydealer.Stack()
    d_tables_act = int(d_tables)      # used for passing to DB
    d_tables_int = int(d_tables) + 1   # used for For loop
    table_no = d_tables_int
    db_name = 'dataset_' + d_name
    low_count = 0
    nut_count = 0
    non_nut_count = 0
    shared_low = 0
    shared_nut = 0
    non_nut_shared = 0
    count_low = 0
    no_lows = 0


# This section is for Hero stacks only    
    hero_terms = []
    d_hero_indicator = False
    d_card = ''
    if d_hero != '':
        d_hero_indicator = True
        hero_length = len(d_hero)
        for hero_loop in range(0,hero_length):
            d_card = d_hero[hero_loop]
            if d_card == '1': d_card = "A"
            d_card += "D"
            hero_terms.append(d_card)
        left_over = 4 - hero_length  # need to have four cards to a hand, how many not in the hero list?
        if left_over > 0:
            hero_terms.append("9S")
            if left_over > 1:
                hero_terms.append("9C")
                if left_over >2:
                    hero_terms.append("9H")
    print('Hero Terms: ')
    print(hero_terms)
    

    d_hands_actual = int(d_hands) # used for passing info to DB
    d_hands_int = int(d_hands) + 1 # used for For X loop    

    two_card_dict = {}
    low_keys = ('12','13','14','15','16','17','18','23','24','25','26','27','28','34','35','36','37','38','45','46','47','48','56','57','58','67','68','78')
    for key_inc in low_keys:
        two_card_dict[key_inc] = 0
 #   print(two_card_dict)


    
    for table_total in range(1,table_no):
        print(table_total)
        new_deck = pydealer.Deck()
        new_deck.shuffle()
        hero_hand.empty()
        if d_hero_indicator:
            for each_hero_card in hero_terms:
                
                new_card = new_deck.get(each_hero_card)
                hero_hand.add(new_card)
#            print('Hero Hand')
#            print(hero_hand)

        flop = new_deck.deal(3)
        flop_text = ''
        for y in range(3):
            flop_text = flop_text + (flop[y].value[0] + flop[y].suit[0])
        turn = new_deck.deal(1)
        turn_text = (turn[0].value[0] + turn[0].suit[0])
        river = new_deck.deal(1)
        river_text =(river[0].value[0] + river[0].suit[0])
        flop_text = flop_text.replace("1","T")
        turn_text = turn_text.replace("1","T")
        river_text = river_text.replace("1","T")
        

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
        

        hand_cards = ''
        low_hand = []  # this will be the four cards from the players hand sorted by low
        hand_list = []
        

        for x in range(1,d_hands_int):
            board_final_low = []
            hand_final_low = []
            hand_cards = ''
            
            
            if x == 1 and d_hero_indicator:
                hand = hero_hand
            else:
                hand = new_deck.deal(4)
#            print(hand)
            hand.sort(ranks=low_ranks)
            low_hand = list_from_stack(hand)
            low_hand = build_match_low(low_hand)
            low_check = False
            if len(match_low) >= 3 and len(low_hand) >=2:  # asking - are there 3 non-dup low cards on the board and at leaast 2 low cards in the hand?
                hand_final_low = find_low(match_low,low_hand)
                if hand_final_low != []: 
                    hand_final_low.append(x)
                    table_lows.append(hand_final_low)

            
            for y in range(4): hand_cards = hand_cards + (hand[y].value[0] + hand[y].suit[0])
            hand_cards = hand_cards.replace("1","T")
            hand_list.append(hand_cards)
       
        win_check = ''
        num_low_hands = 0
        nut_check = 0   
        if board_low_indicator: 
            if table_lows != []:
                table_lows.sort()
#                print(table_lows)
                low_hands_string = get_low_winners(table_lows)
                low_board = 1
                low_count += 1
 #               print('low hands string!: ' + low_hands_string)
                # print(low_hands_string[2:4])
                num_low_hands = int(get_low_tot_from_string(low_hands_string))
                if num_low_hands > 1: shared_low += 1
                win_check = get_low_first_from_string(low_hands_string)
                if nut_cracker(win_check,match_low): 
                    nut_check = 1
                    nut_count += 1
                    if num_low_hands > 1: shared_nut += 1
            else: low_hands_string = ''
        else: low_board = 0
        
        if num_low_hands >= 1: add_to_low_dict(low_hands_string,num_low_hands)
        
        
        
        rabbit_string = ''
        while len(new_deck) > 0:
            rabbit_card = new_deck.deal(1)
            # print('rabbit_card')
            # print(rabbit_card)
            rabbit_string = rabbit_string + rabbit_card[0].value[0] + rabbit_card[0].suit[0]


        rabbit_string = rabbit_string.replace("1","T")    
        # print(rabbit_string)
        # print(hand_list)
        # print(hand_list[0])  

        # Set for short tables
        if len(hand_list) < 11:
            dummy_no = 11 - len(hand_list)
            for dummy_x in range(1,dummy_no):
                hand_list.append('')
        else:
            print('Too many hands')
            

        
    
        sqlcommand = '''    INSERT INTO ''' + db_name + '''(table_no, 
                            flop,
                            turn, 
                            river,
                            hand_1, 
                            hand_2, 
                            hand_3, 
                            hand_4,
                            hand_5,
                            hand_6,
                            hand_7,
                            hand_8,
                            hand_9,
                            hand_10,
                            low_board,
                            low_hands,
                            nut_check,
                            the_rabbit) 
                            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
                            
        body_row =          (table_total,
                            flop_text,
                            turn_text,
                            river_text,
                            hand_list[0],
                            hand_list[1],
                            hand_list[2],
                            hand_list[3],
                            hand_list[4],
                            hand_list[5],
                            hand_list[6],
                            hand_list[7],
                            hand_list[8],
                            hand_list[9],
                            low_board,
                            low_hands_string,
                            nut_check,
                            rabbit_string)

        c.execute(sqlcommand, body_row)
        
        
    sqlcommand = '''    INSERT INTO datasets (db_name, 
                        screen_name,
                        screen_description,
                        hands,
                        tables) 
                        VALUES(?, ?, ?, ?, ?) '''
                        

    
                        
    dataset_row =          (db_name,
                        d_name,
                        d_desc,
                        d_hands_actual,
                        d_tables_act)

    c.execute(sqlcommand, dataset_row)        

    
    no_lows = d_tables_act - low_count
    non_nut_count = low_count - nut_count   
    non_nut_shared = shared_low - shared_nut
    non_nut_solo = non_nut_count - non_nut_shared
    nut_solo = nut_count - shared_nut     
    sql_low_command = '''   INSERT INTO low_counts(dataset, 
                            lows,
                            no_lows, 
                            shared_lows,
                            non_nut_lows, 
                            nut_lows, 
                            non_nut_solo_lows, 
                            non_nut_shared_lows,
                            nut_solo_lows,
                            nut_shared_lows) 
                            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
                            
    body_low_row =          (db_name,
                                low_count,
                                no_lows,
                                shared_low,
                                non_nut_count,
                                nut_count,
                                non_nut_solo,
                                non_nut_shared,
                                nut_solo,
                                shared_nut)
    c.execute(sql_low_command, body_low_row)
    
    
    
#    print(two_card_dict)



    sql_two_command = '''INSERT INTO two_card_lows(dataset, 
                                                    k12,
                                                    k13,
                                                    k14,
                                                    k15,
                                                    k16,
                                                    k17,
                                                    k18,
                                                    k23,
                                                    k24,
                                                    k25,
                                                    k26,
                                                    k27,
                                                    k28,
                                                    k34,
                                                    k35,
                                                    k36,
                                                    k37,
                                                    k38,
                                                    k45,
                                                    k46,
                                                    k47,
                                                    k48,
                                                    k56,
                                                    k57,
                                                    k58,
                                                    k67,
                                                    k68,
                                                    k78)
                        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
                        
    body_two_row =  (db_name,
            two_card_dict['12'],
            two_card_dict['13'],
            two_card_dict['14'],
            two_card_dict['15'],
            two_card_dict['16'],
            two_card_dict['17'],
            two_card_dict['18'],
            two_card_dict['23'],
            two_card_dict['24'],
            two_card_dict['25'],
            two_card_dict['26'],
            two_card_dict['27'],
            two_card_dict['28'],
            two_card_dict['34'],
            two_card_dict['35'],
            two_card_dict['36'],
            two_card_dict['37'],
            two_card_dict['38'],
            two_card_dict['45'],
            two_card_dict['46'],
            two_card_dict['47'],
            two_card_dict['48'],
            two_card_dict['56'],
            two_card_dict['57'],
            two_card_dict['58'],
            two_card_dict['67'],
            two_card_dict['68'],
            two_card_dict['78'])

    c.execute(sql_two_command, body_two_row)    
    
    
    
   
    
    
    conn.commit()  
    conn.close()
    
