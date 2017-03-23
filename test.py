from tkinter import *
from tkinter.messagebox import *

def do_about_dialog():
    tk_version = window.tk.call('info', 'patchlevel')
    showinfo(message= app_name + "\nThe answer to all your problems.\n\nTK version: " + tk_version)

def do_preferences():
    showinfo(message="Preferences window")

def do_button():
    print("You pushed my button")

def main():
    global app_name
    app_name = "Chocolate Rain"
    global window
    window = Tk()
    window.title("Main")

    # find out which version of Tk we are using
    tk_version = window.tk.call('info', 'patchlevel')
    tk_version = tk_version.replace('.', '')
    tk_version = tk_version[0:2]
    tk_version = int(tk_version)

    menubar = Menu(window)
    app_menu = Menu(menubar, name='apple')
    menubar.add_cascade(menu=app_menu)

    app_menu.add_command(label='About ' + app_name, command=do_about_dialog)
    app_menu.add_separator()

    if tk_version < 85:
       app_menu.add_command(label="Preferences...", command=do_preferences)
    else:
        # Tk 8.5 and up provides the Preferences menu item
        window.createcommand('tk::mac::ShowPreferences', do_preferences)

    window.config(menu=menubar) # sets the window to use this menubar

    my_button = Button(window, text="Push", command=do_button)
    my_button.grid(row=0, column=0, padx=50, pady=30)

    mainloop()

if __name__ == "__main__":
    main()