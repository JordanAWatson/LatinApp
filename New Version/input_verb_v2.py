from abc import ABC
import mysql.connector

class Verb(ABC):
    '''abstract Verb class'''

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.pull_query = ""
        self.search_query = ""

    def push():
        pass


class Dictionary(Verb):
    '''interacts with dictionary table'''
    
    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.pull_query = "SELECT * FROM dictionay WHERE %s == %s;"
        self.push_query = "INSERT INTO dictionary VALUES (%s, %s);"
        self.search_query = "SELECT verb FROM dictionary WHERE %s == %s;"
        self.verb = ""
        self.conjugation = ""

    def set_verb(self, verb):
        self.verb = verb

    def set_conjugation(self, conjugation):
        if (
            conjugation != "1st"
            or conjugation != "2nd"
            or conjugation != "3rd"
            or conjugaiton != "4th"
            or conjugation != "3rd-io"
            ):
            raise ValueError("Conjugaiton must be 1st, 2nd, 3rd, 4th, or 3rd-io")
        else:
            self.conjugation = conjugation

    def get_verb(self):
        return self.verb

    def get_conjugation(self):
        return self.conjugation


class VerbForm(Verb):
    pass


class FormInfo(Verb):
    pass

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


def dictionary_test_cases():
    print("Starting tests:")

    connection = create_server_connection("127.0.0.1", "root", "admin", "latin")
    cursor = connection.cursor()

    # build empty dictionary
    try:
        d = Dictionary(connection, cursor)
        if d.get_verb != "":
            raise ValueError("Verb was not initalised empty")
        if d.get_conjugation != "":
            raise ValueError("Conjugation was not initalised empty")
        print("Test pass")
    except Exception as e:
        print("Test fail")
        print("\t", e)


    # build dictionary
    try:
        d.set_verb("a")
        d.set_conjugation("1st")
    except Exception as e:
        print("Test fail")
        print("\t", e)

    # build dictionary wrong
    try:
        d.set_verb("a")
        d.set_conjugation("z")
    except Exception as e:
        print("Test fail")
        print("\t", e)

    cursor.close()
    connection.close()
        


dictionary_test_cases()
