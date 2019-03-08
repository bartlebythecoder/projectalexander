def hero_results_script(look_at_dataname):
    import plotly.plotly as py
    import plotly.tools as tls
    import sqlite3
    from sqlite3 import Error
    import matplotlib.pyplot as plt
    import numpy as np
    from operator import itemgetter


    print('This is what was passed.')
    print(look_at_dataname)

    conn = sqlite3.connect('E:/Dropbox/Code/python/poker/omaha_eight.db')
    c = conn.cursor()

    sql3_select = """SELECT low_board,low_hands,nut_check FROM """ + look_at_dataname
                            
    c.execute(sql3_select)
    allrows = []

    allrows = c.fetchall()
    
    #print(allrows)
    
    low_wins = 0
    low_equity = 0
    low_ties = 0
    low_losses = 0
    nut_lows = 0
    non_lows = 0
    total_lows = 0
    total_tables = 0
    win_equity = 0
    win_pct = 0
    for x in allrows:
        total_tables += 1
        print(total_tables)
        print(x)
        
        if x[0] == 1:
            total_lows += 1
            if x[1] != '':
                if x[1][2] == '1':
                    if x[2] == 1: nut_lows += 1
                    if x[1][0] == '1':
                        low_wins += 1
                        low_equity += 1
                    else:
                        low_ties += 1
                        low_equity += 1/int(x[1][0])
                else: low_losses += 1        
            else: low_losses += 1
        else: non_lows +=1 
            
    
        
    win_equity = low_equity / total_tables
    string_equity = str(win_equity)
    
    win_pct = low_equity / total_lows
    string_win = str(win_pct)

    
    print('Solo Wins: ' + str(low_wins))
    print('Nut Wins: ' + str(nut_lows))
    print('Chops: ' + str(low_ties))
    print('Win Equity: ' + string_equity)
    print('Losses: ' + str(low_losses))  
    print('Lows: ' + str(total_lows))
    print('Non Lows: ' + str(non_lows))
    print('Total: ' + str(total_tables))
    
    labels = ['Wins','Chops','Losses']
    sizes = [low_wins,low_ties,low_losses]
    

    fig1, ax2 = plt.subplots()
    plt.figure(3)
    ax2.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=False, startangle=90)
    ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()
    

    # Uncomment the below for a new low
    
           
        
    sqlcommand = '''    INSERT INTO low_hero_hands (low_cards, 
                        total,
                        non_low_total,
                        low_total,
                        solo_wins,
                        nut_wins,
                        chops,
                        win_pct_when_low,
                        win_equity_all_hands) 
                        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?) '''
                        


                        
    dataset_row =      (look_at_dataname,
                        total_tables,
                        non_lows,
                        total_lows,
                        low_wins,
                        nut_lows,
                        low_ties,
                        win_pct,
                        win_equity)

    c.execute(sqlcommand, dataset_row)        



               
       
    conn.commit()  
    conn.close()