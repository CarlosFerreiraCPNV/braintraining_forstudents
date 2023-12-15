"""
Auteur : Carlos Ferreira
Date : 27.11.2023
Projet : Brain training for students
Description : Côté DB
"""

# IMPORTATIONS
import mysql.connector


# Retourne le nécessaire pour ce connecter à une DB avec python
def open_db():
    return mysql.connector.connect(host='127.0.0.1', port='3306',user='root', password='', database='training',buffered=True, autocommit=True)

# Lancement de la connection
db_connection = open_db()

# Sauve les informations quand on fini un exercice
def save_game_info(nickname, exercises, dates, duration, nb_of_right_answers, total_answers, percentage):
    query = "INSERT INTO results (nickname, exercises, dates, duration, nb_of_right_answers, total_answers, percentage) values (%s,%s,%s,%s,%s,%s,%s)"
    cursor = db_connection.cursor()
    cursor.execute(query, (nickname, exercices, dates, duration, nb_of_right_answers, total_answers, percentage,))
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


def delete_element_on_result_list_by_id(id_for_where):
    query = "DELETE FROM results WHERE results.id = %s"
    cursor = db_connection.cursor()
    cursor.execute(query, (id_for_where,))
    id = cursor.lastrowid
    cursor.close()
    print("delete")
    return id


def insert_into_db_from_list_of_data(nickname, exercices, dates, duration, nb_of_right_answers, total_answers, percentage):
    query = "INSERT INTO results (nickname, exercises, dates, duration, nb_of_right_answers, total_answers, percentage) values (%s,%s,%s,%s,%s,%s,%s)"
    cursor = db_connection.cursor()
    cursor.execute(query, (nickname, exercices, dates, duration, nb_of_right_answers, total_answers, percentage,))
    id = cursor.lastrowid
    cursor.close()
    print("insert")
    return id


def get_info_by_id(index):
    query = "SELECT results.nickname, results.exercises, results.dates, results.duration, results.nb_of_right_answers, results.total_answers FROM results WHERE results.id = %s"
    cursor = db_connection.cursor()
    cursor.execute(query, (index,))
    data = cursor.fetchone()
    cursor.close()
    return data


def modify_results(nickname, exercices, dates, duration, nb_of_right_answers, total_answers, percentage, index):
    query = "UPDATE results SET results.nickname = %s, results.exercises = %s, results.dates = %s, results.duration = %s, results.nb_of_right_answers = %s, results.total_answers = %s, results.percentage = %s WHERE results.id = %s"
    cursor = db_connection.cursor()
    cursor.execute(query, (nickname, exercices, dates, duration, nb_of_right_answers, total_answers, percentage, index))
    id = cursor.lastrowid
    cursor.close()
    return id


def get_total_of_nb_of_lines():
    query = "SELECT COUNT(results.id) FROM results"
    cursor = db_connection.cursor()
    cursor.execute(query)
    total_of_nb_of_lines = cursor.fetchone()
    cursor.close()
    return total_of_nb_of_lines[0]

def get_total_time():
    query = "SELECT SEC_TO_TIME(SUM(time_to_sec(results.duration))) As timeSum FROM results"
    cursor = db_connection.cursor()
    cursor.execute(query)
    total_time = cursor.fetchone()
    cursor.close()
    return total_time[0]

def get_total_nb_ok():
    query = "SELECT SUM(results.nb_of_right_answers) FROM results"
    cursor = db_connection.cursor()
    cursor.execute(query)
    total_nb_ok = cursor.fetchone()
    cursor.close()
    return total_nb_ok[0]

def get_total_nb_total():
    query = "SELECT SUM(results.total_answers) FROM results"
    cursor = db_connection.cursor()
    cursor.execute(query)
    total_nb_total = cursor.fetchone()
    cursor.close()
    return total_nb_total[0]