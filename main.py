import datetime
import time
import os

import telebot
from functools import lru_cache

from telebot import types

from database import Database
from provider import Provider
from task_provider import TaskProvider
from subject_type import SubjectType
from task import TaskType, Task
from file_manager import FileManager
from sqlite_wrapper import add_task


TOKEN = os.getenv('DEMIDOVICH_BOT_TOKEN')
assert (
        TOKEN is not None
), 'Токен не найден'

bot: telebot.TeleBot = telebot.TeleBot(TOKEN)
db = Database("Users")
provider: Provider = Provider()
provider.event += add_task


@lru_cache()
def _get_tasks_providers_classes() -> list[type[TaskProvider]]:
    # TODO: Убрать этот метод в Provider
    return [_provider for _provider in TaskProvider.__subclasses__()]


@lru_cache()
def _build_start_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for _provider in _get_tasks_providers_classes():
        keyboard.add(types.KeyboardButton(_provider.button_name))
    keyboard.add(types.KeyboardButton('/help'))
    return keyboard


@lru_cache()
def _build_book_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for _provider in _get_tasks_providers_classes():
        keyboard.add(types.KeyboardButton(_provider.button_name))
    keyboard.add(types.KeyboardButton('❤️'))
    keyboard.add(types.KeyboardButton('/help'))
    return keyboard


@lru_cache()
def _get_button_request_handlers() -> dict[str, callable]:
    button_requests = {
        '❤️': ('Спасибо за лайк!❤️🥰', lambda chat_id: None),
    }

    # Боремся с замыканием _provider.subject_type
    def set_user_mode(mode: SubjectType):
        def _set_user_mode(chat_id: int):
            provider.set_user_mode(str(chat_id), mode)
        return _set_user_mode

    for _provider in _get_tasks_providers_classes():
        button_requests[_provider.button_name] = (
            _provider.button_message,
            set_user_mode(_provider.subject_type))

    return button_requests


@bot.message_handler(commands=['start'])
def start_message(message):
    start_text = 'Привет! Выбери нужный тебе задачник:'
    keyboard = _build_start_keyboard()
    bot.send_message(message.chat.id, start_text, reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def help_message(message):
    help_text = 'Для начала работы выбери нужный тебе задачник.\n' \
                'После этого напиши номер задачи, которую хочешь найти. Например, 10.1 или 42\n\n' \
                'Если хочешь найти несколько задач, то напиши их через пробел, запятую или дефис.\n' \
                'Например: 1, 2, 3 или 1-3 или 1 2 3\n\n' \
                'Если будут любые проблемы, пиши авторам: ' \
                '@therealnowhereman, @Demotivator_Stepan, @not_amigo Удачи!) 🥰'
    bot.send_message(message.chat.id, help_text)


@bot.message_handler(commands=['stats'])
def stat_message(message):
    stat_text = Provider.get_statistic()
    bot.send_message(message.chat.id, stat_text)


def try_get_tasks(chat_id: int, message: str) -> list[Task] | None:
    try:
        mode = db.get_by_key(str(chat_id))
        return provider.get_tasks(SubjectType(mode), message)
    except KeyError as e:
        return None


def try_handle_button_request(message: types.Message) -> bool:
    button_requests = _get_button_request_handlers()

    if message.text in button_requests:
        text, _function = button_requests[message.text]
        bot.send_message(message.chat.id, text,
                         reply_markup=_build_book_keyboard())
        _function(message.chat.id)
        return True
    return False


def handle_photo_responses(message: types.Message, tasks: list[Task]):
    if len(tasks) >= 1:
        print(tasks[0].text)

    if len(tasks) == 1:
        with open(tasks[0].data, 'rb') as photo:
            try:
                bot.send_photo(message.chat.id, photo, caption=tasks[0].text)
            except Exception as e:
                bot.send_message(message.chat.id, 'Файл в базе поврежден')
    elif len(tasks) > 1:
        file_names = [task.data for task in tasks]
        capture = 'Держи найденные номера'
        if len(tasks) == 10:
            capture += '\n(максимум 10)'

        with FileManager(file_names) as files:
            medias = []
            for i, file in enumerate(files):
                medias.append(types.InputMediaPhoto(file))
            medias[0].caption = capture
            try:
                bot.send_media_group(message.chat.id, medias)
            except Exception as e:
                bot.send_message(message.chat.id,
                                 'Один из файлов в базе поврежден')


def handle_text_responses(message: types.Message, tasks: list[Task]):
    if len(tasks) >= 1:
        print(tasks[0].text)

    if len(tasks) == 1:
        bot.send_message(message.chat.id, tasks[0].data)
    elif len(tasks) > 1:
        text = 'Держи найденные задания:\n'
        if len(tasks) == 10:
            text += '(максимум 10)\n'
        for task in tasks:
            text += f'{task.data}\n\n'
        bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=['text'])
def message_handler(message: types.Message):
    print(datetime.datetime.now(), message.chat.username, message.text)
    if try_handle_button_request(message):
        return

    if not (tasks := try_get_tasks(message.chat.id, message.text)):
        bot.send_message(message.chat.id, "Ты не выбрал задачник",
                         reply_markup=_build_start_keyboard())
        return

    responses_photo = [task for task in tasks
                       if task.task_type == TaskType.PHOTO]
    responses_text = [task for task in tasks
                      if task.task_type == TaskType.TEXT]
    if responses_photo:
        handle_photo_responses(message, responses_photo)
    if responses_text:
        handle_text_responses(message, responses_text)

    if not responses_photo and not responses_text:
        print('No tasks found')
        bot.send_message(message.chat.id, 'Не смог обработать твой запрос :(')


def clear_old_updates():
    updates = bot.get_updates()
    if len(updates) > 0:
        last_update = updates[-1]
        bot.get_updates(offset=last_update.update_id + 1)


if __name__ == '__main__':
    # Заполняем кэш долгого метода
    _get_tasks_providers_classes()
    clear_old_updates()
    while True:
        try:
            bot.polling(non_stop=True, timeout=100)
        except Exception as e:
            bot.send_message(635201622, f'Бот упал с ошибкой: {e}')
            time.sleep(5)
