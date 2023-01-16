import json

from re import escape

files = {
    'user': 'templates/user_messages.json',
    'server': 'templates/server_messages.json',
    'bot': 'templates/bot_messages.json',
    'constants': 'templates/constants.json',
}


def get_templates(which):
    return json.load(open(files[which], encoding='utf-8'))


def fetch_formatter(fetch: [list[str]]) -> str:
    oneline = ""
    try:
        for line in fetch:
            oneline += "`{}\n`".format(escape(str(line)))
    except TypeError:
        oneline += "`{}`".format(escape(str(fetch)))
    return oneline
