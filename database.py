import mysql.connector
import config


def connect_to_database():
    try:
        connection = mysql.connector.connect()
        return connection
    except mysql.connector.Error as err:
        print("Error connecting to database: {}".format(err))
        return err
