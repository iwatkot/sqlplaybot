from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from logger import write_to_servlog, write_to_errlog
from connection import connect_to_db, disconnect_from_db


def manage_db(uid, action):
    connection = connect_to_db(user=uid, password=uid)
    try:
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        manage_db_query = "{} DATABASE {}".format(action, uid)
        cursor.execute(manage_db_query)
        write_to_servlog(f"{action}_DB", uid, uid)
    except (Exception, Error) as error:
        write_to_errlog(error)
    finally:
        disconnect_from_db(connection)


def execute_query(uid, query):
    try:
        connection = connect_to_db(user=uid, password=uid, db_name=uid)
        cursor = connection.cursor()
    except (Exception, Error) as error:
        write_to_errlog(error)
        return 'CONNECTION_FAILED'
    try:
        cursor.execute(query)
        connection.commit()
        write_to_servlog("QUERY_EXECUTED", uid, uid)
        return cursor.fetchall()
    except (Exception, Error) as error:
        if str(error) != 'no results to fetch':
            write_to_errlog(error)
            return error
    finally:
        disconnect_from_db(connection)
