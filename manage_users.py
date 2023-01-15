from psycopg2 import Error

from connection import connect_to_db, disconnect_from_db
from logger import write_to_servlog, write_to_errlog


def manage_user(uid, action):
    connection = connect_to_db()
    admin_user = connection.get_dsn_parameters()['user']
    try:
        cursor = connection.cursor()
        if action == 'CREATE':
            manage_user_query = "{} USER {} WITH PASSWORD '{}'".format(
                action, uid, uid)
        elif action == 'DROP':
            manage_user_query = '{} USER IF EXISTS {}'.format(
                action, uid)
        cursor.execute(manage_user_query)
        connection.commit()
        write_to_servlog(f"{action}_USER", admin_user, uid)
    except (Exception, Error) as error:
        write_to_errlog(error)
    finally:
        disconnect_from_db(connection)


def user_permissions(uid, action):
    connection = connect_to_db()
    admin_user = connection.get_dsn_parameters()['user']
    try:
        cursor = connection.cursor()
        user_permissions_query = '{} USER {} CREATEDB'.format(action, uid)
        cursor.execute(user_permissions_query)
        connection.commit()
        write_to_servlog(f"{action}_USER", admin_user, uid)
    except (Exception, Error) as error:
        write_to_errlog(error)
    finally:
        disconnect_from_db(connection)
