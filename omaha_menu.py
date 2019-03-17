# !/usr/bin/python3
from tkinter import messagebox, Checkbutton, IntVar, Radiobutton, StringVar
from tkinter import *
from analyze_dataset import analyze_dataset_script
from hero_results import hero_results_script
from browse_dataset import browse_dataset
from build_dataset_lows import build_dataset
from play_dataset import play_dataset_script
from ai_play import ai_play_dataset_script
from hero_hand import hero_hand_run
import sqlite3
from sqlite3 import Error
from hero_equity import hero_equity_script
from equity import equity_script
from cinci_equity import cinci_equity_script

top = Tk()
top.title("Omaha 8 Book of Secrets")
top.geometry("1000x800")
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

def send_to_ai_play(z,ai_var,ai_root):
    ai_var_pass = ai_var.get()
    ai_root.destroy()
    ai_play_dataset_script(z,ai_var_pass)

def choose_ai_option(z):
    ai_root = Toplevel()
    ai_root.title("How Should the AI Play?")
    ai_var = StringVar(value="1")

    Radiobutton(ai_root, text="AI Always Calls", variable=ai_var, value="1").grid(row=1, sticky=W,pady=2)
    Radiobutton(ai_root, text="AI Guesses", variable=ai_var, value="2").grid(row=2, sticky=W,pady=2)
    Radiobutton(ai_root, text="AI Uses BillyKid Model", variable=ai_var, value="3").grid(row=3, sticky=W,pady=2)
    Button(ai_root, text='Cancel', command=ai_root.destroy).grid(row=4, sticky=W,pady=2)
    Button(ai_root, text='Submit', command=lambda: send_to_ai_play(z,ai_var,ai_root)).grid(row=4,column = 2, sticky=W,pady=2)


   
def helloCallBack():
    msg = messagebox.showinfo( "Coming Soon", "This feature has not been built yet")


def build_it(e1,e2,e3,e4,e5,builder):
    e1s = str(e1.get())
    e2s = str(e2.get())
    e3s = str(e3.get())
    e4s = str(e4.get())
    e5s = str(e5.get())
    print('Strings:')
    print(e1s,e2s,e3s,e4s,e5s)
    builder.destroy()
    build_dataset(e1s,e2s,e3s,e4s,e5s)

def enter_db_details():
    builder = Toplevel()
    builder.title("Build A New Dataset")
    Label(builder, text="Dataset Name (no spaces):").grid(row=0)
    Label(builder, text="# of Players (1 to 10):").grid(row=1)
    Label(builder, text="# of Tables:").grid(row=2)
    Label(builder, text="Description:").grid(row=3)
    Label(builder, text="Hero Hand:").grid(row=4)
    

    e1 = Entry(builder)
    e2 = Entry(builder)
    e3 = Entry(builder)
    e4 = Entry(builder)
    e5 = Entry(builder)

    e1.grid(row=0, column=1)
    e2.grid(row=1, column=1)
    e3.grid(row=2, column=1)
    e4.grid(row=3, column=1)
    e5.grid(row=4, column=1)
    
    Button(builder, text='Cancel', command=builder.destroy).grid(row=5, column=0, sticky=W, pady=4)
    Button(builder, text='Submit', command=lambda: build_it(e1,e2,e3,e4,e5,builder)).grid(row=5, column=1, sticky=W, pady=4)
    
    

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

def get_all_lows():
    
    conn = sqlite3.connect('E:/Dropbox/Code/python/poker/omaha_eight.db')
    c = conn.cursor()

    sql_low_value = """ SELECT low_string_value FROM low_values_dataset """
    c.execute(sql_low_value)    
    lowrows = []
    lowrows = c.fetchall()
    conn.commit()  
    conn.close()
    return lowrows
    
def create_menus():    
    # create a toplevel menu
    menubar = Menu(top)

    # create a pulldown menu, and add it to the menu bar
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="New", command=helloCallBack)
    filemenu.add_command(label="Save", command=helloCallBack)
    filemenu.add_separator()
    filemenu.add_command(label="Exit", command=top.destroy)
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


def refresh_dataset(x):
    x.destroy()
    create_screan()
    
    
def send_hero_hand(button,dataset,h_frame):
    hero_hand_run(button,dataset)
    h_frame.destroy()    

  

def list_sets(allrows):
    
    datasetframe = Frame(top,width=900,height=400)
    datasetframe.grid(row=0,column=0)
   
    
    title_label = Label(datasetframe, text = "Current Datasets", relief = SUNKEN)
    title_label.grid(row = 1, column = 1, ipadx = 10, padx = 5, pady = 5)
    hands_label = Label(datasetframe, text = "# Players", relief = SUNKEN)
    hands_label.grid(row = 1, column = 2, ipadx = 10, padx = 5, pady = 5)
    
    tables_label = Label(datasetframe, text = "# Tables", relief = SUNKEN)
    tables_label.grid(row = 1, column = 3, ipadx = 10, padx = 5, pady = 5)
    
    desc_label = Label(datasetframe, text = "Description",relief = SUNKEN)
    desc_label.grid(row = 1, column = 4, ipadx = 50, padx = 5, pady = 5)
    action_label = Label(datasetframe, text = "Action",relief = SUNKEN)
    action_label.grid(row = 1, column = 5, ipadx = 10, padx = 10, pady = 5, columnspan=10)
    y = 2
    x = 1 
    for loop in allrows:
        ds_name = loop[2]
        row_label = Label(datasetframe, text=ds_name)
        row_label.grid(row = y, column = x, ipadx = 10)
        
        ds_hands = loop[3]
        hand_y = y
        hand_x = x + 1
        ds_hand_label = Label(datasetframe, text=ds_hands)
        ds_hand_label.grid(row = hand_y, column = hand_x, ipadx = 10)      


        ds_tables = loop[4]
        tables_y = y
        tables_x = x + 2
        tables_label = Label(datasetframe, text=ds_tables)
        tables_label.grid(row = tables_y, column = tables_x, ipadx = 10)      
      
        
        ds_desc = loop[5]
        desc_y = y
        desc_x = x + 3
        desc_label = Label(datasetframe, text=ds_desc)
        desc_label.grid(row = desc_y, column = desc_x)    

        ds_browse_name = loop[1]
        browse_y = y
        browse_x = x + 4
        browse_button = Button(datasetframe, text="Browse", command = lambda loop = loop: browse_dataset(loop[1]), relief = RAISED)
        browse_button.grid(row = browse_y, column = browse_x, ipadx = 10, padx =1)    

        ds_analyze_name = loop[1]
        analyze_y = y
        analyze_x = x + 5
        analyze_button = Button(datasetframe, text="Analyze", command = lambda loop = loop: analyze_a_set(loop[1]), relief = RAISED)
        analyze_button.grid(row = analyze_y, column = analyze_x, ipadx = 10, padx =1)   

        play_y = y
        play_x = x + 6
        play_button = Button(datasetframe, text="Play", command = lambda loop = loop: play_dataset_script(loop[1]), relief = RAISED)
        play_button.grid(row = play_y, column = play_x, ipadx = 10, padx =1) 
        
        ai_play_y = y
        ai_play_x = x + 7
        ai_play_button = Button(datasetframe, text="AI", command = lambda loop = loop: choose_ai_option(loop[1]), relief = RAISED)
        ai_play_button.grid(row = ai_play_y, column = ai_play_x, ipadx = 10, padx =1) 
        
#        hero_y = y
#        hero_x = x + 8
#        hero_button = Button(datasetframe, text="Hero", command = lambda loop = loop: hero_results_script(loop[1]), relief = RAISED)
#        hero_button.grid(row = hero_y, column = hero_x, ipadx = 10, padx =1) 
        
        equity_y = y
        equity_x = x + 9
        equity_button = Button(datasetframe, text="Equity", command = lambda loop = loop: equity_script(loop[1]), relief = RAISED)
        equity_button.grid(row = equity_y, column = equity_x, ipadx = 10, padx =1) 
        
        
        
        y += 1
        
    
    build_button = Button(datasetframe, text="Build A New Dataset", command = enter_db_details, relief = RAISED)
    build_button.grid(row = 0, column = 1, ipadx = 10, padx = 10, ipady = 5, pady = 5)   
    refresh_button = Button(datasetframe, text="Refresh", command = lambda: refresh_dataset(datasetframe), relief = RAISED)
    refresh_button.grid(row = 0, column = 5, ipadx = 5, padx = 2, ipady = 5, pady = 5)   
    exit_button = Button(datasetframe, text="Exit", command = top.destroy, relief = RAISED)
    exit_button.grid(row = 0, column = y-1, ipadx = 10, padx = 2, ipady = 5, pady = 5)  
    
#    hero_eq_button = Button(datasetframe, text="Hero Equities", command = hero_equity_script, relief = RAISED)
#    hero_eq_button.grid(row = y+1, column = 2, ipadx = 10, padx = 2, ipady = 5, pady = 5)  
#    
#    six_hand_eq_button = Button(datasetframe, text="Cinci Equities", command = cinci_equity_script, relief = RAISED)
#    six_hand_eq_button.grid(row = y+1, column = 4, ipadx = 10, padx = 2, ipady = 5, pady = 5)  
    


def create_screan():
    allrows = get_data()
    list_sets(allrows)  

   
create_menus()
create_screan()
top.mainloop()