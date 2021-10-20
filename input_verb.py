# this program should not be accessed by users
# this is to input new verbs to the Latin batabase
# strange things happen if ran in the shell, so don't do that
#
# Author: Jordan Watson
# last edited: 10-19-20
#
# CURRENT ISSUES
# SQL thinks vowels with and without macrons are the same
#
# TODO
# check if verbForm exists
# input verbForm and formInfo


import mysql.connector
from mysql.connector import Error
import sys


# this function clears the screen
# taken from https://stackoverflow.com/questions/517970/how-to-clear-the-interpreter-console
import os
def cls():
    os.system('cls' if os.name=='nt' else 'clear')


def create_server_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host_name,
            user = user_name,
            password = user_password,
            database = db_name
        )
        print(f"Connection to to MySQL Database '{host_name}' with Schema '{db_name}' successful")
    except Error as error:
        print(f"Error: '{error}'")
        sys.exit()

    return connection


def push_query(query, data, cursor, connection):
    try:
        cursor.execute(query, data)
    except Error as error:
        print(f"Error pushing query: {query}")
        print(f"SQL error: '{error}'")
        cursor.close()
        connection.close()
        input()
        sys.exit()

    return cursor

def exists(verb, table, field, cursor, connection):
    query = (f"SELECT {field} FROM {table} " # note the space after 'Verb' is required
             f"WHERE {field} = %s;")
    push_query(query, (verb,), cursor, connection)

    if len(cursor.fetchall()) != 0:
        return True
    else:
        return False



# currently the only error handling
def wrong_input(cursor, connection):
    print("Wrong input")
    input()
    cursor.close()
    connection.close()
    sys.exit()

def logic_error(cursor, connection):
    print("Logic error")
    input()
    cursor.close()
    connection.close()
    sys.exit()




# MAIN
def main():
    connection = create_server_connection("127.0.0.1", "root", "admin", "latin")
    cursor = connection.cursor()

    stem = input("Verb's dictionary form: ")    # i.e. 'laudo'

    # check if the database already has the dictionary form of the verb
    if not exists(stem, "dictionary", "verb", cursor, connection):
        # add 
        print(f"'{stem}' is new to the database, please tell me about it.")
        print("Conjugation")
        conj = input("1st, 2nd, 3rd, 4th, 3rd-io: ")

        # loops untill the correct input is used
        while not (conj == "1st" or conj == "2nd" or conj == "3rd" or conj == "4th" or conj == "3rd-io"):
            cls()
            print("Conjugation")
            conj = input("1st, 2nd, 3rd, 4th, 3rd-io: ")

        query = ("INSERT INTO dictionary VALUES (%s, %s);")
        print(f"added {conj} conjugation verb '{stem}' to database")

        push_query(query, (stem, conj), cursor, connection)
        connection.commit()
        
    else:
        print(f"{stem} exists in the database")
        print(f"enter form of {stem}")
        voice = input("ACT/PAS: ")
        if voice != "ACT" and voice != "PAS":
            wrong_input(cursor, connection)

        # sets the mood and gives tenses. Not all moods have all the tenses
        mood = input("IND/SUB/IMP/INF: ")
        if mood == "IND":
            tense = int(input("1)Present 2)Imperfect 3)Future 4)Perfect 5)Pluperfect 6)Future Perfect: "))
            if tense > 6 or tense < 1:
                wrong_input(cursor, connection)
        elif mood == "SUB":
            tense = int(input("1)Present 2)Imperfect 4)Perfect 5)Pluperfect: "))
            if tense < 1 or tense == 3 or tense > 5:
                wrong_input(cursor, connection)
        elif mood == "IMP":
            tense = int(input("1)Present 3)Future: "))
            if tense != 1 or tense != 3:
                wrong_input(cursor, connection)
        elif mood == "INF":
            tense = int(input("1)Present 3)Future 4)Perfect: "))
            if tense < 1 or tense == 2 or tense > 4:
                wrong_input(cursor, connection)
        else:
            wrong_input(cursor, connection)

        # set the tense
        tense = str(tense)
        if tense == "1":
            tense = "PRES"
        elif tense == "2":
            tense = "IMPF"
        elif tense == "3":
            tense = "FUTR"
        elif tense == "4":
            tense = "PERF"
        elif tense == "5":
            tense = "PLPF"
        elif tense == "6":
            tense = "FRPF"
        else:
            tense = None
            logic_error(cursor, connection)

        # (form, stem)
        verbForm_query = ("INSERT INTO verbForm VALUES (%s, %s);")

        # (form, voice, mood, tense, number, person)
        formInfo_query = ("INSERT INTO formInfo VALUES (%s, %s, %s, %s, %s, %s);")

        # get all person and number forms for a verb conjugation, and push to the database
        for number in range (2):
            for person in range (3):
                if person == 0:
                    mut = "st"
                elif person == 1:
                    mut = "nd"
                else:
                    mut = "rd"

                if number == 0:
                    cnt = "singular"
                else:
                    cnt = "plural  "

                form = input(f"{person + 1}{mut} person {cnt}: ")

                push_query(formInfo_query, (

                

    cursor.close()
    connection.close()

    # end main

            
if __name__ == "__main__":
    main()
