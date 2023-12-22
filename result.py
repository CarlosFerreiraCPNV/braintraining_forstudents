"""
Auteur : Carlos Ferreira
Date : 15.12.2023
Projet : Brain training for students
"""
import datetime
import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
from database import *

# Variables
top_label_list = [("ID", "Elève", "Exercice", "Date", "Temps", "Nb Ok", "Nb Total", "% Total")]
top_label_result_list = [("NbLignes", "Temps total", "Nb OK", "Nb Total", "% Total")]

# Fonction qui sert à vérifier le type de données il y a dans un entry
def check_type(val) :
    global check_type_var
    # Essaye de transformer en int
    try:
        int(val)
        check_type_var = True
    # S'il arrive pas mettre la variable en false
    except ValueError:
        check_type_var = False
    return check_type_var

# call other windows (exercices)
def results():
    global exercice, pseudo, filter_variable

    # Sert à reload l'affichage
    def display_tuple_in_table(mytuple):
        global exercice, pseudo, filter_variable, info_label, top_label_result_list

        # Informations nécessaires à afficher
        total_of_nb_of_lines = (get_total_of_nb_of_lines())
        total_time = (get_total_time())
        total_nb_ok = (get_total_nb_ok())
        total_nb_total = (get_total_nb_total())
        percentage = round((total_nb_ok * 100) / total_nb_total)

        list_total = [("delete")]

        list_total.append(total_of_nb_of_lines)
        list_total.append(total_time)
        list_total.append(total_nb_ok)
        list_total.append(total_nb_total)
        list_total.append(percentage)
        list_total.remove("delete")

        list_total_for_append = tuple(list_total)

        top_label_result_list.append(list_total_for_append)

        display_total_of_results(top_label_result_list)

        # Création du tableau pour l'affichage
        for line in range(0, len(mytuple)):
            for col in range(0, len(mytuple[line])):
                info_label = tk.Label(list_of_results_frame, text=mytuple[line][col], width=14, font=("Arial", 10))
                info_label.grid(row=line,column=col,padx=2,pady=2, sticky='w')

            # Ceci sert à mettre afficher au lieu d'un chiffre un rectangle qui change de taille et de couleur en fonction du pourcent qui lui est attribué
            if line > 0:
                info_label.config(text="")
                widht_color = round(mytuple[line][7] / 10)
                if mytuple[line][7] <= 25:
                    info_label.config(bg="red", width=widht_color, padx=10)
                if mytuple[line][7] > 25 and mytuple[line][6] < 75:
                    info_label.config(bg="orange", width=widht_color, padx=10)
                if mytuple[line][7] >= 75:
                    info_label.config(bg="green", width=widht_color, padx=10)

    # Prend les 4 paramètres et génère une requête spéciale
    def sql_generate():
        sql_base = "SELECT * from results"
        pseudo = pseudo_entry.get()
        exercise = exercice_entry.get()
        date_start = start_date_entry.get()
        date_end = ends_date_entry.get()

        # S'il n'y a une date dans le champ on vas la transformer et ajouter un jour pour qu'il affiche les bonnes dates
        if date_end == "":
            print("pas de date")
        else:
            date_convert = datetime.datetime.strptime(date_end, "%Y-%m-%d")
            date_convert = date_convert + datetime.timedelta(days=1)
            print(date_convert)

            date = str(date_convert)
            date_split = date.split()

            date_end = date_split[0]
            print(date_end)
        sql_base = sql_base + sql_dynamic(pseudo, exercise, date_start, date_end)
        print(sql_base)
        return sql_base

    # Génère la fin de la requête dynamiquement
    def sql_dynamic(p, e, ds, de):
        sql_add = "\n where 1=1 "
        if (p != ""):
            sql_add += "\n and results.nickname ='" + str(p) + "'"
        if (e != ""):
            sql_add += "\n and results.exercises ='" + str(e) + "'"
        if (ds != ""):
            sql_add += "\n and results.dates >='" + str(ds) + "'"
        if (de != ""):
            sql_add += "\n and results.dates <='" + str(de) + "'" + "ORDER BY results.dates ASC"
        return sql_add

    # Supprime les informations qu'il y a dans une frame
    def clear():
        for widget in list_of_results_frame.winfo_children():
            widget.grid_forget()

    # Applique les filtres
    def apply_filters():
        global exercice, pseudo, filter_variable
        clear()
        filter_variable = [()]
        filter_variable = sql_generate()
        list_of_results = get_data_for_result_list(filter_variable)
        return list_of_results

    # Sert à supprimer une ligne en fonction de l'id donné
    def button_delete_action():
        if delete_entry.get() == "":
            print("Vide")
            messagebox.showinfo("Erreur", "Veuillez entrer un chiffre !")
        else:
            delete_id = delete_entry.get()
            delete_element_on_result_list_by_id(delete_id)
            display_tuple_in_table((top_label_list + apply_filters()))

    # Sert à afficher les resultats totaux
    def display_total_of_results(mytuple):
        global total_label
        # Création du tableau pour l'affichage
        for line in range(0, len(mytuple)):
            for col in range(0, len(mytuple[line])):
                total_label = tk.Label(total_of_results_frame, text=mytuple[line][col], width=14, font=("Arial", 10))
                total_label.grid(row=line, column=col, padx=2, pady=2)

            # Ceci sert à mettre afficher au lieu d'un chiffre un rectangle qui change de taille et de couleur en fonction du pourcent qui lui est attribué
            if line > 0:
                total_label.config(text="")
                widht_color = round(mytuple[line][4] / 10)
                if mytuple[1][4] <= 25:
                    total_label.config(bg="red", width=widht_color, padx=10)
                if mytuple[1][4] > 25 and mytuple[1][4] < 75:
                    total_label.config(bg="orange", width=widht_color, padx=10)
                if mytuple[1][4] >= 75:
                    total_label.config(bg="green", width=widht_color, padx=10)

    #________________WINDOW INSERT TO DB________________#
    # Sert à créer une interface pour inserer un nouveau résultat
    def create_window():
        # Désactive tous les autres boutons et entry pour pas qu'on puisse faire d'autres changements
        modify_entry.config(state='disabled')
        modify_button.config(state='disabled')
        delete_button.config(state='disabled')
        delete_entry.config(state='disabled')
        create_button.config(state='disabled')

        # Création de la fênetre
        window = tk.Tk()
        window.title("Affichage braintraining")
        # Centre la fenetre au milieu de l'écran
        w = 600
        h = 600
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
            insert_into_db_from_list_of_data(pseudo, exercise, date, time, nbsuccess, nbtrials, percentage)
            # reload l'affichage
            display_tuple_in_table((top_label_list + apply_filters()))

            # détruit la fenetre de create
            window.destroy()
            # Active les entrys et boutons
            modify_entry.config(state="normal")
            modify_button.config(state="normal")
            delete_button.config(state='normal')
            delete_entry.config(state='normal')
            create_button.config(state='normal')

        ##########################################

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

        exercise_entry = tk.ttk.Combobox(exercice_frame, values=["GEO01", "INFO02", "INFO05"], width=15, state='readonly')
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

        # Demande à l'utilisateur s'il veut vraiment fermer la fênetre
        def on_closing():
            if messagebox.askokcancel("Attention", "Voulez-vous vraiment quitter ?\nLa création du nouveau résultat ne sera pas prise en compte !"):
                # Détruit la fenetre
                window.destroy()
                # Activation des boutons et entrys
                modify_entry.config(state="normal")
                modify_button.config(state="normal")
                delete_button.config(state='normal')
                delete_entry.config(state='normal')
                create_button.config(state='normal')

        window.protocol("WM_DELETE_WINDOW", on_closing)

        # lancement infini de la fênetre
        window.mainloop()

        ###########################################

    # ________________Modify informations________________#
    # Création de l'interface pour modifier les informations d'un résultat
    def modify_window():
        # vérifie que l'entré est un int
        check_entry = check_type(modify_entry.get())
        if check_entry == True:
            # Si c'est vide afficher une erreur
            if modify_entry.get() == "":
                print("vide")
                messagebox.showinfo("Erreur", "Veuillez entrer un chiffre !")
            else:
                # Essaye d'afficher la fenetre
                try:
                    if int(modify_entry.get()) > 0:
                        index = modify_entry.get()
                        info_var = get_info_by_id(index)
                        pseudo = info_var[0]
                        exercises = info_var[1]
                        date = info_var[2]
                        duration = info_var[3]
                        nbsuccess = info_var[4]
                        nbtrials = info_var[5]

                        # désactive les boutons et entrys
                        modify_entry.config(state='disabled')
                        modify_button.config(state='disabled')
                        delete_button.config(state='disabled')
                        delete_entry.config(state='disabled')
                        create_button.config(state='disabled')

                        # Création de la fênetre
                        window = tk.Tk()
                        window.title("Affichage braintraining")
                        # Centre la fenetre au milieu de l'écran
                        w = 600
                        h = 600
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
                            # recuperations d'informations requises
                            nickname = pseudo_entry.get()
                            exercises = exercise_entry.get()
                            date = date_entry.get()
                            time = time_entry.get()
                            nbsuccess = NbOk_entry.get()
                            nbtrials = NbTotal_entry.get()
                            percentage = (int(nbsuccess) * 100) / int(nbtrials)

                            # modifie les résultats dans la db
                            modify_results(nickname, exercises, date, time, nbsuccess, nbtrials, percentage, index)

                            # affiche les résultats
                            display_tuple_in_table((top_label_list + apply_filters()))

                            # détruit la fenetre
                            window.destroy()

                            # active les boutons et entrys
                            modify_entry.config(state='normal')
                            modify_button.config(state='normal')
                            delete_button.config(state='normal')
                            delete_entry.config(state='normal')
                            create_button.config(state='normal')

                        ################################################

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
                        pseudo_entry.config(state='disabled')

                        """
                        [------------Exercice------------]
                        """

                        exercice_frame = tk.Frame(center_frame)
                        exercice_frame.pack(pady=10)

                        exercise_label = tk.Label(exercice_frame, text="Exercice :")
                        exercise_label.pack(side=LEFT)

                        exercise_entry = tk.ttk.Combobox(exercice_frame, values=["GEO01", "INFO02", "INFO05"], width=15, state='readonly')
                        exercise_entry.insert(0, exercises)
                        exercise_entry.pack(side=LEFT)
                        exercise_entry.config(state='disabled')

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
                        date_entry.config(state='disabled')

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

                        # Demande à l'utilisateur s'il est sur de fermer la fenetre
                        def on_closing():
                            if messagebox.askokcancel("Attention", "Voulez-vous vraiment quitter ?\nVos modifications ne seront pas prises en compte !"):
                                # Supprime la fenetre de modification
                                window.destroy()
                                # Active les boutons
                                modify_entry.config(state="normal")
                                modify_button.config(state="normal")
                                delete_button.config(state='normal')
                                delete_entry.config(state='normal')
                                create_button.config(state='normal')

                        window.protocol("WM_DELETE_WINDOW", on_closing)

                        # lancement infini de la fênetre
                        window.mainloop()

                        #######################################
                    # Affiche un message d'erreur si le chiffre est 0 ou inferieur à 0
                    else:
                        messagebox.showinfo("Erreur", "Veuillez entrer un chiffre supérieur à 0 !")
                except:
                    print()
        # Affiche ce message si on à pas écrit un chiffre
        else:
            messagebox.showinfo("Erreur", "Veuillez entrer un chiffre !")

    # Main window
    window = tk.Tk()
    window.title("Affichage braintraining")
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

    title_frame = tk.Frame(window)
    title_frame.pack(pady=4)

    # Title création
    lbl_title = tk.Label(title_frame, text="TRAINING : AFFICHAGE", font=("Arial", 15))
    lbl_title.pack()

    ########################################################################
    ########################## Affichage Résultats #########################
    ########################################################################

    filterframe = tk.Frame(window)
    filterframe.pack(pady=20)

    top_side_frame = tk.Frame(filterframe)
    top_side_frame.pack(side=TOP,pady=5)
    bottom_side_frame = tk.Frame(filterframe)
    bottom_side_frame.pack(side=LEFT,pady=5)

    # Création de l'interface pour les filtres (pseudo)
    pseudo_frame = tk.Frame(top_side_frame)
    pseudo_frame.pack(side=LEFT)
    pseudo_label = tk.Label(pseudo_frame, text="Pseudo:")
    pseudo_label.pack(side=LEFT)
    pseudo_entry = tk.Entry(pseudo_frame)
    pseudo_entry.pack(padx=20)

    # Création de l'interface pour les filtres (exercice)
    exercice_frame = tk.Frame(top_side_frame)
    exercice_frame.pack(side=LEFT)
    exercice_label = tk.Label(exercice_frame, text="Exercice:")
    exercice_label.pack(side=LEFT)
    exercice_entry = tk.ttk.Combobox(exercice_frame, values=["", "GEO01", "INFO02", "INFO05"], state='readonly')
    exercice_entry.pack(padx=25)

    # Création de l'interface pour les filtres (start_date)
    start_date_frame = tk.Frame(top_side_frame)
    start_date_frame.pack(side=LEFT)
    start_date_label = tk.Label(start_date_frame, text="Date début:")
    start_date_label.pack(side=LEFT)
    start_date_entry = tk.Entry(start_date_frame)
    start_date_entry.pack(padx=25)

    # Création de l'interface pour les filtres (end_date)
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

    results_button_frame = tk.Frame(bottom_side_frame)
    results_button_frame.pack()

    # Bouton qui sert à afficher les résultats
    button_results = tk.Button(results_button_frame, text="Voir résultats")
    button_results.pack()
    button_results.bind("<Button-1>", lambda e: display_tuple_in_table((top_label_list + apply_filters())))

    ########################################################################
    ################################# CRUD #################################
    ########################################################################

    crud_frame = tk.Frame(window)
    crud_frame.pack()

    # Création de l'affichage CRUD (delete)
    delete_label = tk.Label(crud_frame, text="Supprimer l'id : ")
    delete_label.pack(side=LEFT, pady=10, padx=5)

    delete_entry = tk.Entry(crud_frame, width=5)
    delete_entry.pack(side=LEFT)

    delete_button = tk.Button(crud_frame, text="Supprimer")
    delete_button.pack(side=LEFT, padx=10)
    delete_button.bind("<Button-1>", lambda e: button_delete_action())

    # Création de l'affichage CRUD (create)
    create_button = tk.Button(crud_frame, text="Insérer un nouveau résultat", command=create_window)
    create_button.pack(side=LEFT, padx=10)

    # Création de l'affichage CRUD (modify)
    modify_label = tk.Label(crud_frame, text="Modifier le résultat de l'id :")
    modify_label.pack(side=LEFT, padx=10)

    modify_entry = tk.Entry(crud_frame, width=5)
    modify_entry.pack(side=LEFT)

    modify_button = tk.Button(crud_frame, text="Modifier", command=modify_window)
    modify_button.pack(side=LEFT, padx=10)

    # Demande à l'utilisateur s'il veut vraiment fermer la fênetre
    def on_closing():
        if messagebox.askokcancel("Attention", "Voulez-vous vraiment quitter ?"):
            # Clear la fenetre pour pas quand on re ouvre il y aie déjà des résultats affiché
            clear()
            window.destroy()

    window.protocol("WM_DELETE_WINDOW", on_closing)

    # main loop
    window.mainloop()
