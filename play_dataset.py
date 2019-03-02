def play_dataset_script(look_at_dataname):

    import sys, pygame
    import pydealer
    from pydealer.const import BOTTOM
    import sqlite3
    from build_hand import get_low_tot_from_string, get_low_winners_from_string, string_to_low, low_ranks, find_low
    pygame.init()



    def disp_cards(card_list,hoz,vert):
        for each_card in card_list:
            if each_card != '':
                new_pic = each_card + '.png'
                screen.blit(pygame.image.load(new_pic).convert_alpha(),(hoz,vert))
                hoz += 100
                
    def disp_cards_villain(card_list,hoz,vert):
        for each_card in card_list:
            if each_card != '':
                new_pic = 'yellow_back.png'
                screen.blit(pygame.image.load(new_pic).convert_alpha(),(hoz,vert))
                hoz += 100
                        
            
    def get_board(table_index):
        board = []
        board.append(allrows[table_index][1][0:2])
        board.append(allrows[table_index][1][2:4])
        board.append(allrows[table_index][1][4:6])
        board.append(allrows[table_index][2][0:2])
        board.append(allrows[table_index][3][0:2])
        return(board)
        
    def get_hands(table_index, hand_no):
        hand = []
        hand_index = hand_no + 4
        hand.append(allrows[table_index][hand_index][0:2])
        hand.append(allrows[table_index][hand_index][2:4])
        hand.append(allrows[table_index][hand_index][4:6])
        hand.append(allrows[table_index][hand_index][6:8])
        return(hand)    

        
    def get_low_coord(table):
        
        low_coord_dict = {
        '1'   : [425,255],
        '2'   : [925,255],
        '3'   : [425,380],
        '4'   : [925,380],
        '5'   : [425,505],
        '6'   : [925,505],
        '7'   : [425,630],
        '8'   : [925,630],
        '9'   : [425,755],
        '10'  : [925,755]}
        
        table_place = []
        table_place = low_coord_dict[table]
        return(table_place)

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
                                nut_check
                        FROM """ + look_at_dataname

                            
    c.execute(sql3_select)
    allrows = []

    allrows = c.fetchall()    

    y_cord_dict = {
        0   : 150,
        1   : 550}
        
    x_cord_dict = {
        0   :   300,
        1   :   300}
        

    table_no = 1
    table_index = table_no - 1 
    max_tables = len(allrows) 

       
    size = width, height = 1000, 850
    black = 0, 0, 0
    white = (255,255,255)
    red = (255,0,0)
    green = (0,102,0)

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Omaha Eight Book of Secrets')
    myfont = pygame.font.SysFont('Helvetica', 20)
    clock = pygame.time.Clock()
    low_games_list = []
    hero_roll = 0
    villain_roll = 0
    pot = 0

    result_surface = result_surface = myfont.render('', False, white) 
    crashed = False
    see_results = False
    decision_time = False
    low_result = 'chop'
    hero_fold = False
    
    while not crashed:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
                crashed = True
            else:
                keys = pygame.key.get_pressed()

                # if keys[pygame.K_RIGHT]: table_no += 1
                # if keys[pygame.K_LEFT]: table_no -= 1
                # if keys[pygame.K_SPACE]:
                    # if see_results: see_results = False
                    # else: see_results = True
                result = 0   
                if decision_time == True:
                    print(hero_low_hand[0:5])
                    print(villain_low_hand[0:5])
                    if hero_low_hand != [] and villain_low_hand != []:
                        result = 1
                        if hero_low_hand[0:5] == villain_low_hand[0:5]:
                            low_result = 'chop'
                        elif hero_low_hand[0:5] < villain_low_hand[0:5]:  
                            low_result = 'hero'
                        else: low_result = 'villain'
                    elif hero_low_hand == [] and villain_low_hand != []:
                        low_result = 'villain'
                        result = 2
                    elif hero_low_hand != [] and villain_low_hand == []:
                        low_result = 'hero'
                        result = 3
                    elif hero_low_hand == [] and villain_low_hand == []:
                        low_result = 'chop'
                        result = 4
                    else: 
                        low_result = 'problem'
                        result = 5
                    print(str(result))    
                    
                
                    if see_results == False:
                        if keys[pygame.K_c]:
                            hero_roll -= 100
                            pot += 100
                            see_results = True
                            if low_result == 'chop':
                                result_surface = myfont.render('You chopped', False, white)
                                villain_roll += pot/2
                                hero_roll += pot/2
                                
                            elif low_result == 'villain':
                                result_surface = myfont.render('You lost. Tough beat.', False, white) 
                                villain_roll += pot
                                
                            elif low_result == 'hero':
                                result_surface = myfont.render('You win.  Good call!', False, white) 
                                hero_roll += pot
                                
                            else:
                                result_surface = myfont.render('We have a problem!', False, white)                         
                        
                            pot = 0
                        
                        
                        
                        if keys[pygame.K_f]:
                            villain_roll += pot
                            pot = 0
                            see_results = True
                            hero_fold = True
  
                            if low_result == 'chop':
                                result_surface = myfont.render('You fold.  It would have been a chop.', False, white)                            
                            elif low_result == 'villain':
                                result_surface = myfont.render('You fold.  Good move! You would have lost.', False, white) 
                            elif low_result == 'hero':
                                result_surface = myfont.render('You fold.  Too bad! You would have won!', False, white) 
                            else:
                                result_surface = myfont.render('We have a problem!', False, white) 
                    else:        
                        
                        if keys[pygame.K_RIGHT]: 
                            table_no += 1    
                            result_surface = result_surface = myfont.render('', False, white) 
                            decision_time = False
                            see_results = False
                            pot = 0
                        
                else: 
                    if keys[pygame.K_r]:
                        decision_time = True
                        pot += 100
                        villain_roll -= 100


                if keys[pygame.K_ESCAPE]: crashed = True
                    

                if table_no < 1: table_no = 1
                elif table_no > max_tables: table_no = max_tables

        table_index = table_no - 1
        low_board = allrows[table_index][14]
        while low_board != 1 and table_no < max_tables:
            table_no += 1
            table_index = table_no - 1
            low_board = allrows[table_index][14]  
       
        
        screen.fill(green)

        board = get_board(table_index)
        board_low_list = string_to_low(board)
        disp_cards(board,250,350)
        low_board = allrows[table_index][14]
                
        villain_hand = get_hands(table_index,0)
        villain_low_list = string_to_low(villain_hand)
        villain_low_hand = find_low(board_low_list,villain_low_list)
        
        
        
        hero_hand = get_hands(table_index,1)
        y_cord = y_cord_dict[1]
        x_cord = x_cord_dict[1]
        hero_low_list = string_to_low(hero_hand)
        hero_low_hand = find_low(board_low_list,hero_low_list)
        

        
        
        
        
        disp_cards(hero_hand,x_cord,y_cord)
        
        
        if see_results:
            screen.blit(myfont.render('See Results', False, red),(700,10)) 
            y_cord = y_cord_dict[0]
            x_cord = x_cord_dict[0]
            disp_cards(villain_hand,x_cord,y_cord)

                
                
                
                

        else:
            
            y_cord = y_cord_dict[0]
            x_cord = x_cord_dict[0]
            disp_cards_villain(villain_hand,x_cord,y_cord)
        
        
        
        
        textsurface = myfont.render('Hand Number #' + str(table_no), False, white)   
        
        pot_surface = myfont.render('Pot: $' + str(pot), False, white)  
        hero_surface = myfont.render('$' + str(hero_roll), False, white)  
        villain_surface = myfont.render('$' + str(villain_roll), False, white) 
        if decision_time == False:
            instruction_surface = myfont.render('Press R when ready', False, white) 
            instruction_start = 400
        elif see_results == False:
            instruction_surface = myfont.render('$100 to you. (C)all or (F)old.', False, white) 
            instruction_start = 350
        else:
            instruction_surface = myfont.render('Hit -> for next hand', False, white) 
            instruction_start = 400
        
        screen.blit(result_surface,(0,0))
        screen.blit(pot_surface,(100,400))   
        screen.blit(textsurface,(400,50))   
        screen.blit(hero_surface,(150,650))   
        screen.blit(villain_surface,(150,125))   
        screen.blit(instruction_surface,(instruction_start,710)) 
        
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
