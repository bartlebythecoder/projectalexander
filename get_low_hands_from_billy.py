# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 11:10:08 2019
Build a file of Low Hands from the Billy the Kid Database
@author: sean
"""

import sqlite3
from build_hand import get_low_tot_from_string, get_low_winners_from_string, string_to_low, low_ranks, find_low, db_hand_to_low

conn = sqlite3.connect('E:/Dropbox/Code/python/poker/omaha_eight.db')
c = conn.cursor()

sql3_select = """ SELECT    hand_1,
                            hand_2,
                            hand_3,
                            hand_4,
                            hand_5,
                            hand_6,
                            hand_7,
                            hand_8,
                            hand_9,
                            hand_10
                    FROM dataset_Doc_Holliday """

                        
c.execute(sql3_select)
allrows = []
allrows = c.fetchall()    


sql_create_dataset = """CREATE TABLE low_values_dataset_Doc_Holliday (
    low_string_value TEXT PRIMARY KEY,
    no_cards INTEGER
    );"""
c.execute('DROP TABLE IF EXISTS low_values_dataset_Doc_Holliday')
c.execute(sql_create_dataset) 

final_low_list = []

row_count = 0
for e_row in allrows:
    row_count += 1
    hand_count = 0
    for e_hand in e_row:
        hand_count += 1
        low_answer = db_hand_to_low(e_hand)
        if low_answer not in final_low_list and len(low_answer) >= 2: 
            final_low_list.append(low_answer)
            print(str(row_count),str(hand_count),' ',e_hand,str(low_answer)) 
    
final_low_list.sort()
print(final_low_list)


x = 0
for each_low in final_low_list:
    low_string_insert = ''
    for low_number in each_low:
        low_string_insert = low_string_insert + str(low_number)    
    x += 1
    print(str(x), ' from each_low')
    print(each_low)
    print(low_string_insert)
    dummy_string=len(each_low)
    sql_low_list = """  INSERT INTO low_values_dataset_Doc_Holliday (low_string_value,no_cards) VALUES(?,?) """
    sql_low_row = (low_string_insert,dummy_string)
    c.execute(sql_low_list,sql_low_row)

conn.commit()  
conn.close()