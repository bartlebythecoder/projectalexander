def hero_hand_run(hand,dataset):
    import sqlite3
    from build_hand import list_from_stack, build_match_low, find_low, pick_five, low_ranks, db_hand_to_low

    print(hand,dataset)
    
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
                                nut_check,
                                the_rabbit
                        FROM """ + dataset

                            
    c.execute(sql3_select)
    allrows = []

    allrows = c.fetchall()   
    conn.commit()  
    conn.close()
    hero_list = []
    low_index = 0
    in_rabbit = False
    rabbit_finds = 0
    board_list = []
    low_board_ind = 0
    
    
    
    for x in range(len(hand[0])):
        hero_list.append(int(hand[0][low_index]))    
        low_index += 1

    print(hero_list)

    rabbit_low = []
    villain_list = []
    total_no = 0
    for x in allrows:
        total_no += 1
        
        low_board_ind = x[14]
        
        rabbit_low = []
        rabbit_low = db_hand_to_low(x[17])
        
        
        for z in range(4,14):
            if x[z] != '':
                villain_hand = db_hand_to_low(x[z])
                villain_list.append(villain_hand)
            
#            print("vh: " + villain_hand)
        
#        print(villain_list)
        
        in_rabbit = False
        for y in hero_list:
            if y in rabbit_low: in_rabbit = True
            else: 
                in_rabbit = False
                break
        if in_rabbit == True: 
            print('found one',hero_list,x[17])
            rabbit_finds += 1
            

                
            
            
            
    print("Total rabbit finds = " + str(rabbit_finds) + " out of " + str(total_no))           

