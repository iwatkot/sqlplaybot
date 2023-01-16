import logging
import sys
import os

from datetime import datetime

from templates_handler import get_templates

SERVER_MESSAGES = get_templates('server')
BOT_MESSAGES = get_templates('bot')

try:
    os.mkdir('./logs')
except FileExistsError:
    pass

logging.basicConfig(
    level=logging.INFO,
    filename=get_templates('constants')['files']['LOG_FILE'],
    filemode='a', format="%(asctime)s %(levelname)s %(message)s")
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))


def write_to_servlog(event, *args):
    logging.info(SERVER_MESSAGES[event].format(*args))


def write_to_errlog(error):
    logging.error((str(error).replace('\n', '')))


def write_to_botlog(*args):
    logging.info(BOT_MESSAGES['COMMAND'].format(*args))


def write_bug_report(bug_report, uid, user_name, encoding='utf-8'):
    timestamp = datetime.now()
    bug_report_entry = "{} {} name: {} report: {}\n".format(
        timestamp, uid, user_name, bug_report)
    with open(
        get_templates('constants')['files']['BUGREPORTS_FILE'], 'a') as brf:
        brf.write(bug_report_entry)
    write_to_servlog('BUG_REPORTED', uid, bug_report)
