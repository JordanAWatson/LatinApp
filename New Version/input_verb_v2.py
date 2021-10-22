from dataclasses import dataclass
from abc import ABC
import mysql.connector

@dataclass
class Verb(ABC):
    '''abstract Verb class'''

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor

@dataclass
class Dictionary(Verb):
    pass

@dataclass
class VerbForm(Verb):
    pass

@dataclass
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

    # connect to database
    try:
        connection = create_server_connection("127.0.0.1", "root", "admin", "latin")
        cursor = connection.cursor()
        print("Test pass")
    except:
        print("Test fail")

    # build dictionary
    try:
        d = Dictionary(connection, cursor)
        print("Test pass")
    except:
        print("Test fail")
        


dictionary_test_cases()
