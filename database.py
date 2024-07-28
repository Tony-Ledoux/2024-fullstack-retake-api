import mysql.connector
import config


def connect_to_database():
    try:
        connection = mysql.connector.connect(host=config.db_host, user=config.db_username, password=config.db_password)
        return connection
    except mysql.connector.Error as err:
        print("Error connecting to database: {}".format(err))
        return err
