def high_equity_script(dataset):
    
    # take hands from a dataset and build a table with the high equity of each hand
    
    
    import sqlite3
    import pydealer
#    from build_hand import list_from_stack, build_match_low, low_ranks
    from hand_index import hand_info 



   
    
    print('This is what was passed.')
    print(dataset)
    
    conn = sqlite3.connect('E:/Dropbox/Code/python/poker/omaha_eight.db')
    c = conn.cursor()

    sql3_select = """SELECT * FROM """ + dataset
                            
    c.execute(sql3_select)
    allrows = []

    allrows = c.fetchall()
    
    low_dict = {}
    e_table = 0
    
    
    for each_row in allrows:
#        print(each_row)
        e_table += 1
        print('----------------------')
        print(e_table)
        high_class = ''
        winners_string = []
        win_equity = 0.0
                
        winners_string = each_row[18]
        print('Winner String: ' + (winners_string))
        no_winners = len((winners_string))
        print('Number of Winners:' + str(no_winners))
        for winner_no in range(0,no_winners):
            player_no = int(winners_string[winner_no]) + 3
            win_hand = each_row[player_no]
            print('Winning Hand: ' + win_hand)
                        
            deck = pydealer.Deck()
            hand = pydealer.Stack()
            hand = win_hand
            print(hand)
            
#            high_class = hand_info(hand)
#            high_index = high_class.build_index()


        
       
#        seat_no = 0
#        for e_hand in hands:
#            seat_no += 1
#            update_equity_list = [0,0]
#            
#            if len(e_hand) > 1:
#            
#                if seat_no in index_winner_list:
#                    win_equity = round(1/len(index_winner_list),3)
#                    update_equity_list = [1,win_equity] 
#                else: update_equity_list = [1,0]
#                
#                if e_hand not in low_dict: 
#                    low_dict[e_hand] = update_equity_list
#                else:
#                    low_dict[e_hand][0] += update_equity_list[0]
#                    low_dict[e_hand][1] += update_equity_list[1]
    
#        print(hands,index_winner_list)
#        
#    for y in low_dict.values():
#        win_pct = round(y[1]/y[0],3)
#        y.append(win_pct)
#    
#    
##    print(low_dict)
#    
#    sql_create_dataset = """CREATE TABLE low_equity_""" + dataset + """( 
#                                                    low_string_value TEXT PRIMARY KEY,
#                                                    appearances INTEGER,
#                                                    wins REAL,
#                                                    equity);"""
#
#    c.execute("""DROP TABLE IF EXISTS low_equity_""" + dataset)
#    c.execute(sql_create_dataset) 
#    
#    for x,y in low_dict.items():
#        db_low_value = x
#        db_appearances = y[0]
#        db_wins = y[1]
#        db_equity = y[2]
#    
#        sql_insert_command = """INSERT INTO low_equity_""" + dataset + """(
#                                                        low_string_value,
#                                                        appearances,
#                                                        wins,
#                                                        equity)
#                                                        VALUES(?, ?, ?, ?)"""
#                                                        
#        body_row = (db_low_value, db_appearances, db_wins,db_equity)
#        c.execute(sql_insert_command,body_row)
#        
    
    conn.commit()  
    conn.close()       