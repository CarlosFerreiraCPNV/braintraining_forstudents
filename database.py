"""
Auteur : Carlos Ferreira
Date : 15.12.2023
Projet : Brain training for students
Description : Côté DB
"""

# IMPORTATIONS
import mysql.connector


# Retourne le nécessaire pour ce connecter à une DB avec python
def open_db():
    return mysql.connector.connect(host='127.0.0.1', port='3306', user='root', password='', database='training', buffered=True, autocommit=True)

# Lancement de la connection
db_connection = open_db()

# Sauve les informations quand on fini un exercice
def save_game_info(nickname, exercises, dates, duration, nb_of_right_answers, total_answers, percentage):
    query = "INSERT INTO results (nickname, exercises, dates, duration, nb_of_right_answers, total_answers, percentage) values (%s,%s,%s,%s,%s,%s,%s)"
    cursor = db_connection.cursor()
    cursor.execute(query, (nickname, exercises, dates, duration, nb_of_right_answers, total_answers, percentage,))
    row_id = cursor.lastrowid
    cursor.close()
    return row_id


# Prends les informations de la db pour en faire une liste de resultats
def get_data_for_result_list(select_variable):
    query = select_variable
    cursor = db_connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return data


# Supprime une ligne de la DB en fonction du id donné
def delete_element_on_result_list_by_id(id_for_where):
    query = "DELETE FROM results WHERE results.id = %s"
    cursor = db_connection.cursor()
    cursor.execute(query, (id_for_where,))
    id = cursor.lastrowid
    cursor.close()
    print("delete")
    return id


# Insert les informations donné dans la DB
def insert_into_db_from_list_of_data(nickname, exercises, dates, duration, nb_of_right_answers, total_answers, percentage):
    query = "INSERT INTO results (nickname, exercises, dates, duration, nb_of_right_answers, total_answers, percentage) values (%s,%s,%s,%s,%s,%s,%s)"
    cursor = db_connection.cursor()
    cursor.execute(query, (nickname, exercises, dates, duration, nb_of_right_answers, total_answers, percentage,))
    id = cursor.lastrowid
    cursor.close()
    print("insert")
    return id


# Donne les informations de la ligne appartir d'un id donné
def get_info_by_id(index):
    query = "SELECT results.nickname, results.exercises, results.dates, results.duration, results.nb_of_right_answers, results.total_answers FROM results WHERE results.id = %s"
    cursor = db_connection.cursor()
    cursor.execute(query, (index,))
    data = cursor.fetchone()
    cursor.close()
    return data


# Modifie la ligne du résultat en fonction du id donné
def modify_results(nickname, exercises, dates, duration, nb_of_right_answers, total_answers, percentage, index):
    query = "UPDATE results SET results.nickname = %s, results.exercises = %s, results.dates = %s, results.duration = %s, results.nb_of_right_answers = %s, results.total_answers = %s, results.percentage = %s WHERE results.id = %s"
    cursor = db_connection.cursor()
    cursor.execute(query, (nickname, exercises, dates, duration, nb_of_right_answers, total_answers, percentage, index))
    id = cursor.lastrowid
    cursor.close()
    return id


# Donne les informations du nombre de lignes de résultats
def get_total_of_nb_of_lines():
    query = "SELECT COUNT(results.id) FROM results"
    cursor = db_connection.cursor()
    cursor.execute(query)
    total_of_nb_of_lines = cursor.fetchone()
    cursor.close()
    return total_of_nb_of_lines[0]


# Donne les informations du temps total de tous les résultats
def get_total_time():
    query = "SELECT SEC_TO_TIME(SUM(time_to_sec(results.duration))) As timeSum FROM results"
    cursor = db_connection.cursor()
    cursor.execute(query)
    total_time = cursor.fetchone()
    cursor.close()
    return total_time[0]


# Donne les informations du nombre Ok de tous les résultats
def get_total_nb_ok():
    query = "SELECT SUM(results.nb_of_right_answers) FROM results"
    cursor = db_connection.cursor()
    cursor.execute(query)
    total_nb_ok = cursor.fetchone()
    cursor.close()
    return total_nb_ok[0]


# Donne les informations du nombre Total de tous les résultats
def get_total_nb_total():
    query = "SELECT SUM(results.total_answers) FROM results"
    cursor = db_connection.cursor()
    cursor.execute(query)
    total_nb_total = cursor.fetchone()
    cursor.close()
    return total_nb_total[0]


def create_user(nickname, password, permission_level):
    query = "INSERT INTO users (nickname, password, permission_level) values (%s,%s,%s)"
    cursor = db_connection.cursor()
    cursor.execute(query, (nickname, password, permission_level))
    lastrowid = cursor.lastrowid
    cursor.close()
    return lastrowid


def verify_user(nickname):
    query = "SELECT users.nickname FROM users WHERE users.nickname = %s"
    cursor = db_connection.cursor()
    cursor.execute(query, (nickname,))
    nickname_var = cursor.fetchone()
    cursor.close()
    print(nickname_var)
    return nickname_var


def get_password_by_nickname(nickname):
    query = "SELECT users.password FROM users WHERE users.nickname = %s"
    cursor = db_connection.cursor()
    cursor.execute(query, (nickname,))
    nickname_var = cursor.fetchone()
    cursor.close()
    return nickname_var[0]


# Sert à avoir le niveau de permission via le pseudo et le mdp
def get_permission_level_from_nickname_and_password(nickname, password):
    query = "SELECT users.permission_level FROM users WHERE users.nickname = %s AND users.password = %s"
    cursor = db_connection.cursor()
    cursor.execute(query, (nickname, password))
    permission_level = cursor.fetchone()
    cursor.close()
    return permission_level[0]


# Sert à avoir le niveau de permissions via le pseudo
def get_permission_level_from_nickname(nickname):
    query = "SELECT users.permission_level FROM users WHERE users.nickname = %s"
    cursor = db_connection.cursor()
    cursor.execute(query, (nickname,))
    permission_level = cursor.fetchone()
    cursor.close()
    return permission_level[0]


def change_permission_level(nickname):
    query = "UPDATE users SET users.permission_level = 2 WHERE users.nickname = %s"
    cursor = db_connection.cursor()
    cursor.execute(query, (nickname,))
    lastrowid = cursor.lastrowid
    cursor.close()
    return lastrowid