import logging
import json
import sys

SYS_MESSAGE_FILE = 'templates/system.json'
LOG_FILE = 'logs/main_log.txt'

logging.basicConfig(level=logging.INFO, filename=LOG_FILE, filemode='a',
                    format="%(asctime)s %(levelname)s %(message)s")
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

with open(SYS_MESSAGE_FILE) as smf:
    SYS_MESSAGES = json.load(smf)


def write_to_servlog(connection, event):
    user = connection.get_dsn_parameters()['user']
    db_name = connection.get_dsn_parameters()['dbname']
    logging.info(SYS_MESSAGES[event].format(user, db_name))


def write_to_errlog(error):
    logging.error((str(error).replace('\n', '')))
