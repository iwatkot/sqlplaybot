from psycopg2 import Error

from random_word import RandomWords
from random import randint, uniform, choice

from logger import write_to_servlog, write_to_errlog
from connection import connect_to_db, disconnect_from_db

ROWS = (2, 10)
COLUMNS = (2, 10)
RANDLIMITS = (-1000, 1000)
DATA_TYPES = [
    'VARCHAR',
    'TEXT',
    'INT',
    'REAL'
]
FIRST_COLUMN = 'id SERIAL PRIMARY KEY NOT NULL'
CREATE_QUERY = 'CREATE TABLE {} ({});'
INSERT_QUERY = "INSERT INTO {} ({}) VALUES ({});"


def create_table(columns_number, table_name):
    column_types = ['SERIAL']
    column_names = ['id']
    column_str = FIRST_COLUMN
    for i in range(1, columns_number + 1):
        column_type = choice(DATA_TYPES)
        column_name = RandomWords().get_random_word()
        column_types.append(column_type)
        column_names.append(column_name)
        column_str += ', {} {}'.format(column_name, column_type)
    create_query = CREATE_QUERY.format(table_name, column_str)
    return create_query, column_names, column_types


def fill_table(uid):
    columns_number = randint(*COLUMNS)
    rows_number = randint(*ROWS)
    table_name = RandomWords().get_random_word()
    create_query, column_names, column_types = create_table(
        columns_number, table_name)
    try:
        connection = connect_to_db(user=uid, password=uid, db_name=uid)
        cursor = connection.cursor()
    except (Exception, Error) as error:
        write_to_errlog(error)
        return 'CONNECTION_FAILED'
    try:
        cursor.execute(create_query)
        connection.commit()
        write_to_servlog('RANDOM_TABLE_CREATED', uid, uid)
        for row in range(rows_number + 1):
            names_str = 'id'
            values_str = "DEFAULT"
            for colummn in range(1, columns_number + 1):
                names_str += ', {}'.format(column_names[colummn])
                value_type = column_types[colummn]
                if value_type == 'VARCHAR' or value_type == 'TEXT':
                    value = "'{}'".format(RandomWords().get_random_word())
                elif value_type == 'INT':
                    value = str(randint(*RANDLIMITS))
                elif value_type == 'REAL':
                    value = str(uniform(*RANDLIMITS))
                values_str += ", {}".format(value)
            insert_query = INSERT_QUERY.format(
                table_name, names_str, values_str)
            cursor.execute(insert_query)
            connection.commit()
        write_to_servlog('RANDOM_TABLE_FILLED', uid, uid)
        return table_name
    except (Exception, Error) as error:
        write_to_errlog(error)
    finally:
        disconnect_from_db(connection)
