# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 15:58:44 2019

@author: sean
"""

def build_low_equivalent(hand):
    low_list = ['A','2','3','4','5','6','7','8']
    low_hand = ''
    check = ''
    for x in range(0,len(hand)):
        if hand[x] in low_list:
            low_hand = low_hand + hand[x]
    check = list(set(low_hand))
    if len(check) < 2: low_hand = ''
    return(low_hand)




conn = sqlite3.connect('E:/Dropbox/Code/python/poker/omaha_eight.db')
c = conn.cursor()

sql3_select = """ SELECT    table_no,
                            high_winners,
                            high_value,
                            hand_1_index,
                            hand_2_index,
                            hand_3_index,
                            hand_4_index,
                            hand_5_index,
                            hand_6_index,
                            hand_7_index,
                            hand_8_index,
                            hand_9_index,
                            hand_10_index
                    FROM dataset_Vindolanda"""
                
                
c.execute(sql3_select)
allrows = []

allrows = c.fetchall()                    

index_dict = {}



for each_row in allrows:
    print ("Table #" + str(each_row[0]))
    winner = 0
    winner = int(each_row[1])+4    
    for each_index in range(3,9):
        if each_row[each_index] not in index_dict:
            print ("New one: " + each_row[each_index])
            index_dict[each_row[each_index]] = [1,0,''] 
        else:
            index_dict[each_row[each_index]][0] += 1
            
        if winner == each_index: index_dict[each_row[each_index]][1] += 1 
        low_string = build_low_equivalent(each_row[each_index])
        index_dict[each_row[each_index]][2] = low_string
        

print (len(index_dict))
print (index_dict)      


  
sql_create_dataset = """CREATE TABLE hand_index_high( 
                                                high_index TEXT PRIMARY KEY,
                                                low_index INTEGER,
                                                frequency,
                                                vindolanda_equity);"""

c.execute("""DROP TABLE IF EXISTS hand_index_high""")
c.execute(sql_create_dataset) 

for x,y in index_dict.items():
    high_index = x
    low_index = y[2]
    frequency = y[0]
    wins = y[1]
    vindolanda_equity = round(wins/frequency,3)


    sql_insert_command = """INSERT INTO hand_index_high(
                                                    high_index,
                                                    low_index,
                                                    frequency,
                                                    vindolanda_equity)
                                                    VALUES(?, ?, ?, ?)"""
                                                    
    body_row = (high_index, low_index, frequency, vindolanda_equity)
    c.execute(sql_insert_command,body_row)
    

conn.commit()  
conn.close()   
    