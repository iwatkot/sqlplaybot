import psycopg2

from decouple import config
from psycopg2 import Error

from logger import write_to_servlog, write_to_errlog

HOST = config('HOST')
PORT = config('PORT')


def connect_to_server(user, password):
    try:
        connection = psycopg2.connect(
            user=user,
            password=password,
            host=HOST,
            port=PORT,
            sslmode='require'
        )
        write_to_servlog(connection, 'CONNECTED')
        return connection
    except (Exception, Error) as error:
        write_to_errlog(error)


def disconnect_from_server(connection):
    if connection:
        write_to_servlog(connection, 'DISCONNECTING')
        connection.close()
