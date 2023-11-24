import mysql.connector


# Retourne le nécessaire pour ce connecter à une DB avec python
def open_db():
    return mysql.connector.connect(host='127.0.0.1', port='3306',user='root', password='', database='training',buffered=True, autocommit=True)

db_connection = open_db()


def save_by_nickname(nickname, exercices, dates, duration, nb_of_right_answers, total_answers):
    query = "INSERT INTO results (nickname, exercices, dates, duration, nb_of_right_answers, total_answers) values (%s,%s,%s,%s,%s,%s)"
    cursor = db_connection.cursor()
    cursor.execute(query, (nickname, exercices, dates, duration, nb_of_right_answers, total_answers,))
    row_id = cursor.lastrowid
    cursor.close()
    return row_id


def get_data_for_result_list():
    query = "SELECT results.nickname, results.exercices, results.dates, results.duration, results.nb_of_right_answers, results.total_answers FROM results"
    cursor = db_connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return data