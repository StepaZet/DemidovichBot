import time
import json
import telegram_methods as tg
import re
import logging
import sys
import asyncio

def build_keyboard_help():
    reply_markup = {"keyboard": [['/help'],['❤️']], "one_time_keyboard": False, "resize_keyboard": True}
    return json.dumps(reply_markup)

simple_statistic = set()
keyboard_help = build_keyboard_help()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler(sys.stdout)
    ]
)


async def process_update(update: dict) -> None:
    logs = []

    for key in update:
        if type(update[key]) is dict and 'chat' in update[key]:
            logs.append(f"Запрос принят от {update[key]['chat']['username']}")
            break

    if 'edited_message' in update:
        simple_statistic.add(update['edited_message']['chat']['id'])
        await tg.async_send_message('Ты изменил какое-то сообщение -.-', update['edited_message']['chat']['id'])
        for log in logs:
            logging.info(log)
        logging.info(f"Измененное сообщение")
        return

    if 'message' not in update:
        simple_statistic.add(update['my_chat_member']['chat']['id'])
        await tg.async_send_message('Такого функционала пока нет', update['my_chat_member']['chat']['id'])
        for log in logs:
            logging.info(log)
        logging.info(f'Кто-то подписался или отписался')
        return

    chat = update["message"]["chat"]["id"]
    simple_statistic.add(chat)
    try:
        text = update["message"]["text"]

        if text == '/start':
            await tg.async_send_message(
                'Привет! Напиши номер задачки из Демидовича, '
                'которую хочешь получить', chat, keyboard_help)
            for log in logs:
                logging.info(log)
            logging.info("    * Отправил /start")
        elif text == '/help':
            await tg.async_send_message(
                'Привет! Бот может отправить тебе номер из демидовича \n'
                'Пиши ему номер задания по типу:\n652 или 652.1 \n\n'
                'Пока отправляем только картинку условия (ответов и решений нет, увы) \n'
                'Если номер не найден, но ты знаешь, что он точно есть, '
                'попробуй отправить соседние номера \n(или, если это номер с точкой как 123.4, '
                'попробуй отправить только целую часть (123))\n\n'
                'Если будут любые проблемы, пиши авторам: @therealnowhereman, @Demotivator_Stepan, @not_amigo\n'
                'Удачи!) 🥰', chat)
            for log in logs:
                logging.info(log)
            logging.info('    * Отправил /help')
        elif text == '❤️':
            await tg.async_send_message(f'❤️', chat)
            for log in logs:
                logging.info(log)
            logging.info('    * Отправил сердечко')
        elif text == '/stat':
            await tg.async_send_message(
                f'Cегодня бота юзали {len(simple_statistic)} человек 😱', chat)
            for log in logs:
                logging.info(log)
            logging.info("    * Отправил статистику")
        else:
            number_found = re.fullmatch(r'\d*\.?(\d*)?', text)
            if number_found:
                if tg.is_file_exist(f'images/{number_found[0]}.gif'):
                    await tg.async_send_photo(f'images/{number_found[0]}.gif', chat,
                                     f'Вот твой номер {number_found[0]} 😘')
                    for log in logs:
                        logging.info(log)
                    logging.info(f'    * Отправил номер {number_found[0]}')
                else:
                    possible_number = number_found[0].split('.')[0]
                    await tg.async_send_message(f'Не могу найти номер {number_found[0]} в базе 🤥', chat)

                    logs.append(f'    * Не нашел номера {number_found[0]} в базе')

                    if tg.is_file_exist(f'images/{possible_number}.gif'):
                        await tg.async_send_photo(f'images/{possible_number}.gif', chat,
                                         f'Возможно, твой номер есть на картинке с номером {possible_number} 🙄')
                        for log in logs[:-1]:
                            logging.info(log)
                        logging.warning(logs[-1])
                        logging.info(f'    * Отправил возможный номер {possible_number}')

            else:
                await tg.async_send_message(f'"{text}" - Не могу распознать номер 🥸\n'
                                   f'Номера имею вид:\n'
                                   f'652 и 652.1', chat, keyboard_help)
                for log in logs:
                    logging.info(log)
                logging.info(f'    * Не номер "{text}"')
    except Exception as e:
        await tg.async_send_message(f'Ты что-то не то отправил 🫣', chat, keyboard_help)
        for log in logs:
            logging.info(log)
        logging.error(f"    * Что-то пошло не так! {str(e)}")


async def handle_updates(updates):
    futures = [process_update(update) for update in updates["result"]]
    for future in asyncio.as_completed(futures):
        await future


async def start():
    last_update_id = tg.get_latest_request_id()
    while True:
        updates = tg.get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = tg.get_last_update_id(updates) + 1
            await handle_updates(updates)
        time.sleep(0.5)


async def main():
    while True:
        try:
            # 635201622 - id чата с StepaZet
            await tg.async_send_message(f'Бот поднят', 635201622)
            await start()
        except Exception as e:
            await tg.async_send_message(f'Бот лег с ошибкой {str(e)}', 635201622)
            time.sleep(120)

if __name__ == '__main__':
    while True:
        ioloop = asyncio.new_event_loop()
        top_dict = ioloop.run_until_complete(main())
        ioloop.close()
