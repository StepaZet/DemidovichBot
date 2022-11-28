import telebot

from telebot import types
from provider import Provider
from subject_type import SubjectType
from task import TaskType, Task
from provider import ProviderError

TOKEN = '5487430726:AAGd7xMlvZaYOJ3wTP4JVokW16NWy4oD31Q'
bot: telebot.TeleBot = telebot.TeleBot(TOKEN)
provider: Provider = Provider()


def build_start_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Демидович'))
    keyboard.add(types.KeyboardButton('Тервер (ФИИТ)'))
    keyboard.add(types.KeyboardButton('/Помощь'))
    return keyboard


def build_book_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard.add(types.KeyboardButton('Демидович'))
    keyboard.add(types.KeyboardButton('Тервер (ФИИТ)'))
    keyboard.add(types.KeyboardButton('❤️'))
    keyboard.add(types.KeyboardButton('/Помощь'))
    return keyboard


@bot.message_handler(commands=['start'])
def start_message(message):
    start_text = ...
    keyboard = build_start_keyboard()
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


@bot.message_handler(content_types=['text'])
def message_handler(message):
    button_requests = {
        'Демидович': ('Выбран Демидович\n'
                      'Напиши номер(а) задачи(задачек, через пробел)',
                      SubjectType.DEMIDOVICH),
        'Тервер (ФИИТ)': ('Выбран Тервер (ФИИТ)\n'
                          'Напиши номер(а) задачи(задачек, через пробел)',
                          SubjectType.PROBABILITIES),
        '❤️': ('Спасибо за лайк!', None),
    }

    if message.text in button_requests:
        text, subject_type = button_requests[message.text]
        bot.send_message(message.chat.id, text)
        if subject_type:
            provider.set_user_mode(message.chat.id, subject_type)
    else:
        tasks = try_get_tasks(message.chat.id, message.text)
        if isinstance(tasks, str):
            bot.send_message(message.chat.id, tasks, reply_markup=build_start_keyboard())
            return

        for task in tasks:
            if task.task_type == TaskType.TEXT:
                bot.send_message(message.chat.id, task.text)
            elif task.task_type == TaskType.PHOTO:
                with open(task.data, 'rb') as photo:
                    bot.send_photo(message.chat.id, photo, caption=task.text)


if __name__ == '__main__':
    bot.polling()
