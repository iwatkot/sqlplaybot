from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from logger import write_to_servlog, write_to_errlog
from connection import connect_to_db, disconnect_from_db


def db_ddl(db_name, action):
    connection = connect_to_db(user=db_name, password=db_name)
    try:
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()
        db_ddl_query = "{} DATABASE {}".format(action, db_name)
        cursor.execute(db_ddl_query)
        write_to_servlog(db_name, db_name, f"{action}_DB")
    except (Exception, Error) as error:
        write_to_errlog(error)
    disconnect_from_db(connection)


def db_dml(db_name, query):
    connection = connect_to_db(user=db_name, password=db_name, db_name=db_name)
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except (Exception, Error) as error:
        write_to_errlog(error)
    disconnect_from_db(connection)
