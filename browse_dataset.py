def browse_dataset(look_at_dataname):

    import sys, pygame
    import pydealer
    from pydealer.const import BOTTOM
    import sqlite3
    from build_hand import get_low_tot_from_string, get_low_winners_from_string
    pygame.init()



    def disp_cards(card_list,hoz,vert):
        for each_card in card_list:
            if each_card != '':
                new_pic = each_card + '.png'
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
        0   : 200,
        1   : 200,
        2   : 325,
        3   : 325,
        4   : 450,
        5   : 450,
        6   : 575,
        7   : 575,
        8   : 700,
        9   : 700}
        
    x_cord_dict = {
        0   :   50,
        1   :   550,
        2   :   50,
        3   :   550,
        4   :   50,
        5   :   550,
        6   :   50,
        7   :   550,
        8   :   50,
        9   :   550}
        

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

    crashed = False
    see_results = False

    while not crashed:

        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
                crashed = True
            else:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_RIGHT]: table_no += 1
                if keys[pygame.K_LEFT]: table_no -= 1
                if keys[pygame.K_SPACE]:
                    if see_results: see_results = False
                    else: see_results = True
                if keys[pygame.K_ESCAPE]: crashed = True
                    

                if table_no < 1: table_no = 1
                elif table_no > max_tables: table_no = max_tables

        
        screen.fill(green)
        table_index = table_no - 1
        board = get_board(table_index)
        disp_cards(board,250,60)
        low_board = allrows[table_index][14]
        if see_results:
            screen.blit(myfont.render('See Results', False, red),(700,10)) 
            if low_board == 1: 
                board_img = 'low.png' 
                
                low_string = allrows[table_index][15]            
                low_count = int(get_low_tot_from_string(low_string))
                nut_check = allrows[table_index][16]

                if low_count > 0:
                    winners_list = get_low_winners_from_string(low_string)

                    for count_loop in winners_list:
                        if nut_check ==1: low_img = 'made_nuts.png'
                        else: low_img = 'won_low.png'
                        low_coord = get_low_coord(count_loop)
                        screen.blit(pygame.image.load(low_img).convert_alpha(),(low_coord[0],low_coord[1])) 
            else: board_img = 'no_low.png'             
            screen.blit(pygame.image.load(board_img).convert_alpha(),(730,90))
        for hand_loop in range(10):
            hand = get_hands(table_index,hand_loop)
            y_cord = y_cord_dict[hand_loop]
            x_cord = x_cord_dict[hand_loop]
            disp_cards(hand,x_cord,y_cord)

        textsurface = myfont.render('Hand Number #' + str(table_no), False, white)   
        screen.blit(textsurface,(400,10))   
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
