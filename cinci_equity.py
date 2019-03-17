def cinci_equity_script():
    import sqlite3
    print('Here goes!')
    print('We are in Highhands branch')
    
    
    conn = sqlite3.connect('E:/Dropbox/Code/python/poker/omaha_eight.db')
    c = conn.cursor()

    sql3_select = """SELECT * FROM low_equity_dataset_CinciKid"""
                            
    c.execute(sql3_select)
    allrows = []

    allrows = c.fetchall()
    
    total_rows = 0
    total_appearances = 0
    total_wins = 0
    
    for e_row in allrows:
        total_rows += 1
        total_wins += e_row[2]
        total_appearances += e_row[1]

    average_equity = total_wins / total_appearances    
    print('Total Lows is: ' + str(total_rows))
    print('Total Wins is: ' + str(total_wins))
    print('Total appearances is: ' + str(total_appearances))
    print('Average equity is: ' + str(average_equity))

        
        
        
    
    
    
    
    
    
    
    conn.commit()  
    conn.close()