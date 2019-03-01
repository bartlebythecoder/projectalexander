def analyze_dataset_script(look_at_dataname,var1,var2,var3):
    import plotly.plotly as py
    import plotly.tools as tls
    import sqlite3
    from sqlite3 import Error
    import matplotlib.pyplot as plt
    import numpy as np
    from operator import itemgetter


    print('This is what was passed.')
    print(look_at_dataname)

    
    def getKey(item):
        return item[0]

    # def add_to_dict(two_card_dict,two_cards,victory):
        # if two_cards in two_card_dict:
            # two_card_dict[two_cards] = two_card_dict[two_cards] + victory
            # print('Found ' + two_cards)
        # else: 
            # print('Did not find ' + two_cards)
            # two_card_dict[two_cards] = victory
    

    if var1:    
        conn = sqlite3.connect('E:/Dropbox/Code/python/poker/omaha_eight.db')
        c = conn.cursor()

        sql3_select = 'SELECT * FROM low_counts WHERE dataset = "' + look_at_dataname + '"'

                                
        c.execute(sql3_select)
        allrows = []

        allrows = c.fetchall()
        print(look_at_dataname)
        print(allrows)

                
        
        no_lows = allrows[0][2]
        low_count = allrows[0][1]
        nut_count = allrows[0][5]
        non_nut_count = allrows[0][4]
        non_nut_shared = allrows[0][7]
        non_nut_solo = allrows[0][6]
        nut_solo = allrows[0][8]
        shared_low = allrows[0][3]
        shared_nut = allrows[0][9]
                
    
        print('Var1 = ' + str(var1))
        print('# of no lows: ' + str(no_lows))
        print('# of lows: ' + str(low_count))
        print('# of total shared lows: ' + str(shared_low))
        print('# of total non-nut lows: ' + str(non_nut_count))
        print('# of nut lows: ' + str(nut_count))
        print('# of total non-nut solo lows: ' + str(non_nut_solo))
        print('# of total non-nut shared lows: ' + str(non_nut_shared))
        print('# of nut solo lows: ' + str(nut_solo))
        print('# of nut shared lows: ' + str(shared_nut))

    
        
        labels = ['No Low','Non-Nut Low Solo','Non-Nut Low Shared','Nut Solo','Nut Shared']
        sizes = [no_lows, non_nut_solo, non_nut_shared, nut_solo, shared_nut]
        
        
        
        fig1, ax1 = plt.subplots()
        plt.figure(1)
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=False, startangle=90)
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.


        
    if var2 or var3:
    
        conn2 = sqlite3.connect('E:/Dropbox/Code/python/poker/omaha_eight.db')
        c2 = conn2.cursor()

        sql3_select2 = 'SELECT * FROM two_card_lows WHERE dataset = "' + look_at_dataname + '"'

                                
        c2.execute(sql3_select2)
        allrows = []

        allrows = c2.fetchall()
        print(look_at_dataname)
        print(allrows)    
        y_victories = allrows[0]
        y_victories = y_victories[1:len(y_victories)]
        x_two_cards = ['12','13','14','15','16','17','18','23','24','25','26','27','28','34','35','36','37','38','45','46','47','48','56','57','58','67','68','78']

        
    if var2:

        two_card_victories = []
        two_card_victories = zip(y_victories,x_two_cards)
        a = sorted(two_card_victories, key=getKey, reverse = True)
        print(a)
        
        y_axis,x_axis = zip(*a)
        plt.figure(2)
        plt.plot(x_axis,y_axis)


        
    if var3:
        wheel_total = 0
        no_wheel_total = 0
        wheel_index = 0
        print('Going into wheel loop')
        print(y_victories)
        for wheel_loop in x_two_cards:
            print(wheel_loop)
            wheel_list = ['12','13','14','15','23','24','25','34','35','45']
            if x_two_cards[wheel_index] in wheel_list:
                wheel_total += y_victories[wheel_index]
                print(str(y_victories[wheel_index]) + ' in')
            else:
                no_wheel_total += y_victories[wheel_index]
                print(str(y_victories[wheel_index]) + ' out')
            wheel_index += 1   
                
        labels = ['5s and under','At least one over 5']
        sizes = [wheel_total,no_wheel_total]
        

        fig1, ax2 = plt.subplots()
        plt.figure(3)
        ax2.pie(sizes, labels=labels, autopct='%1.1f%%',
                shadow=False, startangle=90)
        ax2.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()
                

     
    
