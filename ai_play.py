def ai_play_dataset_script(look_at_dataname):

    import sqlite3
    from build_hand import string_to_low, find_low

            
    def get_board(table_index):
        board = []
        board.append(allrows[table_index][1][0:2])
        board.append(allrows[table_index][1][2:4])
        board.append(allrows[table_index][1][4:6])
        board.append(allrows[table_index][2][0:2])
        board.append(allrows[table_index][3][0:2])
        return(board)
        
    def get_hands(table_index, hand_no):
        hand = []
        hand_index = hand_no + 4
        hand.append(allrows[table_index][hand_index][0:2])
        hand.append(allrows[table_index][hand_index][2:4])
        hand.append(allrows[table_index][hand_index][4:6])
        hand.append(allrows[table_index][hand_index][6:8])
        return(hand)    
        
    def pick_two(b_list,h_list):
        pick_two_list = []
        for each_c in h_list:
            if each_c not in b_list: pick_two_list.append(each_c)
            if len(pick_two_list) > 2: pick_two_list = pick_two_list[0:2]    
        return(pick_two_list)

        
    conn = sqlite3.connect('E:/Dropbox/Code/python/poker/omaha_eight.db')
    c = conn.cursor()

    sql3_select = """ SELECT    table_no,
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
                                nut_check
                        FROM """ + look_at_dataname

                            
    c.execute(sql3_select)
    allrows = []

    allrows = c.fetchall()    


    table_no = 1
    table_index = table_no - 1 
    max_tables = len(allrows) 

    hero_roll = 0
    villain_roll = 0
    pot = 0

    gap_dict = {}  # for AI purposes

    low_result = 'chop'

    
    while table_no <= max_tables:


        table_index = table_no - 1
        low_board = allrows[table_index][14]
        while low_board != 1 and table_no <= max_tables:
            print(str(table_no))
            table_no += 1
            if table_no < max_tables:
                table_index = table_no - 1
                low_board = allrows[table_index][14]
            

        if low_board == 1:        
            board = get_board(table_index)
            board_low_list = string_to_low(board)
            low_board = allrows[table_index][14]
                    
            villain_hand = get_hands(table_index,0)
            villain_low_list = string_to_low(villain_hand)
            villain_low_hand = find_low(board_low_list,villain_low_list)
            
            hero_hand = get_hands(table_index,1)
            hero_low_list = string_to_low(hero_hand)
            hero_low_hand = find_low(board_low_list,hero_low_list)
            hero_two = pick_two(board_low_list,hero_low_list)
            if len(hero_two) == 2:
                hero_two_sum = 15 - (hero_two[0]+hero_two[1])  # For AI purposes
            else: hero_two_sum = 0
            print(hero_two,hero_two_sum)
            if hero_two_sum not in gap_dict:
                gap_dict[hero_two_sum] = [0,1]
            else: gap_dict[hero_two_sum][1] += 1
                
            
            result = 0   
    #            print(hero_low_hand[0:5])
    #            print(villain_low_hand[0:5])
            if hero_low_hand != [] and villain_low_hand != []:
                result = 1
                if hero_low_hand[0:5] == villain_low_hand[0:5]:
                    low_result = 'chop'
                    gap_dict[hero_two_sum][0] += 0.5
                elif hero_low_hand[0:5] < villain_low_hand[0:5]:  
                    low_result = 'hero'
                    gap_dict[hero_two_sum][0] += 1
                else: low_result = 'villain'
            elif hero_low_hand == [] and villain_low_hand != []:
                low_result = 'villain'
                result = 2
            elif hero_low_hand != [] and villain_low_hand == []:
                low_result = 'hero'
                gap_dict[hero_two_sum][0] += 1
                result = 3
            elif hero_low_hand == [] and villain_low_hand == []:
                low_result = 'chop'
                gap_dict[hero_two_sum][0] += 0.5
                result = 4
            else: 
                low_result = 'problem'
                result = 5
            print(str(table_no) + ': ' + low_result)    
    
            table_no += 1    
            pot = 0
            pot += 100
            villain_roll -= 100
    
    
            hero_roll -= 100
            pot += 100
    
            if low_result == 'chop':
    
                villain_roll += pot/2
                hero_roll += pot/2
                
            elif low_result == 'villain':
    
                villain_roll += pot
                
            elif low_result == 'hero':
    
                hero_roll += pot
               
            else:
                print('Problem')
                           
            print("Total won: " + str(hero_roll) + " / " + str(villain_roll))
            pot = 0 
            


    sql_create_dataset = """CREATE TABLE low_gaps_""" + look_at_dataname + """ (
        gap_sum INTEGER PRIMARY KEY,
        gap_win_pct REAL
        );"""
    c.execute('DROP TABLE IF EXISTS low_gaps_' + look_at_dataname)
    c.execute(sql_create_dataset) 


    
    for aigap,aisum in gap_dict.items():
    
        win_pct = aisum[0]/aisum[1]

        
        sql_low_gaps = """  INSERT INTO low_gaps_""" + look_at_dataname + """(gap_sum, 
                            gap_win_pct) 
                            VALUES(?, ?) """
                            
        gap_row =          (aigap,
                            win_pct                                )
        c.execute(sql_low_gaps, gap_row)
        
        
        
        
    print(gap_dict)
    conn.commit()  
    conn.close()
