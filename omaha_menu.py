# !/usr/bin/python3
from tkinter import *
from tkinter import messagebox, Checkbutton, IntVar
from analyze_dataset import analyze_dataset_script
from browse_dataset import browse_dataset
from build_dataset_lows import build_dataset
from play_dataset import play_dataset_script
from ai_play import ai_play_dataset_script
import sqlite3
from sqlite3 import Error

top = Tk()
top.title("Omaha 8 Book of Secrets")
top.geometry("800x600")
# photo1 = PhotoImage(file="hand.png")
# Label (top, image = photo1) .grid(row=0,column=0,sticky=W)

def send_to_analyzer(set,var1,var2,var3,analyzer):
    var1_pass = var1.get()
    var2_pass = var2.get()
    var3_pass = var3.get()
    analyzer.destroy()
    analyze_dataset_script(set,var1_pass,var2_pass,var3_pass)

def analyze_a_set(z):

    analyzer = Toplevel()
    analyzer.title("Build A New Dataset")
    var1 = IntVar()
    Checkbutton(analyzer, text="Nut vs Non-Nut Report", variable=var1).grid(row=0, sticky=W)
    var2 = IntVar()
    Checkbutton(analyzer, text="2 Card Low Report", variable=var2).grid(row=1, sticky=W)
    var3 = IntVar()
    Checkbutton(analyzer, text="Wheel/Non Wheel Breakdown", variable=var3).grid(row=2, sticky=W)
    Button(analyzer, text='Cancel', command=analyzer.destroy).grid(row=6, sticky=W, pady=2)
    Button(analyzer, text='Submit', command=lambda: send_to_analyzer(z,var1,var2,var3,analyzer)).grid(row=6,column=2, sticky=W, pady=2)

   
def helloCallBack():
   msg = messagebox.showinfo( "Coming Soon", "This feature has not been built yet")
   photo1 = PhotoImage(file="hand.png")
#   Label (msg, image = photo1) .grid(row=0,column=0,sticky=W)

def build_it(e1,e2,e3,e4,builder):
    e1s = str(e1.get())
    e2s = str(e2.get())
    e3s = str(e3.get())
    e4s = str(e4.get())
    print('Strings:')
    print(e1s,e2s,e3s,e4s)
    builder.destroy()
    build_dataset(e1s,e2s,e3s,e4s)

def enter_db_details():
    builder = Toplevel()
    builder.title("Build A New Dataset")
    Label(builder, text="Dataset Name (no spaces):").grid(row=0)
    Label(builder, text="# of Hands (1 to 10):").grid(row=1)
    Label(builder, text="# of Tables:").grid(row=2)
    Label(builder, text="Description:").grid(row=3)

    e1 = Entry(builder)
    e2 = Entry(builder)
    e3 = Entry(builder)
    e4 = Entry(builder)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)
    e4.grid(row=3, column=1)
    
    Button(builder, text='Cancel', command=builder.destroy).grid(row=4, column=0, sticky=W, pady=4)
    Button(builder, text='Submit', command=lambda: build_it(e1,e2,e3,e4,builder)).grid(row=4, column=1, sticky=W, pady=4)
    
    

def get_data():
    conn = sqlite3.connect('E:/Dropbox/Code/python/poker/omaha_eight.db')
    c = conn.cursor()

    sql3_select = """ SELECT    ID,
                                db_name, 
                                screen_name, 
                                hands,
                                tables,
                                screen_description 
                        FROM datasets"""

                            
    c.execute(sql3_select)
    allrows = []

    allrows = c.fetchall()    
    conn.commit()  
    conn.close()
    return allrows

    
def create_menus():    
    # create a toplevel menu
    menubar = Menu(top)

    # create a pulldown menu, and add it to the menu bar
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=helloCallBack)
    filemenu.add_command(label="Save", command=helloCallBack)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=top.quit)
    menubar.add_cascade(label="File", menu=filemenu)

    # create more pulldown menus
    dbmenu = Menu(menubar, tearoff=0)
    dbmenu.add_command(label="Build a New Dataset", command=enter_db_details)
    dbmenu.add_command(label="Browse a Dataset", command=helloCallBack)
    dbmenu.add_command(label="Analyze a Dataset", command=helloCallBack)
    menubar.add_cascade(label="Dataset", menu=dbmenu)

    helpmenu = Menu(menubar, tearoff=0)
    helpmenu.add_command(label="About", command=helloCallBack)
    menubar.add_cascade(label="Help", menu=helpmenu)
       

    # display the menu
    top.config(menu=menubar)     
    
def list_sets(allrows):
    title_label = Label(top, text = "Current Datasets", relief = SUNKEN)
    title_label.grid(row = 1, column = 1, ipadx = 10, padx = 5, pady = 5)
    hands_label = Label(top, text = "# Hands", relief = SUNKEN)
    hands_label.grid(row = 1, column = 2, ipadx = 10, padx = 5, pady = 5)
    
    tables_label = Label(top, text = "# Tables", relief = SUNKEN)
    tables_label.grid(row = 1, column = 3, ipadx = 10, padx = 5, pady = 5)
    
    desc_label = Label(top, text = "Description",relief = SUNKEN)
    desc_label.grid(row = 1, column = 4, ipadx = 50, padx = 5, pady = 5)
    action_label = Label(top, text = "Action",relief = SUNKEN)
    action_label.grid(row = 1, column = 5, ipadx = 100, padx = 5, pady = 5, columnspan=5)
    y = 2
    x = 1 
    for loop in allrows:
        ds_name = loop[2]
        row_label = Label(top, text=ds_name)
        row_label.grid(row = y, column = x, ipadx = 10)
        
        ds_hands = loop[3]
        hand_y = y
        hand_x = x + 1
        ds_hand_label = Label(top, text=ds_hands)
        ds_hand_label.grid(row = hand_y, column = hand_x, ipadx = 10)      


        ds_tables = loop[4]
        tables_y = y
        tables_x = x + 2
        tables_label = Label(top, text=ds_tables)
        tables_label.grid(row = tables_y, column = tables_x, ipadx = 10)      
      
        
        ds_desc = loop[5]
        desc_y = y
        desc_x = x + 3
        desc_label = Label(top, text=ds_desc)
        desc_label.grid(row = desc_y, column = desc_x)    

        ds_browse_name = loop[1]
        browse_y = y
        browse_x = x + 4
        browse_button = Button(top, text="Browse", command = lambda loop = loop: browse_dataset(loop[1]), relief = RAISED)
        browse_button.grid(row = browse_y, column = browse_x, ipadx = 10, padx =1)    

        ds_analyze_name = loop[1]
        analyze_y = y
        analyze_x = x + 5
        analyze_button = Button(top, text="Analyze", command = lambda loop = loop: analyze_a_set(loop[1]), relief = RAISED)
        analyze_button.grid(row = analyze_y, column = analyze_x, ipadx = 10, padx =1)   

        play_y = y
        play_x = x + 6
        play_button = Button(top, text="Play", command = lambda loop = loop: play_dataset_script(loop[1]), relief = RAISED)
        play_button.grid(row = play_y, column = play_x, ipadx = 10, padx =1) 
        
        ai_play_y = y
        ai_play_x = x + 7
        ai_play_button = Button(top, text="AI", command = lambda loop = loop: ai_play_dataset_script(loop[1]), relief = RAISED)
        ai_play_button.grid(row = ai_play_y, column = ai_play_x, ipadx = 10, padx =1) 
        
        
        
        y += 1
        
    
    build_button = Button(top, text="Build A New Dataset", command = enter_db_details, relief = RAISED)
    build_button.grid(row = 0, column = 1, ipadx = 10, padx = 10, ipady = 5, pady = 5)   
    refresh_button = Button(top, text="Refresh", command = create_screan, relief = RAISED)
    refresh_button.grid(row = 0, column = 5, ipadx = 5, padx = 2, ipady = 5, pady = 5)   
    exit_button = Button(top, text="Exit", command = top.destroy, relief = RAISED)
    exit_button.grid(row = 0, column = 8, ipadx = 10, padx = 2, ipady = 5, pady = 5)   

def create_screan():
    allrows = get_data()
    list_sets(allrows)   
   
create_menus()
create_screan()
top.mainloop()