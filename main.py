import datetime
import os
import telebot
import time

from functools import lru_cache, partial
from telebot import types
from database import Database
from task_provider import TaskProvider, get_providers
from subject_type import SubjectType
from task import TaskType, Task
from file_manager import FileManager
from stat_repo import StatRepo, add_stat
from event import Event
from stat_builder import StatBuilder

TOKEN = os.getenv('DEMIDOVICH_BOT_TOKEN')

assert TOKEN is not None, 'Токен не найден'

ADMINS = [
    635201622,
    453148886,
    413639483
]

bot: telebot.TeleBot = telebot.TeleBot(TOKEN)
db = Database("Users")
event = Event()
event += partial(add_stat, StatRepo())


def set_user_mode(user_id: int, mode: SubjectType):
    db.set(str(user_id), mode.value)


@lru_cache()
def _build_start_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for _provider in get_providers():
        keyboard.add(types.KeyboardButton(_provider.button_name))
    keyboard.add(types.KeyboardButton('/help'))
    return keyboard


@lru_cache()
def _build_book_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    for _provider in get_providers():
        keyboard.add(types.KeyboardButton(_provider.button_name))
    keyboard.add(types.KeyboardButton('❤️'))
    keyboard.add(types.KeyboardButton('/help'))
    return keyboard


@lru_cache()
def _get_button_request_handlers() -> dict[str, callable]:
    button_requests = {
        '❤️': ('Спасибо за лайк!❤️🥰', lambda chat_id: None),
    }

    for _provider in get_providers():
        button_requests[_provider.button_name] = (
            _provider.button_message,
            partial(set_user_mode, mode=_provider.subject_type)
        )

    return button_requests


@bot.message_handler(commands=['start'])
def start_message(message):
    start_text = 'Привет! Выбери нужный тебе задачник:'
    keyboard = _build_start_keyboard()
    bot.send_message(message.chat.id, start_text, reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def help_message(message):
    help_text = (
        'Для начала работы выбери нужный тебе задачник.\n'
        'После этого напиши номер задачи, которую хочешь найти. Например, 10.1 или 42\n\n'  # noqa: E501
        'Если хочешь найти несколько задач, то напиши их через пробел, запятую или дефис.\n'  # noqa: E501
        'Например: 1, 2, 3 или 1-3 или 1 2 3\n\n'
        'Если будут любые проблемы, пиши авторам: '
        '@therealnowhereman, @Demotivator_Stepan, @not_amigo Удачи!) 🥰'
    )
    bot.send_message(message.chat.id, help_text)


@bot.message_handler(commands=['stats'])
def stat_message(message):
    words = message.text.split()[1:]
    if words is None or len(words) == 0:
        bot.send_message(message.chat.id, StatRepo().build())
        return
    stat_texts = StatBuilder().build(words)
    bot.send_message(message.chat.id, '\n\n'.join(stat_texts))


def try_get_tasks(chat_id: int, message: str) -> list[Task] | None:
    try:
        mode = SubjectType(db.get_by_key(str(chat_id)))
        provider = TaskProvider.get_provider_by_subject_type(mode)
        answer = provider.get_tasks(message)
        event(chat_id=chat_id, message=message, answer=answer, mode=mode)
        return answer
    except KeyError:
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
            except Exception:
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
            except Exception:
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
    get_providers()
    clear_old_updates()
    while True:
        for admin in ADMINS:
            bot.send_message(admin, 'Я живой!')

        try:
            bot.polling(non_stop=True, timeout=100)
        except Exception as e:
            for admin in ADMINS:
                bot.send_message(admin, f'Я упал с ошибкой: {e}')
            time.sleep(5)
