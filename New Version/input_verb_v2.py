'''
This program is being built to be used for inserting verbs
into the latin database

Built in Python 3.10
Not backwards compatible with Python 2.

KNOWN ISSUES


TODO
    complete test cases
    build verb insertion code
    pass all tests
'''

__author__ = "Jordan Watson"
__maintainer__ = "Jordan Watson"
__email__ = "JordanA.Watson@calbaptist.edu"
__status__ = "Development"
__date__ = "11-03-21"
__credits__ = ["Abraham Calvillo"]

import mysql.connector
from mysql.connector import Error
import sys
import configparser
import re

class Verb():
    ''' parent class for all specific table classses '''

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self._data = {}
        self.push_query = ""

    def __repr__(self):
        string = ""
        i = len(self._data.items())
        for a in self._data.items():
            i = i - 1
            string = string + f"{a[0]}: {a[1]}"
            if i > 0:
                string = string + ", "
        return string
    
    def push(self) -> None:
        try:
            # values are taken from data then turned into a tuple
            self.cursor.execute(self.push_query, tuple(self._data.values()))
            self.connection.commit()
        except Error as e:
            raise Exception(f"SQL error: '{e}'")

    def get_data() -> dict:
        return self._data
        


class Dictionary(Verb):
    ''' interacts with dictionary table '''
    
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.push_query = "INSERT INTO dictionary VALUES (%s, %s);"
        self._data = {
            "verb": None,
            "conjugation": None,
            }

    # sets verb
    def set_verb(self, verb) -> None:
        self._data["verb"] = verb

    # sets conjugation after validating input
    def set_conjugation(self, conjugation) -> None:
        if conjugation not in {"1st", "2nd", "3rd", "4th", "4th-io"}:
            raise ValueError("Conjugation must be 1st, "
                             "2nd, 3rd, 4th, or 3rd-io")
        else:
            self._data["conjugation"] = conjugation
        

class VerbForm(Verb):
    '''interacts with verbForm table'''

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.push_query = "INSERT INTO verbForm VALUES (%s, %s);"
        self._data = {
            "form": "",
            "stem": ""
            }

    # sets form
    def set_form(self, form) -> None:
        self._data["form"] = form

    # sets stem
    def set_stem(self, stem) -> None:
        self._data["stem"] = stem


class FormInfo(Verb):
    ''' interacts with formInfo table '''

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.push_query = ("INSERT INTO formInfo "
                           "VALUES(%s, %s, %s, %s, %s, %s);")
        self._data = {
            "form": "",
            "voice": "",
            "mood": "",
            "tense": "",
            "number": "",
            "person": "",
            }

    # sets form
    def set_form(self, form) -> None:
        self._data["form"] = form

    # sets voice
    def set_voice(self, voice) -> None:
        if voice in ["ACT", "PAS"]:
            self._data["voice"] = voice
        else:
            raise ValueError("Must be ACT or PAS")

    # sets mood
    def set_mood(self, mood) -> None:
        if mood in ["IND", "SUB", "IMP", "INF"]:
            self._data["mood"] = mood
        else:
            raise ValueError("Msut be IND, SUB, IMP, or INF")

    # sets tense
    def set_tense(self, tense) -> None:
        if tense in ["PRES", "IMPF", "FUTR", "PERF", "PLPF", "FRPF"]:
            self._data["tense"] = tense
        else:
            raise ValueError("Must be PRES, IMPF, FUTR, PERF, PLPF, or FRPF")

    # sets number
    def set_number(self, number) -> None:
        if number in [1, 2]:
            self._data["number"] = number
        else:
            raise ValueError("Must be 1 or 2")

    # sets person
    def set_person(self, person) -> None:
        if person in [1, 2, 3]:
            self._data["person"] = person
        else:
            raise ValueError("Must be 1, 2, or 3")



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

def clean_input(prompt) -> str:
    ''' removes non character, number, and macron elements of an input
        returns a cleaned string '''
    dirty = input(prompt)

    # FIXME would rather have whitelisting here
    return re.sub("[!@#$%^&*(){}[\]|\\\\:;\"'<>,.?/_\-\+\=~`\n\t]", "", dirty)


def table_test_cases():
    ''' tests tabel objects '''
    
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
        if d._data["verb"] != None:
            raise ValueError("Verb was not initalised empty")
        if d._data["conjugation"] != None:
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
        if d._data["verb"] == "amo" and d._data["conjugation"] == "1st":
            print("Test pass")
        else:
            raise Exception
    except Exception as e:
        print("Test fail")
        print("\tcouldn't build dictionary")
        print("\t", e)

    # print dictionary
    try:
        if str(d) == "verb: amo, conjugation: 1st":
            print("Test pass")
        else:
            raise Exception("failed to string")
    except Exception as e:
        print("Test fail")
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

    # build bad verbForm
    try:
        v.set_form("amas")
        v.set_stem("am")
        print("Test fail")
    except Exception as e:
        print("Test pass")
        print("\t", e)

    # build verbForm
    try:
        v.set_form("amas")
        v.set_stem("amo")
        if v._data["form"] == "amas" and v._data["stem"] == "amo":
            print("Test pass")
            
        else:
            raise Exception("data not set correctly")
    except Exception as e:
        print("Test fail")
        print("\t", e)

    # print verbForm
    try:
        if str(v) == "form: amas, stem: amo":
            print("Test pass")
        else:
            raise Exception("failed to string")
    except Exception as e:
        print("Test fail")
        print("\t", e)

    # push verbform
    try:
        v.push()
        print("Test pass")
    except Exception as e:
        print("Test fail")
        print("\t", e)
        


    # FORMINFO TESTS
    print()
    print("formInfo Tests:")
    # build empty formInfo
    try:
        f = FormInfo(connection, cursor)
        print("Test pass")
    except Exception as e:
        print("Test fail")
        print("\t", e)

    # build bad formInfo with wrong input
    try:
        f.set_form("amas")
        f.set_voice("active")
        print("Test fail")
    except ValueError as e:
        print("Test pass")
    except Exception as e:
        print("Test fail")
        print("\t", e)
    try:
        f.set_mood("a")
        print("Test fail")
    except ValueError as e:
        print("Test pass")
    except Exception as e:
        print("Test fail")
        print("\t", e)
    try:
        f.set_tense("a")
        print("Test fail")
    except ValueError as e:
        print("Test pass")
    except Exception as e:
        print("Test fail")
        print("\t", e)
    try:
        f.set_number("a")
        print("Test fail")
    except ValueError as e:
        print("Test pass")
    except Exception as e:
        print("Test fail")
        print("\t", e)
    try:
        f.set_person("a")
        print("Test fail")
    except ValueError as e:
        print("Test pass")
    except Exception as e:
        print("Test fail")
        print("\t", e)

    # build bad formInfo with mood-tense mismatch
    try:
        f.set_mood("SUB")
        f.set_tense("FUTR")
        print("Test fail")
    except Exception as e:
        print("Test pass")
        print("\t", e)

    # build good formInfo
    try:
        f.set_form("amas")
        f.set_voice("ACT")
        f.set_mood("IND")
        f.set_tense("PRES")
        f.set_number(1)
        f.set_person(2)
        print("Test pass")
    except Exception as e:
        print("Test pass")
        print("\t", e)

    # print formInfo
    try:
        if str(f) == ("form: amas, voice: ACT, mood: IND, tense: "
                      "PRES, number: 1, person: 2"):
            print("Test pass")
        else:
            raise Exception("failed to string")
    except Exception as e:
        print("Test fail")
        print("\t", e)

    # push formInfo
    try:
        f.push()
        print("Test pass")
    except Exception as e:
        print("Test fail")
        print("\t", e)

    # MYSQL key tests
    print("\nSQL key test")
    try:
        d.set_verb("liber")
        d.push()
        d.set_verb("līber")
        d.push()
        print("Test pass")
    except Exception as e:
        print("Test fail")
        print("\t", e)


    # end tests
    print()
    #input("Check values in SQL now")
    print("Clearing database")
    try:
        cursor.execute("DELETE FROM dictionary;", ())
        connection.commit()
    except:
        cursor.execute("DELETE FROM formInfo;", ())
        cursor.execute("DELETE FROM verbForm;", ())
        cursor.execute("DELETE FROM dictionary;", ())
        connection.commit()

    print("Closing database connection")
    cursor.close()
    connection.close()
    print("Testing complete")
    #input()
        

# main
def main() -> None:
    if ENVIRONMENT == "test":
        table_test_cases()
    else:
        print(f"Environment '{ENVIRONMENT}' is not valid")


if __name__ == "__main__":
    # set config variables
    config = configparser.ConfigParser()
    config.read("config.ini")
    ENVIRONMENT = config.get("settings", "ENVIRONMENT")
    host_name = config.get("database", "host_name")
    user_name = config.get("database", "user_name")
    user_password = config.get("database", "user_password")
    db_name = config.get("database", "db_name")

    main()
