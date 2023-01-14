from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from logger import write_to_servlog, write_to_errlog


def create_db(connection, db_name):
    try:
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        create_db_query = "CREATE DATABASE {}".format(db_name)
        cursor.execute(create_db_query)
        write_to_servlog(connection, "CREATED_DB")
    except (Exception, Error) as error:
        write_to_errlog(error)


def delete_db(connection, db_name):
    try:
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        delete_db_query = "DROP DATABASE {}".format(db_name)
        cursor.execute(delete_db_query)
        write_to_servlog(connection, "DELETED_DB")
    except (Exception, Error) as error:
        write_to_errlog(error)
