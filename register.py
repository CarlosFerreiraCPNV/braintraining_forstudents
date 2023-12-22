import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox

#________________WINDOW INSERT TO DB________________#
# Sert à créer une interface pour inserer un nouveau résultat
def create_window_register():
    # Désactive tous les autres boutons et entry pour pas qu'on puisse faire d'autres changements


    # Création de la fênetre
    window = tk.Tk()
    window.title("Affichage braintraining")
    # Centre la fenetre au milieu de l'écran
    w = 200
    h = 200
    screen_W = window.winfo_screenwidth()
    screen_H = window.winfo_screenheight()
    x = (screen_W / 2) - (w / 2)
    y = (screen_H / 2) - (h / 2)
    window.geometry("%dx%d+%d+%d" % (w, h, x, y))

    # color définition
    rgb_color = (139, 201, 194)
    hex_color = '#%02x%02x%02x' % rgb_color  # translation in hexa
    window.configure(bg=hex_color)

    # insert informations on DB
    def button_event():
        # récupere les informations
        pseudo = pseudo_entry.get()
        exercise = exercise_entry.get()
        date = date_entry.get()
        time = time_entry.get()
        nbsuccess = NbOk_entry.get()
        nbtrials = NbTotal_entry.get()
        percentage = (int(nbsuccess) * 100) / int(nbtrials)

        # insertion dans la db
        create_user(pseudo, exercise, date, time, nbsuccess, nbtrials, percentage)
        # reload l'affichage
        display_tuple_in_table((top_label_list + apply_filters()))

        # détruit la fenetre de create
        window.destroy()
        # Active les entrys et boutons


    ##########################################

    space_frame = tk.Frame(window)
    space_frame.pack(pady=10)

    # Mise en page
    center_frame = tk.Frame(window)
    center_frame.pack()

    title_frame = tk.Frame(center_frame)
    title_frame.pack()

    title_label = tk.Label(title_frame, text="Informations pour s'enregistrer :")
    title_label.pack()

    """
    [------------Pseudo------------]
    """

    pseudo_frame = tk.Frame(center_frame)
    pseudo_frame.pack(pady=5)

    pseudo_label = tk.Label(pseudo_frame, text="Pseudo :")
    pseudo_label.pack()

    pseudo_entry = tk.Entry(pseudo_frame)
    pseudo_entry.pack()

    """
    [------------Exercice------------]
    """

    exercice_frame = tk.Frame(center_frame)
    exercice_frame.pack(pady=5)

    exercise_label = tk.Label(exercice_frame, text="Mot de passe :")
    exercise_label.pack()

    exercise_entry = tk.Entry(exercice_frame)
    exercise_entry.pack()

    space_frame2 = tk.Frame(window)
    space_frame2.pack(pady=5)

    submit_frame = tk.Frame(window)
    submit_frame.pack()

    submit_button = tk.Button(submit_frame, text="Submit")
    submit_button.pack(side=LEFT)


    # Demande à l'utilisateur s'il veut vraiment fermer la fênetre
    def on_closing():
        if messagebox.askokcancel("Attention", "Voulez-vous vraiment quitter ?\nLa création du nouveau résultat ne sera pas prise en compte !"):
            # Détruit la fenetre
            window.destroy()
            # Activation des boutons et entrys


    window.protocol("WM_DELETE_WINDOW", on_closing)

    # lancement infini de la fênetre
    window.mainloop()

    ###########################################
