# -*- coding: utf-8 -*-
"""
Created on Mon Apr 29 15:58:44 2019

@author: sean
"""

conn = sqlite3.connect('E:/Dropbox/Code/python/poker/omaha_eight.db')
c = conn.cursor()

sql3_select_ind = """ SELECT high_index FROM hand_index_high"""
                
                
c.execute(sql3_select_ind)
index_rows = []
index_rows = c.fetchall()                    

sql3_select_vin = """ SELECT    table_no,
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
                    FROM dataset_Londonium"""
                
                
c.execute(sql3_select_vin)
allrows = []
allrows = c.fetchall()                    

index_dict = {}
current_list = []


for each_index in index_rows:
    current_list.append(each_index[0])


print(current_list)





for each_row in allrows:
    print ("Table #" + str(each_row[0]))
    winner = 0
    winner = int(each_row[1])+4    
    for each_index in range(3,9):
        if each_row[each_index] not in current_list:
            print ("New one: " + each_row[each_index])
            index_dict[each_row[each_index]] = [1,0,''] 
            if winner == each_index: index_dict[each_row[each_index]][1] += 1 
            low_string = build_low_equivalent(each_row[each_index])
            index_dict[each_row[each_index]][2] = low_string
        

print (len(index_dict))
print (index_dict)      


#
#for x,y in index_dict.items():
#    high_index = x
#    low_index = y[2]
#    frequency = y[0]
#    wins = y[1]
#    vindolanda_equity = round(wins/frequency,3)
#
#
#    sql_insert_command = """INSERT INTO hand_index_high(
#                                                    high_index,
#                                                    low_index,
#                                                    frequency,
#                                                    vindolanda_equity)
#                                                    VALUES(?, ?, ?, ?)"""
#                                                    
#    body_row = (high_index, low_index, frequency, vindolanda_equity)
#    c.execute(sql_insert_command,body_row)
    

conn.commit()  
conn.close()   
    