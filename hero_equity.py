# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 18:26:49 2019

@author: sean
"""

def hero_equity_script():
    import plotly.plotly as py
    import plotly.tools as tls
    import sqlite3
    from sqlite3 import Error
    import matplotlib.pyplot as plt
    import numpy as np
    from operator import itemgetter


    conn = sqlite3.connect('E:/Dropbox/Code/python/poker/omaha_eight.db')
    c = conn.cursor()

    sql3_select = """SELECT low_cards,win_equity_all_hands FROM low_hero_hands"""
                            
    c.execute(sql3_select)
    allrows = []

    allrows = c.fetchall()
    
    conn.commit()  
    conn.close()
    
    hands = []
    equity = []
    
    for each_row in allrows:
        full_hand = each_row[0]
        split_hand = full_hand.split("_")
        hands.append(split_hand[2])
        equity_round = round(each_row[1]*100)
        equity.append(equity_round)
    
    
    plt.bar(hands,equity)
    for a,b in zip(hands, equity):
        plt.text(a, b-5, str(b),horizontalalignment='center',verticalalignment='center',color='white')
    plt.show()
    