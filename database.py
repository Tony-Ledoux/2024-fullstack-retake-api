import mysql.connector
import config


def connect_to_database():
    try:
        connection = mysql.connector.connect(host=config.db_host, user=config.db_username,
                                             password=config.db_password)
        return connection
    except mysql.connector.Error as err:
        print("Error connecting to database: {}".format(err))
        return err


def execute_sql_query(sql_query, query_parameters=None):
    connection = connect_to_database()
    result = ''
    try:
        cursor = connection.cursor()
        cursor.execute(sql_query, query_parameters)
        if sql_query.upper().startswith("SELECT"):
            # executed for GET requests
            result = cursor.fetchall()
        else:
            # executed for POST requests
            connection.commit()
            result = True

        cursor.close()

    except mysql.connector.Error as exception:
        print("Error executing SQL query:", exception)
        result = exception

    finally:
        if connection.is_connected():
            connection.close()

        return result
