import time
import json
import urllib.parse
import requests
import re
import os
import threading
from datetime import datetime


#db = DBHelper('weather_data')
TOKEN = "5584161509:AAFwAx4FNR_hSJNArQulRQ1alba-CjjLszA"
URL = f"https://api.telegram.org/bot{TOKEN}/"
simple_statistic = set()

def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = f"{URL}sendMessage?text={text}&chat_id={chat_id}"
    if reply_markup:
        url += f"&reply_markup={reply_markup}"
    get_url(url)


def send_photo(photo, chat_id, text=None, reply_markup=None, ):
    url = f"{URL}sendPhoto?chat_id={chat_id}"
    files = {'photo': open(photo, 'rb')}
    if text:
        text = urllib.parse.quote_plus(text)
        url += f'&caption={text}'
    if reply_markup:
        url += f"&reply_markup={reply_markup}"
    requests.post(url, files=files)


def get_url(url: str):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url: str):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += f"&offset={offset}"
    js = get_json_from_url(url)
    return js


'''
def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard": True}
    return json.dumps(reply_markup)
'''


def build_keyboard_help():
    reply_markup = {"keyboard": [['/help'],['❤']], "one_time_keyboard": False, "resize_keyboard": True}
    return json.dumps(reply_markup)


def is_file_exist(path: str) -> bool:
    return os.path.isfile(path)


def handle_updates(updates):
    for update in updates["result"]:
        keyboard_help = build_keyboard_help()
        print(f'Принят запрос в {datetime.now()}')
        if 'edited_message' in update:
            simple_statistic.add(update['edited_message']['chat']['id'])
            send_message('Ты изменил какое-то сообщение -.-', update['edited_message']['chat']['id'])
            print(f'    * Измененное сообщение')
            continue

        if 'message' not in update:
            simple_statistic.add(update['my_chat_member']['chat']['id'])
            send_message('Такого функционала пока нет', update['my_chat_member']['chat']['id'])
            print(f'    * Кто-то подписался или отписался')
            continue

        chat = update["message"]["chat"]["id"]
        simple_statistic.add(chat)
        try:
            text = update["message"]["text"]

            if text == '/start':

                send_message(
                    'Привет! Напиши номер задачки из Демидовича, '
                    'которую хочешь получить', chat, keyboard_help)
                print('    * Отправил /start')
            elif text == '/help':
                send_message(
                    'Привет! Бот может отправить тебе номер из демидовича \n'
                    'Пиши ему номер задания по типу:\n123 или 123.4 \n\n'
                    'Пока отправляем только картинку условия (ответов и решений нет, увы) \n'
                    'Если номер не найден, но ты знаешь, что он точно есть, '
                    'попробуй отправить соседние номера \n(или, если это номер с точкой как 123.4, '
                    'попробуй отправить только целую часть (123))\n\n'
                    'Если будут любые проблемы, пиши авторам: @therealnowhereman, @Demotivator_Stepan, @not_amigo\n'
                    'Удачи!) 🥰', chat)
                print('    * Отправил /start')
            elif text == '/stat':
                send_message(
                    f'Cегодня бота его юзали {len(simple_statistic)} человек 😱', chat)
                print('    * Отправил статистику')
            elif text == '❤':
                send_message(f'❤', chat)
                print('    * Отправил ❤')
            else:
                number_found = re.fullmatch(r'\d*\.?(\d*)?', text)
                if number_found:
                    if is_file_exist(f'images/{number_found[0]}.gif'):
                        send_photo(f'images/{number_found[0]}.gif', chat,
                                   f'Вот твой номер {number_found[0]} 😘')
                        print(f'    * Отправил номер {number_found[0]}')
                    else:
                        send_message(f'Номера {number_found[0]} нет в базе 🤥', chat)
                        print(f'    * Не нашел номера {number_found[0]} в базе')
                else:
                    send_message(f'"{text}" - Не номер 🥸', chat, keyboard_help)
                    print(f'    * Не номер {text}')
        except:
            send_message(f'Ты что-то не то отправил 🫣', chat, keyboard_help)
            print('    (#) Что-то пошло не так!')


def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)


def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)


def send_message(text, chat_id, reply_markup=None):
    text = urllib.parse.quote_plus(text)
    url = f"{URL}sendMessage?text={text}&chat_id={chat_id}"
    if reply_markup:
        url += f"&reply_markup={reply_markup}"
    get_url(url)


def send_photo(photo, chat_id, text=None, reply_markup=None, ):
    url = f"{URL}sendPhoto?chat_id={chat_id}"
    files = {'photo': open(photo, 'rb')}
    if text:
        text = urllib.parse.quote_plus(text)
        url += f'&caption={text}'
    if reply_markup:
        url += f"&reply_markup={reply_markup}"
    requests.post(url, files=files)


def get_latest_request_id():
    updates = get_updates()["result"]
    url = URL + "getUpdates?timeout=100"
    return updates[-1]["update_id"] + 1


def main():
    #db.setup()
    last_update_id = get_latest_request_id()
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)
        time.sleep(0.5)


if __name__ == '__main__':
    while (True):
        try:
            # 635201622 - id чата с StepaZet
            send_message(f'Бот поднят', 635201622)
            main()
        except Exception as e:
            send_message(f'Бот лег с ошибкой {str(e)}', 635201622)
            time.sleep(120)