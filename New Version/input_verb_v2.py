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
# move SQL login info to config file


import mysql.connector
from mysql.connector import Error
import sys
import configparser
import re

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
        if voice in ["ACT", "PAS"]:
            self.data["voice"] = voice
        else:
            raise ValueError("Must be ACT or PAS")

    # sets mood
    def set_form(self, mood) -> None:
        if mood in ["IND", "SUB", "IMP", "INF"]:
            self.data["mood"] = mood
        else:
            raise ValueError("Msut be IND, SUB, IMP, or INF")

    # sets tense
    def set_form(self, tense) -> None:
        if tense in ["PRES", "IMPF", "FUTR", "PERF", "PLPF", "FRPF"]:
            self.data["tense"] = tense
        else:
            raise ValueError("Must be PRES, IMPF, FUTR, PERF, PLPF, or FRPF")

    # sets number
    def set_form(self, number) -> None:
        if number in ["1st", "2nd", "3rd", "4th", "3rd-io"]:
            self.data["number"] = number
        else:
            raise ValueError("Must be 1st, 2nd, 3rd, 4th, or 3rd-io")

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
              f"'{db_name}' successful")
    except Error as error:
        print(f"Error: '{error}'")
        input()
        sys.exit()

    return connection

# removes non character, number, and macron elements of an input
# returns a cleaned string
def clean_input(prompt) -> str:
    dirty = input(prompt)

    # FIXME would rather have whitelisting here
    return re.sub("[!@#$%^&*(){}[\]|\\\\:;\"'<>,.?/_\-\+\=~`\n\t]", "", dirty)


def dictionary_test_cases():
    
    print("Starting tests:")

    connection = create_server_connection(host_name, user_name,
                                          user_password, db_name)
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


    try:
        cursor.execute("DELETE FROM dictionary;", ())
        connection.commit()
    except:
        cursor.execute("DELETE FROM formInfo;", ())
        cursor.execute("DELETE FROM verbForm;", ())
        cursor.execute("DELETE FROM dictionary;", ())
        connection.commit()

    cursor.close()
    connection.close()
        

# main
def main() -> None:
    print("Main")


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("config.ini")
    ENVIROMENT = config.get("settings", "ENVIROMENT")
    host_name = config.get("database", "host_name")
    user_name = config.get("database", "user_name")
    user_password = config.get("database", "user_password")
    db_name = config.get("database", "db_name")

    if ENVIROMENT == "test":
        dictionary_test_cases()

    else:
        main()
