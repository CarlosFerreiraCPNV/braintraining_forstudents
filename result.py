#############################
# Training (Menu)
# JCY oct 23
# PRO DB PY
#############################

import tkinter as tk
from tkinter import *
from database import *
import geo01
import info02
import info05

# TABLEAU DES VALEURS DU JEU
top_label_list = [("Elève", "Exercice", "Date", "Temps", "Nb Ok", "Nb Total", "% Total")]

for x in range(len(data_list)):
    print()

# call other windows (exercices)
def results():

    def display_tuple_in_table(mytuple):
        for line in range(0, len(mytuple)):
            for col in range(0, len(mytuple[line])):
                (tk.Label(list_of_results_frame, text=mytuple[line][col], width=14, font=("Arial", 10)).grid(row=line,column=col,padx=2,pady=2))

    def clear(event):
        for widget in frame_results.winfo_children():
            widget.grid_forget()

    # Main window
    window = tk.Tk()
    window.title("Affichage braintraining")
    window.geometry("1100x900")

    # color définition
    rgb_color = (139, 201, 194)
    hex_color = '#%02x%02x%02x' % rgb_color # translation in hexa
    window.configure(bg=hex_color)

    title_frame = tk.Frame(window)
    title_frame.pack(pady=4)

    # Title création
    lbl_title = tk.Label(title_frame, text="TRAINING : AFFICHAGE", font=("Arial", 15))
    lbl_title.pack()

    filterframe = tk.Frame(window)
    filterframe.pack(pady=20)

    top_side_frame = tk.Frame(filterframe)
    top_side_frame.pack(side=TOP,pady=5)
    bottom_side_frame = tk.Frame(filterframe)
    bottom_side_frame.pack(side=LEFT,pady=5)

    pseudo_frame = tk.Frame(top_side_frame)
    pseudo_frame.pack(side=LEFT)
    pseudo_label = tk.Label(pseudo_frame, text="Pseudo:")
    pseudo_label.pack(side=LEFT)
    pseudo_entry = tk.Entry(pseudo_frame)
    pseudo_entry.pack(padx=20)


    exercice_frame = tk.Frame(top_side_frame)
    exercice_frame.pack(side=LEFT)
    exercice_label = tk.Label(exercice_frame, text="Exercice:")
    exercice_label.pack(side=LEFT)
    exercice_entry = tk.Entry(exercice_frame)
    exercice_entry.pack(padx=25)

    start_date_frame = tk.Frame(top_side_frame)
    start_date_frame.pack(side=LEFT)
    start_date_label = tk.Label(start_date_frame, text="Date début:")
    start_date_label.pack(side=LEFT)
    start_date_entry = tk.Entry(start_date_frame)
    start_date_entry.pack(padx=25)

    ends_date_frame = tk.Frame(top_side_frame)
    ends_date_frame.pack(side=LEFT)
    ends_date_label = tk.Label(ends_date_frame, text="Date fin:")
    ends_date_label.pack(side=LEFT)
    ends_date_entry = tk.Entry(ends_date_frame)
    ends_date_entry.pack()

    list_of_results_frame = tk.Frame(window)
    list_of_results_frame.pack()

    total_of_results_frame = tk.Frame(window)
    total_of_results_frame.pack(pady=35)

    total_top_side_frame = tk.Frame(total_of_results_frame)
    total_top_side_frame.pack()

    nb_lignes_label = tk.Label(total_top_side_frame, text="NbLignes\n12")
    nb_lignes_label.pack(side=LEFT, padx=25)

    temps_total_label = tk.Label(total_top_side_frame, text="Temps total\n0:06:15")
    temps_total_label.pack(side=LEFT, padx=25)

    nb_ok_label = tk.Label(total_top_side_frame, text="Nb OK\n8")
    nb_ok_label.pack(side=LEFT, padx=25)

    nb_total_label = tk.Label(total_top_side_frame, text="Nb Total\n15")
    nb_total_label.pack(side=LEFT, padx=25)

    poucentage_total_label = tk.Label(total_top_side_frame, text="% Total\n 25")
    poucentage_total_label.pack(side=LEFT, padx=25)

    mise_en_page_frame = tk.Frame(total_top_side_frame, width=295, height=50)
    mise_en_page_frame.pack(side=RIGHT, padx=25)

    results_button_frame = tk.Frame(bottom_side_frame)
    results_button_frame.pack()

    button_results = tk.Button(results_button_frame, text="Voir résultats")
    button_results.pack()
    button_results.bind("<Button-1>", lambda e: display_tuple_in_table((top_label_list + data_list)))

    #display()

    # main loop
    window.mainloop()


results()