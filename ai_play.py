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

        
    def get_low_coord(table):
        
        low_coord_dict = {
        '1'   : [425,255],
        '2'   : [925,255],
        '3'   : [425,380],
        '4'   : [925,380],
        '5'   : [425,505],
        '6'   : [925,505],
        '7'   : [425,630],
        '8'   : [925,630],
        '9'   : [425,755],
        '10'  : [925,755]}
        
        table_place = []
        table_place = low_coord_dict[table]
        return(table_place)

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

       
    low_games_list = []
    hero_roll = 1000
    villain_roll = 1000
    pot = 50


    see_results = False
    low_result = 'chop'

    
    while table_no <= max_tables:

        table_index = table_no - 1
        low_board = allrows[table_index][14]
        while low_board != 1:
            table_no += 1
            table_index = table_no - 1
            low_board = allrows[table_index][14]  
       
        
        board = get_board(table_index)
        board_low_list = string_to_low(board)
        low_board = allrows[table_index][14]
                
        villain_hand = get_hands(table_index,0)
        villain_low_list = string_to_low(villain_hand)
        villain_low_hand = find_low(board_low_list,villain_low_list)
        
        
        
        hero_hand = get_hands(table_index,1)
        hero_low_list = string_to_low(hero_hand)
        hero_low_hand = find_low(board_low_list,hero_low_list)
        


        result = 0   
#            print(hero_low_hand[0:5])
#            print(villain_low_hand[0:5])
        if hero_low_hand != [] and villain_low_hand != []:
            result = 1
            if hero_low_hand[0:5] == villain_low_hand[0:5]:
                low_result = 'chop'
            elif hero_low_hand[0:5] < villain_low_hand[0:5]:  
                low_result = 'hero'
            else: low_result = 'villain'
        elif hero_low_hand == [] and villain_low_hand != []:
            low_result = 'villain'
            result = 2
        elif hero_low_hand != [] and villain_low_hand == []:
            low_result = 'hero'
            result = 3
        elif hero_low_hand == [] and villain_low_hand == []:
            low_result = 'chop'
            result = 4
        else: 
            low_result = 'no lows'
            result = 5
        print(str(table_no) + ': ' + low_result)    

        table_no += 1    
        pot = 50
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
                       
        print("Total" + str(hero_roll))
        pot = 0 


