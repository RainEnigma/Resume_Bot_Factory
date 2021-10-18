from telebot import types

from config import config


def start_keyboard(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)

    keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['🆘 Помошь', '📋О нас']])

    if message.from_user.id in config.list_admins:
        keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['🔑 Администрирование']])

    return keyboard


def go_to_main_keyboard(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.add(*[types.InlineKeyboardButton(text=name, callback_data=name) for name in ['']])

    return keyboard


def contact_keyboard(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    butContact = types.KeyboardButton(text='📲 Отправить мой номер телефона', request_contact=True)
    markup.add(butContact)

    return markup
