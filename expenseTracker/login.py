'''
Jacky Liu
This program simulates a registration and login system
'''
import tkinter as tk

def append_login_info(file, text): 
    '''opens a file in append mode and writes one line of specified text'''
    with open(file, "a") as f:
        f.write(text + "\n")

def create_popup(txt, txt_color):
    popup = tk.Toplevel(master=window)
    popup.title("Popup")
    frame = tk.Frame(master=popup)
    label = tk.Label(master=popup, text=txt, fg=txt_color)
    frame.pack()
    label.pack()

def display_username_taken():
    '''creates a popup message that says username is taken'''
    create_popup("Username taken", "red")

def display_registration_error():
    '''creates a popup message that says error in registration'''
    create_popup("You did not enter a username or password", "red")

def display_registration_success():
    '''creates a popup message that says successful registration'''
    create_popup("Successful registration!", "green")
    screen.destroy()
    login_window()

def display_login_error(): #maybe a popup msg
    '''creates a popup message that says incorrect login info'''
    create_popup("Incorrect username or password", "red")

def display_login_success():
    '''creates a popup message that says successful login'''
    create_popup("Successful login!", "green")
    window.destroy()

def create_login_widgets(txt, padding, show_char, text_var):
    '''creates widgets for username and password boxes'''
    frame = tk.Frame(master=screen)
    lusername = tk.Label(master=frame, text=txt)
    entry_user = tk.Entry(master=frame, textvariable=text_var, show=show_char)
    frame.pack(pady=padding)
    lusername.pack(side=tk.LEFT)
    entry_user.pack(side=tk.LEFT)

def display_login_boxes(page, txt, func):
    '''displays all widgets related to the login/registration page'''
    global screen
    screen = tk.Toplevel(window)
    screen.title(page)
    screen.geometry("500x350")

    create_login_widgets("Username:", (100, 0), "", username_var)
    create_login_widgets("Password: ", (0, 0), "*", password_var)

    frame = tk.Frame(master=screen)
    button = tk.Button(master=frame, text=txt, command=func)
    frame.pack()
    button.pack(side=tk.LEFT)

def login_window():
    '''displays the login window'''
    display_login_boxes("Login Page", "Login", login)
 

def register_window():
    '''displays the registration window'''
    display_login_boxes("Registration Page", "Register", register)

def login():
    '''
    attempts to login by verifying username and password against previously stored
    usernames and passwords that were saved in a file.
    '''
    index = 0
    username = username_var.get()
    password = password_var.get()

    if password == '' or username == '':
        display_login_error()
        return
    with open("usernames.txt", "r") as f:
        lines = f.read().splitlines()
        if username in lines:
            index = lines.index(username)
        else:
            display_login_error()
            return
    with open("passwords.txt", "r") as file:
        lines = file.read().splitlines()
        if password == lines[index]:
            display_login_success()
        else:
            display_login_error() 
            

def register():
    '''
    attempts to register by checking if the inputted username is
    available

    appends username and password to their respective files if
    registration is successful
    '''
    username = username_var.get()
    password = password_var.get()

    if password == '' or username == '':
        display_registration_error()
        return
    with open("usernames.txt", "r") as f:
        lines = f.read().splitlines()
        if username in lines:
            display_username_taken()
            return

    append_login_info("usernames.txt", username)
    append_login_info("passwords.txt", password)
    display_registration_success()

def main_menu():
    '''displays the main login menu'''
    global window
    window = tk.Tk()
    window.title("Login Page")
    window.geometry("500x350")

    global username_var
    global password_var
    username_var = tk.StringVar()
    password_var = tk.StringVar()
    
    label = tk.Label(text="Welcome!", width=200, font=("Calibri", 40))
    login_button = tk.Button(text="Login", height=5, width=30, command=login_window)
    register_button = tk.Button(text="Register", height=5, width=30, command=register_window)

    label.pack()
    login_button.pack(pady=(30,40))
    register_button.pack(pady=10)

    window.mainloop()
    username = username_var.get()
    return username
