# This program is being built to be used for inserting verbs
# into the latin database
#
# Authour: Jordan Watson
# last edited: 10-22-20
#
# KNOWN ISSUES
# SQL thinks vowels with and without macrons are the same
#   this may break the project if not fixed
#
# TODO
# complete test cases
# build verb insertion code
# pass all tests


import mysql.connector
from mysql.connector import Error
import sys

class Verb():

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.data = {}
        self.push_query = ""
    
    def push(self) -> None:
        try:
            # values are taken from data then turned into a tuple
            self.cursor.execute(self.push_query, tuple(self.data.values()))
            self.connection.commit()
        except Error as e:
            raise Exception(f"SQL error: '{e}'")


class Dictionary(Verb):
    '''interacts with dictionary table'''
    
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.push_query = "INSERT INTO dictionary VALUES (%s, %s);"
        self.data = {
            "verb": None,
            "conjugation": None,
            }

    # sets verb
    def set_verb(self, verb) -> None:
        self.data["verb"] = verb

    # sets conjugation after validating input
    def set_conjugation(self, conjugation) -> None:
        if conjugation not in {"1st", "2nd", "3rd", "4th", "4th-io"}:
            raise ValueError("Conjugaiton must be 1st, "
                             "2nd, 3rd, 4th, or 3rd-io")
        else:
            self.data["conjugation"] = conjugation
        

class VerbForm(Verb):
    '''interacts with verbForm table'''

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.push_query = "INSERT INTO verbForm VALUES (%s, %s);"
        self.data = {
            "form": "",
            "stem": ""
            }

    # sets form
    def set_form(self, form) -> None:
        self.data["form"] = form

    # sets stem
    def set_stem(self, stem) -> None:
        self.data["stem"] = stem


class FormInfo(Verb):
    '''interacts with formInfo table'''

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.push_query = ("INSERT INTO formInfo "
                           "VALUES(%s, %s, %s, %s, %s, %s, %s,);")
        self.data = {
            "form": "",
            "voice": "",
            "mood": "",
            "tense": "",
            "number": "",
            "person": "",
            "data": ""
            }

    # sets form
    def set_form(self, form) -> None:
        self.data["form"] = form

    # sets voice
    def set_form(self, voice) -> None:
        self.data["voice"] = voice

    # sets mood
    def set_form(self, mood) -> None:
        self.data["mood"] = mood

    # sets tense
    def set_form(self, tense) -> None:
        self.data["tense"] = tense

    # sets number
    def set_form(self, number) -> None:
        self.data["number"] = number

    # sets person
    def set_form(self, person) -> None:
        self.data["person"] = person



def create_server_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host = host_name,
            user = user_name,
            password = user_password,
            database = db_name
        )
        print(f"Connection to to MySQL Database '{host_name}' with Schema "
              "'{db_name}' successful")
    except Error as error:
        print(f"Error: '{error}'")
        input()
        sys.exit()

    return connection


def dictionary_test_cases():
    print("Starting tests:")

    connection = create_server_connection("127.0.0.1", "root", "admin",
                                          "latin")
    cursor = connection.cursor()

    # DICTIONARY TESTS
    print()
    print("Dictionary tests:")
    # build empty dictionary
    try:
        d = Dictionary(connection, cursor)
        if d.data["verb"] != None:
            raise ValueError("Verb was not initalised empty")
        if d.data["conjugation"] != None:
            raise ValueError("Conjugation was not initalised empty")
        print("Test pass")
    except Exception as e:
        print("Test fail")
        print("\t", e)


    # build dictionary wrong
    try:
        d.set_verb("amo")
        d.set_conjugation("z")
        print("Test fail")
        print("\tconjugation shouldn't be accepted")
    except ValueError as e:
        print("Test pass")
    except Exception as e:
        print("Test fail")
        print("\t", e)

    # build dictionary
    try:
        d.set_verb("amo")
        d.set_conjugation("1st")
        if d.data["verb"] == "amo" and d.data["conjugation"] == "1st":
            print("Test pass")
        else:
            raise Exception
    except Exception as e:
        print("Test fail")
        print("\tcouldn't build dictionary")
        print("\t", e)

    # push dictionary
    try:
        d.push()
        print("Test pass")
    except Exception as e:
        print("Test fail")
        print("\t", e)


    # VEBRFORM TESTS
    print()
    print("verbForm Tests:")
    # build empty verbform
    try:
        v = VerbForm(connection, cursor)
        print("Test pass")
    except Exception as e:
        print("Test fail")
        print("\t", e)


    cursor.execute("DELETE FROM Dictionary;", ())
    connection.commit()

    cursor.close()
    connection.close()
        


dictionary_test_cases()
