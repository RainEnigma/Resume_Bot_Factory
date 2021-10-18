from telebot import types

from config.from_exel_file import text_message
from database.get_data import get_items_basket, get_some_data, get_past_orders, get_all_data


def start_keyboard(message):
    list_buttons = ['🥡Лапша',
                    '🍜Супы',
                    '🥗Салаты',
                    '🍟Гарниры',
                    '🍔Бургеры',
                    '🍩Сладости']

    list_about_buttons = ['✉Написать', 'Доставка/оплата', '🤠О нас']

    markup = types.InlineKeyboardMarkup(row_width=2)

    markup.add(*[types.InlineKeyboardButton(text=name, callback_data=f'first_{name}') for name in list_buttons])

    past_orders = len(get_past_orders(message.chat.id))
    # выпадает корзина если она не пуста!
    numb_items = len(get_items_basket(message.chat.id))
    if past_orders != 0 and numb_items != 0:
        button_b_po = [f'📦Корзина({numb_items})', '✅Вып. заказы']
        markup.add(*[types.InlineKeyboardButton(text=name, callback_data=f'first_{name}') for name in button_b_po])

    elif past_orders != 0:
        button_b_po = ['✅Вып. заказы']
        markup.add(*[types.InlineKeyboardButton(text=name, callback_data=f'first_{name}') for name in button_b_po])

    elif numb_items != 0:
        button_basket = [f'📦Корзина({numb_items})']
        markup.add(*[types.InlineKeyboardButton(text=name, callback_data=f'first_{name}') for name in button_basket])

    markup.row(*[types.InlineKeyboardButton(text=name, callback_data=f'first_{name}') for name in list_about_buttons])

    admins = [admin[0] for admin in get_all_data('admins', 'user_id')]
    if message.chat.id in admins:
        markup.add(types.InlineKeyboardButton(text='🛠Админпанель', callback_data='first_🛠Админпанель'))

    return markup


# генерация кнопок предидущих заказов
def buttons_past_order(tuple_orders):
    list_buttons_2 = ['◀Меню']
    text = 'Ваши заказы:\n\n'
    list_buttons = []
    for num, order in enumerate(tuple_orders):
        text += f'{num+1} - Заказ № {order[0]} ... {"{:%d.%m.%Y %H:%M}".format(order[1])}\n'
        list_buttons.append(order[0])

    markup = types.InlineKeyboardMarkup(row_width=4)
    markup.add(*[types.InlineKeyboardButton(text=num+1, callback_data=f'PastOrders_{name}') for num, name in enumerate(list_buttons)])
    markup.add(*[types.InlineKeyboardButton(text=name, callback_data=f'PastOrders_{name}') for name in list_buttons_2])
    return [text, markup]


def buttons_generator(num, category, call):
    # Колличество кнопок в блюдах
    if category == 'salads':
        end_num = int(text_message(15, 1))
    elif category == 'sup':
        end_num = int(text_message(16, 1))
    elif category == 'noodles':
        end_num = int(text_message(17, 1))
    elif category == 'garnish':
        end_num = int(text_message(18, 1))
    elif category == 'burger':
        end_num = int(text_message(19, 1))
    elif category == 'sweets':
        end_num = int(text_message(20, 1))
    num = int(num)

    if end_num >= 5:  # Если кнопок 5 и больше
        if num == 2:
            list_buttons = [f'1',
                            f'• {num} •',
                            f'{num + 1}',
                            f'{num + 2}',
                            f'{end_num}']

        elif num == end_num - 1:
            list_buttons = [f'1',
                            f'{num - 2}',
                            f'{num - 1}',
                            f'• {num} •',
                            f'{end_num}']

        elif num == end_num:
            list_buttons = [f'1',
                            f'{num - 3}',
                            f'{num - 2}',
                            f'{num - 1}',
                            f'• {num} •']

        elif num > 2:
            list_buttons = [f'1',
                            f'{num - 1}',
                            f'• {num} •',
                            f'{num + 1}',
                            f'{end_num}']

        else:
            list_buttons = [f'• {num} •',
                            f'{num + 1}',
                            f'{num + 2}',
                            f'{num + 3}',
                            f'{end_num}']

    elif end_num == 3:  # Если у нас только три блюда

        if num == 1:
            list_buttons = [f'• {num} •',
                            f'{num + 1}',
                            f'{end_num}']
        elif num == 2:
            list_buttons = [f'{num - 1}',
                            f'• {num} •',
                            f'{num + 1}']
        elif num == 3:
            list_buttons = [f'{num - 2}',
                            f'{num - 1}',
                            f'• {num} •']

    elif end_num == 4:  # Если у нас только четыре блюда
        if num == 1:
            list_buttons = [f'• {num} •',
                            f'{num + 1}',
                            f'{num + 2}',
                            f'{end_num}']
        elif num == 2:
            list_buttons = [f'{num - 1}',
                            f'• {num} •',
                            f'{num + 1}',
                            f'{end_num}']
        elif num == 3:
            list_buttons = [f'{num - 2}',
                            f'{num - 1}',
                            f'• {num} •',
                            f'{num + 1}', ]
        elif num == 4:
            list_buttons = [f'{num - 3}',
                            f'{num - 2}',
                            f'{num - 1}',
                            f'• {num} •']

    numb_items = len(get_items_basket(call.message.chat.id))
    if numb_items == 0:
        list_buttons_1 = ['⏬Добавить в корзину']
    else:
        list_buttons_1 = [f'📦Корзина({numb_items})', '⏬Добавить в корзину']

    list_buttons_2 = ['◀Меню']

    markup = types.InlineKeyboardMarkup(row_width=5)
    markup.add(*[types.InlineKeyboardButton(text=name, callback_data=f'{category}_{name}') for name in list_buttons])
    markup.add(*[types.InlineKeyboardButton(text=name, callback_data=f'basket_{name}') for name in list_buttons_1])

    markup.row(*[types.InlineKeyboardButton(text=name, callback_data=f'{category}_{name}') for name in list_buttons_2])

    return markup


# кнопки корзины
def basket_keyboard():
    list_buttons = ['✏Изменить', '☑Оформить']

    list_buttons_2 = ['◀Меню']

    markup = types.InlineKeyboardMarkup(row_width=2)

    markup.add(*[types.InlineKeyboardButton(text=name, callback_data=f'order_{name}') for name in list_buttons])
    markup.add(*[types.InlineKeyboardButton(text=name, callback_data=f'order_{name}') for name in list_buttons_2])

    return markup


# Кнопки редактирование корзины
def basket_redact_keyboard(list_buttons_del, call):
    list_buttons_del = set(list_buttons_del)
    numb_items = len(get_items_basket(call.message.chat.id))
    if numb_items == 0:
        list_buttons = ['◀Меню']
    else:
        list_buttons = [f'📦Корзина({numb_items})', '◀Меню']
    # что б вывести кнопки без повторений

    markup = types.InlineKeyboardMarkup(row_width=1)

    markup.add(*[types.InlineKeyboardButton(text=name.split('_')[0],
                                            callback_data=f"delete_{name.split('_')[1]}_{name.split('_')[2]}") for name
                 in list_buttons_del])
    markup.add(*[types.InlineKeyboardButton(text=name, callback_data=f'edit_{name}') for name in list_buttons])

    return markup


# Кнопки оплаты
def payment_keyboard():
    list_buttons = ['💵Наличные', '💳Картой курьеру']
    list_buttons_2 = ['💸Оплатить онлайн']
    list_buttons_3 = ['◀Меню']

    markup = types.InlineKeyboardMarkup(row_width=2)

    markup.add(*[types.InlineKeyboardButton(text=name, callback_data=f"payment1_{name}") for name in list_buttons])
    markup.add(*[types.InlineKeyboardButton(text=name, callback_data=f'payment1_{name}') for name in list_buttons_2])
    markup.add(*[types.InlineKeyboardButton(text=name, callback_data=f'payment1_{name}') for name in list_buttons_3])

    return markup


# Кнопки адрессов
def address_keyboard(message):
    markup = types.InlineKeyboardMarkup(row_width=3)

    list_address = get_some_data('address', 'address.address', message.chat.id)
    text_forming = 'Выберите адрес из раннее вводимых Вами:\n\n'
    list_buttons = []
    for num, button in enumerate(list_address):
        text_forming += f'{num + 1} - {button}\n'
        list_buttons.append(num + 1)
    text_forming += '\nИли введите новый адрес:'
    markup.add(*[types.InlineKeyboardButton(text=name, callback_data=f"address_{name-1}") for name in list_buttons])

    return [markup, text_forming]


# Кнопка запомнить адресс
def remember_address_keyboard():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton(text='СОХРАНИТЬ', callback_data=f"save_address"))

    return markup


# Кнопка выполненные заказы
def past_orders_button():
    markup = types.InlineKeyboardMarkup(row_width=1)
    buttons_list= ['✅Вып. заказы', '◀Меню']
    markup.add(*[types.InlineKeyboardButton(text=name, callback_data=f'first_{name}') for name in buttons_list])

    return markup


# Кнопки Админпанели_1
def admin_pan_1_keyboard(status):

    if status == '🦸‍♂Супер-Админ':
        list_buttons = ['🕹Админ-менеджер', '🙋‍♂Заказы', 'ℹКлиент-инфо', '📮Рассылка', '👤Все клиенты' ]

    elif status == '👨‍💻‍Администратор':
        list_buttons = ['🙋‍♂Заказы', 'ℹКлиент-инфо', '📮Рассылка']

    elif status == '🧑‍🎨Модератор':
        list_buttons = ['🕹Админ-менеджер', '🙋‍♂Заказы', 'ℹКлиент-инфо', '📮Рассылка']

    list_buttons_3 = ['◀Меню']

    markup = types.InlineKeyboardMarkup(row_width=2)

    markup.add(*[types.InlineKeyboardButton(text=name, callback_data=f"admin1_{name}") for name in list_buttons])
    markup.add(*[types.InlineKeyboardButton(text=name, callback_data=f'admin1_{name}') for name in list_buttons_3])

    return markup


# Кнопки менеджер админов
def admin_manage_keyboard(list_buttons=None, argum = None):
    list_buttons_2 = ['➕Добавить нового админа']
    list_buttons_3 = ['⬅Назад', '◀Меню']

    markup = types.InlineKeyboardMarkup(row_width=2)

    if list_buttons is not None:
        markup.add(*[types.InlineKeyboardButton(text=name, callback_data=f"manageAdmin_{name}") for name in list_buttons])
    if argum is None:
        markup.add(*[types.InlineKeyboardButton(text=name, callback_data=f"manageAdmin_{name}") for name in list_buttons_2])
    markup.add(*[types.InlineKeyboardButton(text=name, callback_data=f'manageAdmin_{name}') for name in list_buttons_3])

    return markup


# Кнопки /добавить  админов
def admin_manag_keyboard(list_buttons):
    list_buttons_3 = ['⬅Назад', '◀Меню']

    markup = types.InlineKeyboardMarkup(row_width=2)

    markup.add(*[types.InlineKeyboardButton(text=name, callback_data=f"manageAdmin_{name}") for name in list_buttons])
    markup.add(*[types.InlineKeyboardButton(text=name, callback_data=f'manageAdmin_{name}') for name in list_buttons_3])


# Кнопки указать уровень нового админа
def new_admin_level(id_new_admin):
    list_buttons = ['🦸‍♂Супер-Админ', '👨‍💻‍Администратор', '🧑‍🎨Модератор']
    list_buttons_3 = ['⬅Назад', '◀Меню']

    markup = types.InlineKeyboardMarkup(row_width=2)

    markup.add(*[types.InlineKeyboardButton(text=name, callback_data=f"manageRole_{name}_{id_new_admin}") for name in list_buttons])
    markup.add(*[types.InlineKeyboardButton(text=name, callback_data=f'manageRole_{name}') for name in list_buttons_3])

    return markup


# Кнопки получить данные по ID
def get_user_id_keyboard():
    list_buttons_3 = ['⬅Назад', '◀Меню']
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(*[types.InlineKeyboardButton(text=name, callback_data=f'manageRole_{name}') for name in list_buttons_3])

    return markup