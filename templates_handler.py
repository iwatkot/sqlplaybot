import json

from re import escape

templates = {
    'user': 'templates/user_messages.json',
    'server': 'templates/server_messages.json',
    'bot': 'templates/bot_messages.json',
}


def message_templates(which):
    return json.load(open(templates[which], encoding='utf-8'))


def fetch_formatter(fetch: [list[str]]) -> str:
    oneline = ""
    for line in fetch:
        oneline += "`{}\n`".format(escape(str(line)))
    return oneline
