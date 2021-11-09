import verb_tables
import mysql.connector
from mysql.connector import Error
import configparser


def table_test_cases():
    ''' tests tabel objects '''
    
    print("Starting tests:")

    connection = create_server_connection(host_name, user_name,
                                          user_password, db_name)
    cursor = connection.cursor()

    try:
        d = verb_tables.Dictionary("amo", "1st", connection, cursor)
        d.validate()
        print("Test pass")
    except Exception as e:
        print("Test fail")
        print(f"\t{e}")

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
