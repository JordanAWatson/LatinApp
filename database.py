import mysql.connector
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
    except Error as err:
        print(f"Error: '{err}'")

    return connection



connection = create_server_connection("127.0.0.1", "root", "admin", "latin")
cursor = connection.cursor()


cursor.close()
connection.close()
