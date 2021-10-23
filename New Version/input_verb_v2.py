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
# implement Dictionary class
# implement VerbForm class
# implement FormInfo class
# build verb insertion code
# pass all tests



from abc import ABC
import mysql.connector

class Verb(ABC):
    '''abstract Verb class'''

    def __init__(self, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self._built = False

    def build_data(self):
        raise NotImplementedError("Child class has not implemented function")
    
    def push():
        raise NotImplementedError("Child class has not implemented function")


class Dictionary(Verb):
    '''interacts with dictionary table'''
    
    def __init__(self, connection, cursor):
        # self.connection = connection    # TODO test if this is inherited
        # self.cursor = cursor
        # self.built = False
        self.pull_query = "SELECT * FROM dictionay WHERE %s == %s;"
        self.push_query = "INSERT INTO dictionary VALUES (%s, %s);"
        self.search_query = "SELECT verb FROM dictionary WHERE %s == %s;"
        self._verb = ""
        self._conjugation = ""

    # sets _verb
    def set_verb(self, verb) -> None:
        self._verb = verb

    # sets _conjugation after validating input
    def set_conjugation(self, conjugation) -> None:
        if conjugation not in {"1st", "2nd", "3rd", "4th", "4th-io"}:
            raise ValueError("Conjugaiton must be 1st, "
                             "2nd, 3rd, 4th, or 3rd-io")
        else:
            self._conjugation = conjugation

    # returns _verb
    def get_verb(self) -> str:
        return self._verb

    # returns _conjugation
    def get_conjugation(self) -> str:
        return self._conjugation

    def to_string(self) -> None:
        print(f"{self._verb}, {self._conjugation}")

    # build the data to be pushed to the database
    def build_data(self) -> None:
        self.data = (self._verb, self._conjugation)
        self._built = True

    # pushes Dictionary to database
    def push(self) -> None:
        raise NotImplementedError("Function not implemented")


class VerbForm(Verb):
    '''interacts with verbForm table'''
    pass


class FormInfo(Verb):
    '''interacts with formInfo table'''
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
        print(f"Connection to to MySQL Database '{host_name}' with Schema "
              "'{db_name}' successful")
    except Error as error:
        print(f"Error: '{error}'")
        sys.exit()

    return connection






def dictionary_test_cases():
    print("Starting tests:")

    connection = create_server_connection("127.0.0.1", "editor", "editor",
                                          "latin")
    cursor = connection.cursor()

    # build empty dictionary
    try:
        d = Dictionary(connection, cursor)
        if d.get_verb() != "":
            raise ValueError("Verb was not initalised empty")
        if d.get_conjugation() != "":
            raise ValueError("Conjugation was not initalised empty")
        print("Test pass")
    except Exception as e:
        print("Test fail")
        print("\t", e)


    # build dictionary wrong
    try:
        d.set_verb("a")
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
        d.set_verb("a")
        d.set_conjugation("1st")
        if d.get_verb() == "a" and d.get_conjugation() == "1st":
            print("Test pass")
        else:
            raise Exception
    except Exception as e:
        print("Test fail")
        print("\tcouldn't build dictionary")
        print("\t", e)

    # build data
    try:
        d.build_data()
        print("Test pass")
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

    cursor.close()
    connection.close()
        


dictionary_test_cases()
