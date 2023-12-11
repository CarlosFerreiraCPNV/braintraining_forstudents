"""
Auteur : Carlos Ferreira
Date : 27.11.2023
Projet : Brain training for students
"""

import tkinter as tk
from tkinter import *
from tkinter import ttk
from database import *

# TABLEAU DES VALEURS DU JEU
top_label_list = [("ID","Elève", "Exercice", "Date", "Temps", "Nb Ok", "Nb Total", "% Total")]
filters = 0
filter_variable = [()]


# call other windows (exercices)
def results():
    global filters, exercice, pseudo, filter_variable
    def display_tuple_in_table(mytuple):
        global filters, exercice, pseudo, filter_variable, info_label
        for line in range(0, len(mytuple)):
            for col in range(0, len(mytuple[line])):
                info_label = tk.Label(list_of_results_frame, text=mytuple[line][col], width=14, font=("Arial", 10))
                info_label.grid(row=line,column=col,padx=2,pady=2)

            if line > 0:
                info_label.config(text="")
                if mytuple[line][7] <= 25:
                    info_label.config(bg="red")
                if mytuple[line][7] > 25 and mytuple[line][6] < 75:
                    info_label.config(bg="orange")
                if mytuple[line][7] >= 75:
                    info_label.config(bg="green")

    # prend les 4 paramètres et génère une requête spéciale
    def sql_generate():
        sql_base = "SELECT * from results"
        pseudo = pseudo_entry.get()
        exercise = exercice_entry.get()
        date_start = start_date_entry.get()
        date_end = ends_date_entry.get()
        sql_base = sql_base + sql_dynamic(pseudo, exercise, date_start, date_end)
        print(sql_base)
        return sql_base

    # génère la fin de la requête dynamiquement
    def sql_dynamic(p, e, ds, de):
        sql_add = "\n where 1=1 "
        if (p != ""):
            sql_add += "\n and results.nickname ='" + str(p) + "'"
        if (e != ""):
            sql_add += "\n and results.exercises ='" + str(e) + "'"
        if (ds != ""):
            sql_add += "\n and results.dates >='" + str(ds) + "'"
        if (de != ""):
            sql_add += "\n and results.dates <='" + str(de) + "'"
        return sql_add


    def clear():
        for widget in list_of_results_frame.winfo_children():
            widget.grid_forget()

    def apply_filters():
        global filters, exercice, pseudo, filter_variable
        clear()
        filter_variable = [()]
        filter_variable = sql_generate()
        list_of_results = get_data_for_result_list(filter_variable)
        return list_of_results


    def button_delete_action():
        delete_id = delete_entry.get()
        delete_element_on_result_list_by_id(delete_id)
        display_tuple_in_table((top_label_list + apply_filters()))


    #________________INSERT TO DB________________#
    def create_window():
        # Création de la fênetre
        window = tk.Tk()
        window.title("Affichage braintraining")
        window.geometry("600x600")

        # color définition
        rgb_color = (139, 201, 194)
        hex_color = '#%02x%02x%02x' % rgb_color  # translation in hexa
        window.configure(bg=hex_color)

        # insert informations on DB
        def button_event():
            pseudo = pseudo_entry.get()
            exercise = exercise_entry.get()
            date = date_entry.get()
            time = time_entry.get()
            nbsuccess = NbOk_entry.get()
            nbtrials = NbTotal_entry.get()
            percentage = (int(nbsuccess) * 100) / int(nbtrials)
            insert_into_db_from_list_of_data(pseudo, exercise, date, time, nbsuccess, nbtrials, percentage)
            display_tuple_in_table((top_label_list + apply_filters()))
            window.destroy()

        space_frame = tk.Frame(window)
        space_frame.pack(pady=70)

        # Mise en page
        center_frame = tk.Frame(window)
        center_frame.pack()

        title_frame = tk.Frame(center_frame)
        title_frame.pack()

        title_label = tk.Label(title_frame, text="Informations à insérer :")
        title_label.pack()

        """
        [------------Pseudo------------]
        """

        pseudo_frame = tk.Frame(center_frame)
        pseudo_frame.pack(pady=10)

        pseudo_label = tk.Label(pseudo_frame, text="Pseudo :")
        pseudo_label.pack(side=LEFT)

        pseudo_entry = tk.Entry(pseudo_frame)
        pseudo_entry.pack(side=LEFT)

        """
        [------------Exercice------------]
        """

        exercice_frame = tk.Frame(center_frame)
        exercice_frame.pack(pady=10)

        exercise_label = tk.Label(exercice_frame, text="Exercice :")
        exercise_label.pack(side=LEFT)

        exercise_entry = tk.ttk.Combobox(exercice_frame, values=["GEO01", "INFO02", "INFO05"], width=15)
        exercise_entry.pack(side=LEFT)

        """
        [------------Date------------]
        """

        date_frame = tk.Frame(center_frame)
        date_frame.pack(pady=10)

        date_label = tk.Label(date_frame, text="Date :")
        date_label.pack(side=LEFT)

        date_entry = tk.Entry(date_frame)
        date_entry.pack(side=LEFT)

        """
        [------------Temps------------]
        """

        time_frame = tk.Frame(center_frame)
        time_frame.pack(pady=10)

        time_label = tk.Label(time_frame, text="Temps :")
        time_label.pack(side=LEFT)

        time_entry = tk.Entry(time_frame)
        time_entry.pack(side=LEFT)

        """
        [------------Nb Ok------------]
        """

        NbOk_frame = tk.Frame(center_frame)
        NbOk_frame.pack(pady=10)

        NbOk_label = tk.Label(NbOk_frame, text="Nb Ok :")
        NbOk_label.pack(side=LEFT)

        NbOk_entry = tk.Entry(NbOk_frame)
        NbOk_entry.pack(side=LEFT)

        """
        [------------Nb Total------------]
        """

        NbTotal_frame = tk.Frame(center_frame)
        NbTotal_frame.pack(pady=10)

        NbTotal_label = tk.Label(NbTotal_frame, text="Nb Total :")
        NbTotal_label.pack(side=LEFT)

        NbTotal_entry = tk.Entry(NbTotal_frame)
        NbTotal_entry.pack(side=LEFT)

        """
        [------------Submit Button------------]
        """
        submit_frame = tk.Frame(window, bg=hex_color)
        submit_frame.pack()

        submit_button = tk.Button(submit_frame, text="SUBMIT", command=button_event)
        submit_button.pack(pady=10)

        # lancement infini de la fênetre
        window.mainloop()

        ###########################################

    # ________________Modify informations________________#
    def modify_window():
        if int(modify_entry.get()) > 0:
            index = modify_entry.get()
            info_var = get_info_by_id(index)
            pseudo = info_var[0]
            exercises = info_var[1]
            date = info_var[2]
            duration = info_var[3]
            nbsuccess = info_var[4]
            nbtrials = info_var[5]
        else:
            print("veuillez entrer un chiffre supérieur à 0")

        # Création de la fênetre
        window = tk.Tk()
        window.title("Affichage braintraining")
        window.geometry("600x600")

        # color définition
        rgb_color = (139, 201, 194)
        hex_color = '#%02x%02x%02x' % rgb_color  # translation in hexa
        window.configure(bg=hex_color)

        # insert informations on DB
        def button_event():
            nickname = pseudo_entry.get()
            exercises = exercise_entry.get()
            date = date_entry.get()
            time = time_entry.get()
            nbsuccess = NbOk_entry.get()
            nbtrials = NbTotal_entry.get()
            percentage = (int(nbsuccess) * 100) / int(nbtrials)
            modify_results(nickname, exercises, date, time, nbsuccess, nbtrials, percentage, index)
            display_tuple_in_table((top_label_list + apply_filters()))
            window.destroy()

        space_frame = tk.Frame(window)
        space_frame.pack(pady=100)

        # Mise en page
        center_frame = tk.Frame(window)
        center_frame.pack()

        title_frame = tk.Frame(center_frame)
        title_frame.pack()

        title_label = tk.Label(title_frame, text="Informations qui peuvent être changé :")
        title_label.pack()

        """
        [------------Pseudo------------]
        """

        pseudo_frame = tk.Frame(center_frame)
        pseudo_frame.pack(pady=10)

        pseudo_label = tk.Label(pseudo_frame, text="Pseudo :")
        pseudo_label.pack(side=LEFT)

        pseudo_entry = tk.Entry(pseudo_frame)
        pseudo_entry.insert(0, pseudo)
        pseudo_entry.pack(side=LEFT)

        """
        [------------Exercice------------]
        """

        exercice_frame = tk.Frame(center_frame)
        exercice_frame.pack(pady=10)

        exercise_label = tk.Label(exercice_frame, text="Exercice :")
        exercise_label.pack(side=LEFT)

        exercise_entry = tk.ttk.Combobox(exercice_frame, values=["GEO01", "INFO02", "INFO05"], width=15)
        exercise_entry.insert(0, exercises)
        exercise_entry.pack(side=LEFT)

        """
        [------------Date------------]
        """

        date_frame = tk.Frame(center_frame)
        date_frame.pack(pady=10)

        date_label = tk.Label(date_frame, text="Date :")
        date_label.pack(side=LEFT)

        date_entry = tk.Entry(date_frame)
        date_entry.insert(0, date)
        date_entry.pack(side=LEFT)

        """
        [------------Temps------------]
        """

        time_frame = tk.Frame(center_frame)
        time_frame.pack(pady=10)

        time_label = tk.Label(time_frame, text="Temps :")
        time_label.pack(side=LEFT)

        time_entry = tk.Entry(time_frame)
        time_entry.insert(0, duration)
        time_entry.pack(side=LEFT)

        """
        [------------Nb Ok------------]
        """

        NbOk_frame = tk.Frame(center_frame)
        NbOk_frame.pack(pady=10)

        NbOk_label = tk.Label(NbOk_frame, text="Nb Ok :")
        NbOk_label.pack(side=LEFT)

        NbOk_entry = tk.Entry(NbOk_frame)
        NbOk_entry.insert(0, nbsuccess)
        NbOk_entry.pack(side=LEFT)

        """
        [------------Nb Total------------]
        """

        NbTotal_frame = tk.Frame(center_frame)
        NbTotal_frame.pack(pady=10)

        NbTotal_label = tk.Label(NbTotal_frame, text="Nb Total :")
        NbTotal_label.pack(side=LEFT)

        NbTotal_entry = tk.Entry(NbTotal_frame)
        NbTotal_entry.insert(0, nbtrials)
        NbTotal_entry.pack(side=LEFT)

        """
        [------------Submit Button------------]
        """
        submit_frame = tk.Frame(window, bg=hex_color)
        submit_frame.pack()

        submit_button = tk.Button(submit_frame, text="SUBMIT", command=button_event)
        submit_button.pack(pady=10)

        # lancement infini de la fênetre
        window.mainloop()

        #######################################

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
    exercice_entry = tk.ttk.Combobox(exercice_frame, values=["", "GEO01", "INFO02", "INFO05"])
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

    button_results.bind("<Button-1>", lambda e: display_tuple_in_table((top_label_list + apply_filters())))

    crud_frame = tk.Frame(window)
    crud_frame.pack()

    delete_label = tk.Label(crud_frame, text="Supprimer l'id : ")
    delete_label.pack(side=LEFT, pady=10, padx=5)

    delete_entry = tk.Entry(crud_frame, width=5)
    delete_entry.pack(side=LEFT)

    delete_button = tk.Button(crud_frame, text="Supprimer")
    delete_button.pack(side=LEFT, padx=10)

    delete_button.bind("<Button-1>", lambda e: button_delete_action())

    create_button = tk.Button(crud_frame, text="Insérer un nouveau résultat", command=create_window)
    create_button.pack(side=LEFT, padx=10)

    modify_label = tk.Label(crud_frame, text="Modifier le résultat de l'id :")
    modify_label.pack(side=LEFT, padx=10)

    modify_entry = tk.Entry(crud_frame, width=5)
    modify_entry.pack(side=LEFT)

    modify_button = tk.Button(crud_frame, text="Modifier", command=modify_window)
    modify_button.pack(side=LEFT, padx=10)

    # main loop
    window.mainloop()


results()