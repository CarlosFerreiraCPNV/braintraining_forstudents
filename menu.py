"""
Auteur : Carlos Ferreira
Date : 15.12.2023
Projet : Brain training for students
"""

import tkinter as tk
import geo01
import info02
import info05
from login import *
from result import *

# exercises array
a_exercise = ["geo01", "info02", "info05"]
albl_image = [None, None, None] # label (with images) array
a_image = [None, None, None] # images array
a_title = [None, None, None] # array of title (ex: GEO01)

dict_games = {"geo01": geo01.open_window_geo_01, "info02": info02.open_window_info_02, "info05": info05.open_window_info_05}

username_login = ""
password_login = ""

# call other windows (exercices)
def exercise(event,exer):
    dict_games[exer](window)


#call display_results
def display_result(event):
    create_window_login()
    print("display_result")


# Main window
window = tk.Tk()
window.title("Training, entrainement cérébral")
# Centre la fenetre au milieu de l'écran
w = 1100
h = 900
screen_W = window.winfo_screenwidth()
screen_H = window.winfo_screenheight()
x = (screen_W / 2) - (w / 2)
y = (screen_H / 2) - (h / 2)
window.geometry("%dx%d+%d+%d" % (w, h, x, y))

# color définition
rgb_color = (139, 201, 194)
hex_color = '#%02x%02x%02x' % rgb_color # translation in hexa
window.configure(bg=hex_color)
window.grid_columnconfigure((0, 1, 2), minsize=300, weight=1)

# Title création
lbl_title = tk.Label(window, text="TRAINING MENU", font=("Arial", 15))
lbl_title.grid(row=0, column=1,ipady=5, padx=40,pady=40)

# labels creation and positioning
for ex in range(len(a_exercise)):
    a_title[ex]=tk.Label(window, text=a_exercise[ex], font=("Arial", 15))
    a_title[ex].grid(row=1+2*(ex//3),column=ex % 3 , padx=40,pady=10) # 3 label per row

    a_image[ex] = tk.PhotoImage(file="img/" + a_exercise[ex] + ".gif") # image name
    albl_image[ex] = tk.Label(window, image=a_image[ex]) # put image on label
    albl_image[ex].grid(row=2 + 2*(ex // 3), column=ex % 3, padx=40, pady=10) # 3 label per row
    albl_image[ex].bind("<Button-1>", lambda event, ex = ex :exercise(event=None, exer=a_exercise[ex])) #link to others .py
    print(a_exercise[ex])

# Buttons, display results & quit
btn_display = tk.Button(window, text="Display results", font=("Arial", 15))
btn_display.grid(row=2 + 2 * len(a_exercise)//3, column=1)
btn_display.bind("<Button-1>", lambda e: display_result(e))

btn_finish = tk.Button(window, text="Quitter", font=("Arial", 15))
btn_finish.grid(row= 3 + 2 * len(a_exercise)//3 , column=1)
btn_finish.bind("<Button-1>", quit)

# Demande à l'utilisateur s'il veut vraiment fermer la fênetre
def on_closing():
    if messagebox.askokcancel("Quitter", "Voulez-vous vraiment quitter ?"):
        window.destroy()


window.protocol("WM_DELETE_WINDOW", on_closing)

# main loop
window.mainloop()
