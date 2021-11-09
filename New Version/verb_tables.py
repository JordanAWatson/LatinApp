'''
These classes are used to store latin database verb tables

Built in Python 3.10
Not backwards compatible with Python 2.

KNOWN ISSUES

'''

__author__ = "Jordan Watson"
__maintainer__ = "Jordan Watson"
__email__ = "JordanA.Watson@calbaptist.edu"
__status__ = "Development"
__date__ = "11-08-21"
__credits__ = ["Abraham Calvillo"]

import mysql.connector
from mysql.connector import Error

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
        

## FIXME using this class to test new usage
class Dictionary(Verb):
    ''' interacts with dictionary table '''
    
    def __init__(self, verb, conjugation, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.push_query = "INSERT INTO dictionary VALUES (%s, %s);"
        self._data = {
            "verb": verb,
            "conjugation": conjugation,
            }

    def validate(self) -> None:
        if self._data["conjugation"] not in {"1st", "2nd", "3rd",
                                            "4th", "4th-io"}:
            
            raise ValueError("Conjugation must be 1st, "
                             "2nd, 3rd, 4th, or 3rd-io")

        

class VerbForm(Verb):
    '''interacts with verbForm table'''

    def __init__(self, form, stem, connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.push_query = "INSERT INTO verbForm VALUES (%s, %s);"
        self._data = {
            "form": form,
            "stem": stem
            }
        

    def validate(self) -> None:
        pass


class FormInfo(Verb):
    ''' interacts with formInfo table '''

    def __init__(self, form, voice, mood, tense, number, person,
                 connection, cursor):
        self.connection = connection
        self.cursor = cursor
        self.push_query = ("INSERT INTO formInfo "
                           "VALUES(%s, %s, %s, %s, %s, %s);")
        self._data = {
            "form": form,
            "voice": voice,
            "mood": mood,
            "tense": tense,
            "number": number,
            "person": person,
            }

    def validate(self) -> None:
        if self._data["voice"] not in ["ACT", "PAS"]:
            raise ValueError("Must be ACT or PAS")            

        if self._data["mood"] not in ["IND", "SUB", "IMP", "INF"]:
            raise ValueError("Msut be IND, SUB, IMP, or INF")

        if self._data["tense"] not in ["PRES", "IMPF", "FUTR",
                                   "PERF", "PLPF", "FRPF"]:
            raise ValueError("Must be PRES, IMPF, FUTR, PERF, PLPF, or FRPF")

        if self._data["number"] not in [1, 2]:
            raise ValueError("Must be 1 or 2")

        if self._data["person"] not in [1, 2, 3]:
            raise ValueError("Must be 1, 2, or 3")
