import tkinter as tk
from tkinter import *
from tkinter import ttk, messagebox
#from register import create_window_register


#________________WINDOW INSERT TO DB________________#
# Sert à créer une interface pour inserer un nouveau résultat
def create_window_login():
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

        # register d'un compte
        def button_event_register():
            global pseudo_for_verification
            # récupere les informations
            pseudo = pseudo_entry_register.get()
            password = password_entry_register.get()

            # S'il n'y a pas de pseudo afficher une alerte sinon continuer le processus
            if len(pseudo) > 0:
                pseudo_for_verification = verify_user(pseudo)
            else:
                messagebox.showinfo("PSEUDO", "Veuillez entrer un pseudo !")

            # S'il n'y a pas de mot de passe afficher une alerte sinon continuer le processus
            if len(password) <= 0:
                messagebox.showinfo("PASSWORD", "Veuillez entrer un mot de passe !")
            else:
                # Si le pseudo n'existe pas dans la db créer le compte sinon afficher une erreur
                if pseudo_for_verification == None:
                    # insertion dans la db
                    create_user(pseudo, password)

                    # Activation des boutons et entrys
                    submit_button.config(state='normal')
                    register_button.config(state='normal')
                    username_entry.config(state='normal')
                    password_entry.config(state='normal')

                    # détruit la fenetre de create
                    window.destroy()
                else:
                    messagebox.showinfo("ERREUR", "Le pseudo existe déjà !\nVeuillez choisir un autre pseudo.")

        ##########################################

        space_frame_register = tk.Frame(window)
        space_frame_register.pack(pady=10)

        # Mise en page
        center_frame_register = tk.Frame(window)
        center_frame_register.pack()

        title_frame_register = tk.Frame(center_frame_register)
        title_frame_register.pack()

        title_label_register = tk.Label(title_frame_register, text="Informations pour s'enregistrer :")
        title_label_register.pack()

        """
        [------------Pseudo------------]
        """

        pseudo_frame_register = tk.Frame(center_frame_register)
        pseudo_frame_register.pack(pady=5)

        pseudo_label_register = tk.Label(pseudo_frame_register, text="Pseudo :")
        pseudo_label_register.pack()

        pseudo_entry_register = tk.Entry(pseudo_frame_register)
        pseudo_entry_register.pack()

        """
        [------------Exercice------------]
        """

        password_frame_register = tk.Frame(center_frame_register)
        password_frame_register.pack(pady=5)

        password_label_register = tk.Label(password_frame_register, text="Mot de passe :")
        password_label_register.pack()

        password_entry_register = tk.Entry(password_frame_register)
        password_entry_register.pack()

        space_frame2_register = tk.Frame(window)
        space_frame2_register.pack(pady=5)

        submit_frame_register = tk.Frame(window)
        submit_frame_register.pack()

        submit_button_register = tk.Button(submit_frame_register, text="Submit", command=button_event_register)
        submit_button_register.pack(side=LEFT)

        # Demande à l'utilisateur s'il veut vraiment fermer la fênetre
        def on_closing():
            if messagebox.askokcancel("Attention",
                                      "Voulez-vous vraiment quitter ?\nLa connection à votre compte ne sera pas établi !"):

                # Activation des boutons et entrys
                submit_button.config(state='normal')
                register_button.config(state='normal')
                username_entry.config(state='normal')
                password_entry.config(state='normal')
                # Détruit la fenetre
                window.destroy()


        window.protocol("WM_DELETE_WINDOW", on_closing)

        # lancement infini de la fênetre
        window.mainloop()

        ###########################################

    # Désactive tous les autres boutons et entry pour pas qu'on puisse faire d'autres changements


    # Création de la fênetre
    window = tk.Tk()
    window.title("Affichage braintraining")
    # Centre la fenetre au milieu de l'écran
    w = 400
    h = 400
    screen_W = window.winfo_screenwidth()
    screen_H = window.winfo_screenheight()
    x = (screen_W / 2) - (w / 2)
    y = (screen_H / 2) - (h / 2)
    window.geometry("%dx%d+%d+%d" % (w, h, x, y))

    # color définition
    rgb_color = (139, 201, 194)
    hex_color = '#%02x%02x%02x' % rgb_color  # translation in hexa
    window.configure(bg=hex_color)

    # login d'un compte
    def button_event_login():
        # récupere les informations
        username = username_entry.get()
        password = password_entry.get()

        username_for_verify = verify_user(username)
        password_for_verify = verify_password(username)

        # Si le pseudo n'existe pas afficher une erreur sinon continuer le processus
        if username_for_verify == None:
            messagebox.showinfo("PSEUDO", "Votre pseudo n'existe pas!\nVérifier l'écriture de votre pseudo, si dans le cas contraire vous n'avez pas de compte veuillez en créer un en cliquant sur le bouton 'Register'.")
        else:
            # Si le mdp est pareil que celui qui est dans la db faire la connection sinon afficher un message d'erreur
            if password_for_verify == password:
                print("=")
                # détruit la fenetre de create
                window.destroy()
            else:
                messagebox.showinfo("PASSWORD", "Votre mot de passe est incorrect !")

    ##########################################

    space_frame = tk.Frame(window)
    space_frame.pack(pady=10)

    # Mise en page
    center_frame = tk.Frame(window)
    center_frame.pack()

    title_frame = tk.Frame(center_frame)
    title_frame.pack()

    title_label = tk.Label(title_frame, text="Informations nécessaires \npour se connecter  :")
    title_label.pack()

    """
    [------------Username------------]
    """

    username_frame = tk.Frame(center_frame)
    username_frame.pack(pady=5)

    username_label = tk.Label(username_frame, text="Pseudo :")
    username_label.pack()

    username_entry = tk.Entry(username_frame)
    username_entry.pack()

    """
    [------------Password------------]
    """

    password_frame = tk.Frame(center_frame)
    password_frame.pack(pady=5)

    password_label = tk.Label(password_frame, text="Mot de passe :")
    password_label.pack()

    password_entry = tk.Entry(password_frame)
    password_entry.pack()

    space_frame2 = tk.Frame(window)
    space_frame2.pack(pady=5)

    submit_frame = tk.Frame(window)
    submit_frame.pack()

    submit_button = tk.Button(submit_frame, text="Submit", command=button_event_login)
    submit_button.pack(side=LEFT)

    def register():
        # désactivation
        username_entry.config(state='disabled')
        password_entry.config(state='disabled')
        submit_button.config(state='disabled')
        register_button.config(state='disabled')
        # lance la fenetre de création d'utilisateur
        create_window_register()

    register_frame = tk.Frame(window)
    register_frame.pack()

    register_button = tk.Button(register_frame, text="Register", command=register)
    register_button.pack(side=LEFT)


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


create_window_login()
