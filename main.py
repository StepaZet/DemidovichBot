import telebot

from telebot import types
from provider import Provider
from subject_type import SubjectType
from task import TaskType, Task
from provider import ProviderError

TOKEN = '5487430726:AAGd7xMlvZaYOJ3wTP4JVokW16NWy4oD31Q'
bot: telebot.TeleBot = telebot.TeleBot(TOKEN)
provider: Provider = Provider()


def _build_start_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Демидович'))
    keyboard.add(types.KeyboardButton('Тервер (ФИИТ)'))
    keyboard.add(types.KeyboardButton('/Помощь'))
    return keyboard


def _build_book_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Демидович'))
    keyboard.add(types.KeyboardButton('Тервер (ФИИТ)'))
    keyboard.add(types.KeyboardButton('❤️'))
    keyboard.add(types.KeyboardButton('/Помощь'))
    return keyboard


@bot.message_handler(commands=['start'])
def start_message(message):
    start_text = ...
    keyboard = _build_start_keyboard()
    bot.send_message(message.chat.id, start_text, reply_markup=keyboard)


@bot.message_handler(commands=['Помощь'])
def help_message(message):
    help_text = ...
    bot.send_message(message.chat.id, help_text)


@bot.message_handler(commands=['Статистика'])
def stat_message(message):
    stat_text = ...
    bot.send_message(message.chat.id, stat_text)


def try_get_tasks(chat_id: int, message: str) -> list[Task] | str:
    try:
        return provider.get_tasks(str(chat_id), message)
    except ProviderError as e:
        return 'Ты не выбрал режим'


def try_handle_button_request(message: types.Message) -> bool:
    button_requests = {
        'Демидович':
            ('Выбран Демидович\n'
             'Напиши номер(а) задачи(задачек, через пробел)',
             lambda: provider.set_user_mode(str(message.chat.id),
                                            SubjectType.DEMIDOVICH)),
        'Тервер (ФИИТ)':
            ('Выбран Тервер (ФИИТ)\n'
             'Напиши номер(а) задачи(задачек, через пробел)',
             lambda: provider.set_user_mode(str(message.chat.id),
                                            SubjectType.PROBABILITIES)),
        '❤️':
            ('Спасибо за лайк!',
             lambda: None),
    }

    if message.text in button_requests:
        text, _function = button_requests[message.text]
        bot.send_message(message.chat.id, text,
                         reply_markup=_build_book_keyboard())
        _function()
        return True
    return False


@bot.message_handler(content_types=['text'])
def message_handler(message: types.Message):
    if try_handle_button_request(message):
        return

    tasks = try_get_tasks(message.chat.id, message.text)
    if isinstance(tasks, str):
        bot.send_message(message.chat.id, tasks,
                         reply_markup=_build_start_keyboard())
        return

    for task in tasks:
        if task.task_type == TaskType.TEXT:
            bot.send_message(message.chat.id, task.data)
        elif task.task_type == TaskType.PHOTO:
            with open(task.data, 'rb') as photo:
                bot.send_photo(message.chat.id, photo, caption=task.text)


if __name__ == '__main__':
    bot.polling()
