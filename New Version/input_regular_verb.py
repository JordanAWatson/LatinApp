import mysql.connector
import sys
from mysql.connector import Error

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


def push_query(query, data):
    try:
        cursor.execute(query, data)
    except Error as error:
        print(f"Error: '{error}'")
        cursor.close()
        connection.close()
        sys.exit()

    return cursor


def search_verb(cursor, p1, dec):
    query = ("SELECT first FROM verb_principle_parts "
         "WHERE first = %s AND declension = %s;")
    push_query(query, (p1, dec))

    i = 0
    for (first) in cursor:
        i = i + 1

    return i

def auto(p1, p2, p3, p4, dec, trans):
    print("Unfinished")

    base = p2[:-3]

    voices = ["active", "passive"]
    moods = ["indicative", "subjunctive", "imperative", "infinitive"]
    tenses = ["present", "imperfect", "future", "perfect", "pluperfect", "future perfect"]
    persons = ["1st", "2nd", "3rd"]
    numbers = ["singular", "plural"]

    active = {"indicative":("present", "imperfect", "future", "perfect", "pluperfect", "future perfect"),
              "subjunctive":("present", "imperfect", "perfect", "pluperfect"),
              "imperative":("present", "future"),
              "infinitive":("present", "future", "perfect")}
    

    query = ("INSERT INTO verb (name, firstPrinciplePart, person, number, voice, mood, tense) "
             "VALUES (%s, %s, %s, %s, %s, %s, %s);")
    data = ()
    
def manual(p1, dec, trans):
    print("Unfinished")

    query = ("INSERT INTO verb (name, firstPrinciplePart, person, number, voice, mood, tense) "
             "VALUES (%s, %s, %s, %s, %s, %s, %s);")

    name = input("Verb: ")
    data = (name, p1)
    

# MAIN

connection = create_server_connection("127.0.0.1", "root", "admin", "latin")
cursor = connection.cursor()


print("Enter verb principle part info")
dec = input("Declension: ")
p1 = input("1st part: ")

if search_verb(cursor, p1, dec) != 0:
    print(f"{p1} already exists")
    input()
    sys.exit()

p2 = input("2nd part: ")
p3 = input("3rd part: ")
p4 = input("4th part: ")
trans = input("Translation: ")

query = ("INSERT INTO verb_principle_parts "
             "VALUES (%s, %s, %s, %s, %s, %s);")

push_query(query, (p1, p2, p3, p4, dec, trans))

print("Manual mode is recomended for irregular verbs")
dec = input("Manual input mode? y/n: ")
if dec == "y":
    manual(p1, p2, dec, trans)
elif dec == "n":
    print("Auto-generating verbs")
    auto(p1, p2, p3, p4, dec, trans)
else:
    print("Incorrect input, defaulting to automatic generation")

connection.commit()

cursor.close()
connection.close()
