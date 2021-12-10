import telegram
import os
import json
from hashlib import sha1

def send_tg_message(text):
    tg_bot = telegram.Bot(os.getenv("TELEGRAM_TOKEN"))
    for chat_id in os.getenv("TELEGRAM_CHAT_ID").split(";"):
        message_id = generate_message_id(chat_id, text)
        if not is_message_sent(message_id):
            tg_bot.send_message(chat_id, text, 'HTML', disable_web_page_preview=True)
            set_message_as_sent(message_id)

def generate_message_id(chat_id, text):
    return sha1(str(chat_id + "_" + text).encode('utf-8')).hexdigest()

def is_message_sent(message_id):
    filename = 'data/tg_sent_messages.json'
    if not os.path.exists(filename):
        return False
    with open(filename, 'r') as f:
        return message_id in json.load(f)

def set_message_as_sent(message_id):
    filename = 'data/tg_sent_messages.json'
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            data = json.load(f)
    else:
        data = []
    data.append(message_id)
    with open(filename, 'w') as f:
        json.dump(data, f)
