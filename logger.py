import logging
import sys
import os

from templates_handler import message_templates

SERVER_MESSAGES = message_templates('server')
BOT_MESSAGES = message_templates('bot')
LOG_FILE = 'logs/main_log.txt'

try:
    os.mkdir('./logs')
except FileExistsError:
    pass

logging.basicConfig(level=logging.INFO, filename=LOG_FILE, filemode='a',
                    format="%(asctime)s %(levelname)s %(message)s")
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


def write_to_servlog(event, *args):
    logging.info(SERVER_MESSAGES[event].format(*args))


def write_to_errlog(error):
    logging.error((str(error).replace('\n', '')))


def write_to_botlog(*args):
    logging.info(BOT_MESSAGES['COMMAND'].format(*args))
