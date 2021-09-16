''' 
By: Jacky Liu
This program allows users to track their expenses. Features 
a login system, progress saving, all presented in a GUI
'''

import tkinter as tk
from tkinter import ttk
from ExpenseItem import ExpenseItem
from functools import partial
import pickle
import login
from datetime import date, datetime
import matplotlib.pyplot as plt

def handle_name(i, *args):
    '''reads input in name entry widget and sets input to an object'''
    name = name_vars[i].get()
    items[i].set_name(name)

def handle_expense(i, *args):
    '''reads input in expense entry widget and sets input to an object
    updates ExpenseItem.total
    '''
    amount = 0 
    try:
        amount = amount_vars[i].get()
    except: 
        amount_vars[i].set(0.0)
    items[i].set_amount(amount)
    items[i].update_total()

def append_expense(i): 
    '''appends widgets and tkinter variables to their respectives lists'''
    items.append(ExpenseItem())
    frames.append(tk.Frame(master=window, borderwidth=5, relief=tk.GROOVE))
    name_vars.append(tk.StringVar())
    amount_vars.append(tk.DoubleVar())
    name_labels.append(tk.Label(master=frames[i], text='Expense Name'))
    amount_labels.append(tk.Label(master=frames[i], text='Amount($)'))
    name_entries.append(tk.Entry(master=frames[i], textvariable=name_vars[i], 
                        bd=10, width=30))
    amount_entries.append(tk.Entry(master=frames[i], 
                          textvariable=amount_vars[i], bd=10))

def format_expense(i):
    '''formats widgets and tkinter variables'''
    frames[i].grid(row=i, column=0, padx=5, pady=15)
    name_labels[i].pack(side=tk.LEFT, padx=10)
    name_entries[i].pack(side=tk.LEFT)
    amount_labels[i].pack(side=tk.LEFT, padx=10)
    amount_entries[i].pack(side=tk.LEFT)
    name_vars[i].trace_add('write', partial(handle_name, i))
    amount_vars[i].trace_add('write', partial(handle_expense, i))

def create_expense(i):
    '''appends and formats widgets to allow a user to enter an expense'''
    append_expense(i)
    format_expense(i)

def add_expense():
    '''creates and formats widgets to add an expense'''
    i = len(items)
    create_expense(i)

def del_expense():
    '''destroys widgets to remove an expense'''
    i = len(items) - 1

    try: 
        frames[i].destroy()
        name_labels[i].destroy()
        name_entries[i].destroy()
        amount_labels[i].destroy()
        amount_entries[i].destroy()
        name_vars[i].set('')
        amount_vars[i].set('')

        items.pop()
        frames.pop()
        name_vars.pop()
        amount_vars.pop()
        name_labels.pop()
        amount_labels.pop()
        name_entries.pop()
        amount_entries.pop()
    except IndexError:
        pass

def create_button(txt, func, col):
    '''creates and formats a button'''
    frame = tk.Frame(master=window, padx=10)
    button = tk.Button(master=frame, text=txt, command=func)
    frame.grid(row=0, column=col)
    button.pack()

def update():
    '''updates the total counter'''
    total_expense.set(ExpenseItem.total)

def generate_graph(days, title):
    i = 0
    x_coord = []
    day_list = []
    total_list = []
    today = datetime.today()
    saved_totals_reversed = list(reversed(saved_dates.values()))
    for day in reversed(list(saved_dates.keys())):
        date_object = datetime.strptime(day, "%Y/%m/%d")
        print((today - date_object).days)
        if (today - date_object).days <= days:
            day_list.append(day)
            total_list.append(saved_totals_reversed[i])
            x_coord.append(i)
            i += 1
        else: 
            break
    
    total_list.reverse()
    day_list.reverse()
    plt.bar(x_coord, total_list, width=0.5, tick_label=day_list)
    plt.xlabel("Dates")
    plt.ylabel("Total Expense")
    plt.title(title)
    plt.show()
    
def view_day_graph():
    generate_graph(1, "Expenses in the past day")

def view_week_graph():
    generate_graph(7, "Expenses in the past week")

def view_month_graph():
    generate_graph(30, "Expenses in the past month")

def view_month_graph():
    generate_graph(365, "Expenses in the past year")

def save():
    '''saves user data into a bineary text file'''
    update()
    today = date.today().strftime("%Y/%m/%d")
    print(list(saved_dates.keys()))
    today_total = {today: ExpenseItem.total}
    if today in saved_dates:
        saved_dates[today] += ExpenseItem.total
    else:
        saved_dates.update(today_total)
    new_total = ExpenseItem.total + saved_total
    filled_items = []
    names = [item.get_name() for item in saved_items]

    for item in items:
        item_name = item.get_name()
        if item_name != '' and item.get_amount() != 0:
            if item_name in names:
                i = names.index(item_name)
                saved_items[i].set_amount(saved_items[i].get_amount() + item.get_amount())
            else:
                filled_items.append(item)
    new_items = saved_items + filled_items

    with open(username, 'wb') as f:
        pickle.dump(saved_dates, f)
        pickle.dump(new_total, f)
        pickle.dump(new_items, f)

def main():
    '''defines the mainline logic of the program'''

    #tries to open saved data from user if it exists
    try:
        with open(username, 'rb') as f:
            global saved_dates
            global saved_total
            global saved_items
            saved_dates = pickle.load(f)
            saved_total = pickle.load(f)
            saved_items = pickle.load(f)
            for i in saved_items:
                print(i.get_name())
                print(i.get_amount())
    except FileNotFoundError:
        pass
    
    global window
    window = tk.Tk()
    window.title("Expense tracker")

    #creates 3 expenses prompting user input
    for i in range(3):
        create_expense(i)

    create_button("Add Expense", add_expense, 1)
    create_button("Delete Expense", del_expense, 2)
    create_button("Save", save, 3)
    create_button("Update Total", update, 4)

    #widgets for the total counter
    frame = tk.Frame(master=window)
    frame.grid(row=0, column=5, padx=(10, 0))
    global total_expense
    total_expense = tk.DoubleVar()
    label = tk.Label(master=frame, textvariable=total_expense, 
                    background="white", bd=6, padx=50)
    label2 = tk.Label(master=frame, text="Total")
    label.grid(row=0, column=6, padx=(10, 0))
    label2.grid(row=0, column=5)

    window.mainloop()
        
#login interface
username = login.main_menu()

global saved_total
global saved_items
global saved_dates
saved_total = 0
saved_items = []
saved_dates = {}
items = []
name_vars = []
amount_vars = []
frames = []
name_labels = []
amount_labels = []
name_entries = []
amount_entries = []

if username != '':
    main()

view_week_graph()