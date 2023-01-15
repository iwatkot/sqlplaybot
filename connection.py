import psycopg2

from decouple import config
from psycopg2 import Error

from logger import write_to_servlog, write_to_errlog

HOST = config('HOST')
PORT = config('PORT')
USER = config('USER')
PASSWORD = config('PASSWORD')
DB_NAME = config('DB_NAME')


def connect_to_db(user=USER, password=PASSWORD, db_name=DB_NAME):
    try:
        connection = psycopg2.connect(
            user=user,
            password=password,
            host=HOST,
            port=PORT,
            sslmode='require',
            database=db_name
        )
        write_to_servlog('CONNECTED', user, db_name)
        return connection
    except (Exception, Error) as error:
        write_to_errlog(error)
        return error


def disconnect_from_db(connection):
    if connection:
        user = connection.get_dsn_parameters()['user']
        db_name = connection.get_dsn_parameters()['dbname']
        write_to_servlog('DISCONNECTING', user, db_name)
        connection.close()
    else:
        write_to_servlog('NO_ACTIVE_CONNECTION')
