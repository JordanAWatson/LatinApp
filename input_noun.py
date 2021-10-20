import mysql.connector
import sys
from mysql.connector import Error


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
        input()
        sys.exit()

    return connection

def push_query(query, data):
    try:
        cursor.execute(query, data)
        connection.commit()
        print("Commit successful")
    except Error as error:
        print(f"Error in query '{query}': '{error}'")
        input()
        cursor.close()
        connection.close()
        sys.exit()



# MAIN
connection = create_server_connection("127.0.0.1", "root", "admin", "latin")
cursor = connection.cursor()

cont = True
while cont == True:
    declension = int(input("Declension: "))
    if declension > 5 or declension < 1:
        print("Incorrect input!")
        break
    gender = input("Gender m/f/n: ")
    if gender != 'm' and gender != 'f' and gender != 'n':
        print("Incorrect input!")
        break
    print("Singular")
    noms = input("Nom: ")
    gens = input("Gen: ")
    dats = input("Dat: ")
    accs = input("Acc: ")
    abls = input("Abl: ")
    vocs = input("Voc: ")
    locs = input("Loc: ")

    print("Singular")
    nomp = input("Nom: ")
    genp = input("Gen: ")
    datp = input("Dat: ")
    accp = input("Acc: ")
    ablp = input("Abl: ")
    vocp = input("Voc: ")
    locp = input("Loc: ")

    if vocs == "":
        voc = None
    if locs == "":
        loc = None
    if vocp == "":
        voc = None
    if locp == "":
        loc = None

    translation = input("Translation: ")
    if len(translation) > 50:
        print("Too long!")
        break
        

    query = ("INSERT INTO noun "
             "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);")
    push_query(query, (noms, gens, dats, accs, abls, vocs, locs, nomp, genp, datp, accp, ablp, vocp, locp, translation, declension, gender))
    connection.commit()
    if input("Add another? y/n") == "n":
        cont = False
    else:
        cls()

input()
cursor.close()
connection.close()
