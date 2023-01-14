from psycopg2 import Error, sql

from connection import connect_to_db, disconnect_from_db
from logger import write_to_servlog, write_to_errlog


def user_ddl(username, action):
    connection = connect_to_db()
    user = connection.get_dsn_parameters()['user']
    try:
        cursor = connection.cursor()
        if action == 'CREATE':
            user_ddl_query = "{} USER {} WITH PASSWORD '{}'".format(
                action, username, username)
        elif action == 'DROP':
            user_ddl_query = '{} USER IF EXISTS {}'.format(
                action, username)
        cursor.execute(user_ddl_query)
        connection.commit()
        write_to_servlog(user, username, f"{action}_USER")
    except (Exception, Error) as error:
        write_to_errlog(error)
    disconnect_from_db(connection)


def user_dml(username, action):
    connection = connect_to_db()
    user = connection.get_dsn_parameters()['user']
    try:
        cursor = connection.cursor()
        user_dml_query = '{} USER {} CREATEDB'.format(action, username)
        cursor.execute(user_dml_query)
        connection.commit()
        write_to_servlog(user, username, f"{action}_USER")
    except (Exception, Error) as error:
        write_to_errlog(error)
    disconnect_from_db(connection)
