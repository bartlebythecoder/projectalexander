def equity_script(dataset):
    import sqlite3
    from build_hand import db_hand_to_low, get_low_winners_from_string, list_to_string
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
        print(e_table)
        hands = []
        low_string = ''
        temp_list = []
        temp_string = ''
        index_winner_list = []
        winners_string = []
        win_equity = 0.0
        
        for x in range(4,14):

            if each_row[x] != '':
                temp_list = db_hand_to_low(each_row[x])
                temp_string = list_to_string(temp_list)
                hands.append(temp_string)
        
        winners_string = []
        index_winner_list = []
        winners_string = each_row[15]
        
        if winners_string != '':
            low_winners = get_low_winners_from_string(winners_string)
            for e_winner in low_winners:
                index_winner = int(e_winner)  # match the seat number with the list index
                index_winner_list.append(index_winner)
        else: index_winner_list = []
        
        seat_no = 0
        for e_hand in hands:
            seat_no += 1
            update_equity_list = [0,0]
            
            if len(e_hand) > 1:
            
                if seat_no in index_winner_list:
                    win_equity = round(1/len(index_winner_list),3)
                    update_equity_list = [1,win_equity] 
                else: update_equity_list = [1,0]
                
                if e_hand not in low_dict: 
                    low_dict[e_hand] = update_equity_list
                else:
                    low_dict[e_hand][0] += update_equity_list[0]
                    low_dict[e_hand][1] += update_equity_list[1]
    
#        print(hands,index_winner_list)
        
    for y in low_dict.values():
        win_pct = round(y[1]/y[0],3)
        y.append(win_pct)
    
    
#    print(low_dict)
    
    sql_create_dataset = """CREATE TABLE low_equity_""" + dataset + """( 
                                                    low_string_value TEXT PRIMARY KEY,
                                                    appearances INTEGER,
                                                    wins REAL,
                                                    equity);"""

    c.execute("""DROP TABLE IF EXISTS low_equity_""" + dataset)
    c.execute(sql_create_dataset) 
    
    for x,y in low_dict.items():
        db_low_value = x
        db_appearances = y[0]
        db_wins = y[1]
        db_equity = y[2]
    
        sql_insert_command = """INSERT INTO low_equity_""" + dataset + """(
                                                        low_string_value,
                                                        appearances,
                                                        wins,
                                                        equity)
                                                        VALUES(?, ?, ?, ?)"""
                                                        
        body_row = (db_low_value, db_appearances, db_wins,db_equity)
        c.execute(sql_insert_command,body_row)
        
    
    conn.commit()  
    conn.close()   