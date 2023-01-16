from psycopg2 import Error

from random_word import RandomWords
from random import randint, uniform, choice

from logger import write_to_servlog, write_to_errlog
from connection import connect_to_db, disconnect_from_db
from templates_handler import get_templates

settings = get_templates('constants')['generator']


def get_create_table_query(columns, table_name):
    column_types = [settings['FIRST_COLUMN_TYPE']]
    column_names = [settings['FIRST_COLUMN_NAME']]
    column_string = settings['FIRST_COLUMN_PREFIX']
    for i in range(1, columns + 1):
        column_type = choice(settings['DATA_TYPES'])
        column_name = RandomWords().get_random_word()
        column_types.append(column_type)
        column_names.append(column_name)
        column_string += ', {} {}'.format(column_name, column_type)
    create_table_query = settings['CREATE_QUERY_TEMPLATE'].format(
        table_name, column_string)
    return create_table_query, column_names, column_types


def get_insert_into_query(columns, column_names, column_types):
    names_string = settings['FIRST_COLUMN_NAME']
    values_string = settings['FIRST_VALUE']
    for column in range(1, columns + 1):
        names_string += ', {}'.format(column_names[column])
        value_type = column_types[column]
        if value_type == 'VARCHAR' or value_type == 'TEXT':
            value = "'{}'".format(RandomWords().get_random_word())
        elif value_type == 'INT':
            value = str(randint(*settings['RAND_LIMITS']))
        elif value_type == 'REAL':
            value = str(uniform(*settings['RAND_LIMITS']))
        values_string += ", {}".format(value)
    return names_string, values_string


def random_table(uid):
    columns = randint(*settings['COLUMNS'])
    rows = randint(*settings['ROWS'])
    table_name = RandomWords().get_random_word()
    create_table_query, column_names, column_types = get_create_table_query(
        columns, table_name)
    try:
        connection = connect_to_db(user=uid, password=uid, db_name=uid)
        cursor = connection.cursor()
    except (Exception, Error) as error:
        write_to_errlog(error)
        return 'CONNECTION_FAILED'
    try:
        cursor.execute(create_table_query)
        connection.commit()
        write_to_servlog('RANDOM_TABLE_CREATED', uid, uid)
        for row in range(rows + 1):
            names_string, values_string = get_insert_into_query(
                columns, column_names, column_types)
            insert_query = settings['INSERT_QUERY_TEMPLATE'].format(
                table_name, names_string, values_string)
            cursor.execute(insert_query)
            connection.commit()
        write_to_servlog('RANDOM_TABLE_FILLED', uid, uid)
        return table_name
    except (Exception, Error) as error:
        write_to_errlog(error)
    finally:
        disconnect_from_db(connection)
