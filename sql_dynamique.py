# Exemple de requête sql dynamique
# JCY oct 23
# PRO DB PY

import tkinter as tk

window = tk.Tk()
window.title("Affichage braintraining")
window.geometry("1100x900")

#prend les 4 paramètres et génère une requête spéciale
def sql_generate(e):
    sql_base="SELECT * from results"
    pseudo=entry_pseudo.get()
    exercise=entry_ex.get()
    date_start=entry_date_start.get()
    date_end=entry_date_end.get()
    sql_base = sql_base + sql_dynamic2(pseudo,exercise, date_start, date_end)
    txt_sql.delete("1.0","end")
    txt_sql.insert("1.0",sql_base)

#génère la fin de la requête dynamiquement
def sql_dynamic(p,e,ds,de):
    sql_add="\n where 1=1 "
    if (p!=""):
        sql_add += "\n and pseudo ='" + str(p) + "'"
    if (e!=""):
        sql_add += "\n and exercise ='" + str(e) + "'"
    if (ds!=""):
        sql_add += "\n and start_date >='" + str(ds) + "'"
    if (de!=""):
        sql_add += "\n and start_date <='" + str(de) + "'"
    return sql_add

#génère la fin de la requête dynamiquement
def sql_dynamic2(p,e,ds,de):
    sql_add=""
    i=0
    if (p!=""):
        sql_add += "\n where pseudo ='" + str(p) + "'"
        i+=1

    if (e!=""):
        if (i>0):
            sql_add += "\n and exercise ='" + str(e) + "'"
        else :
            sql_add += "\n where exercise ='" + str(e) + "'"
        i+=1

    if (ds!=""):
        if (i>0):
            sql_add += "\n and start_date >='" + str(ds) + "'"
        else:
            sql_add += "\n where start_date >='" + str(ds) + "'"
        i+=1

    if (de!=""):
        if (i>0):
            sql_add += "\n and start_date <='" + str(de) + "'"
        else:
            sql_add += "\n where start_date <='" + str(de) + "'"
    return sql_add


# Title création
lbl_title = tk.Label(window, text="exemple requête", font=("Arial", 15))
lbl_title.grid(row=0, column=0,ipady=5, padx=40,pady=40, columnspan=8)

lbl_pseudo =tk.Label(window, text="pseudo:", font=("Arial", 8)).grid(row=1,column=0,sticky="E")
entry_pseudo=tk.Entry(window,font=("Arial", 8))
entry_pseudo.insert(0, "Gaston")
entry_pseudo.grid(row=1,column=1,sticky="W")

lbl_ex =tk.Label(window, text="exercise:", font=("Arial", 8)).grid(row=1,column=2,sticky="E")
entry_ex=tk.Entry(window,font=("Arial", 8))
entry_ex.insert(0, "GEO01")
entry_ex.grid(row=1,column=3,sticky="W")

lbl_date_start =tk.Label(window, text="date début:", font=("Arial", 8)).grid(row=1,column=4,sticky="E" )
entry_date_start=tk.Entry(window,font=("Arial", 8))
entry_date_start.insert(0, "2023-12-01")
entry_date_start.grid(row=1,column=5,sticky="W")

lbl_date_end =tk.Label(window, text="date fin:", font=("Arial", 8)).grid(row=1,column=6,sticky="E")
entry_date_end=tk.Entry(window,font=("Arial", 8),bg="white")
entry_date_end.insert(0, "2023-12-01")
entry_date_end.grid(row=1,column=7,sticky="W")

btn_display = tk.Button(window, text="Affiche", font=("Arial", 10))
btn_display.grid(row=2, column=0, padx=2, pady=2)
btn_display.bind("<Button-1>", sql_generate)

txt_sql = tk.Text(window,  font=("Arial", 15),bg="white")
txt_sql.insert("1.0", "Voici la requête")
txt_sql.grid(row=3, column=1,ipady=5, padx=40,pady=40,columnspan=8)





# main loop
window.mainloop()
