import json

templates = {
    'user': 'templates/user_messages.json',
    'server': 'templates/server_messages.json',
    'bot': 'templates/bot_messages.json',
}


def message_templates(which):
    return json.load(open(templates[which], encoding='utf-8'))
