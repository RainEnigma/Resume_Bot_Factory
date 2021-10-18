import re

import telebot
from telebot import types
from telebot.apihelper import ApiException

from admin_work import admin_work, admin_manage, adding_new_admin, admin_manager
from basket import in_basket
from basket_redaction import basket_redact, deleting_from_basket
from config import config
from config.from_exel_file import text_message
from database import tables_exists, creating_tables, insert_data_to_tables
from database.get_data import get_user_stage, get_some_data
from database.update_data import update_some_data, update_user_stage, update_user_totally_buy, adding_address
from filling_basket import basket_work
from finish_func import finish_funk
from get_user_info import show_user_data
from keyboards import inline_keyboards
from menu.menu import admin_pan, big_cifr_func, menu
from order_registration import order_registration_1, order_registration_2, order_registration_3, order_registration_4
from show_past_order import show_past_order

bot = telebot.TeleBot(config.token, threaded=True)

# запуск ф-ции для создания таблиц в базе данных
list_tab_not_exists = tables_exists.tables_exists(['users', 'admins', 'baskets', 'menu', 'address', 'orders_done'])
if 'users' in list_tab_not_exists:
    creating_tables.create_table_users('users')

if 'menu' in list_tab_not_exists:
    creating_tables.create_table_menu('menu')

if 'admins' in list_tab_not_exists:
    creating_tables.create_table_admins('admins')
    insert_data_to_tables.insert_start_admins()

if 'baskets' in list_tab_not_exists:
    creating_tables.create_table_baskets('baskets')

if 'address' in list_tab_not_exists:
    creating_tables.create_table_address('address')

if 'orders_done' in list_tab_not_exists:
    creating_tables.create_table_orders_done('orders_done')


@bot.message_handler(commands=['start'])
def start(message, marker=None):
    stage = get_user_stage(message.chat.id)
    if stage == 'payment_chosen':  # если сформирован инвойс но не оплачен
        try:
            id_message = get_some_data('baskets', 'additional', message.chat.id)
            bot.delete_message(message.chat.id, id_message)  # удаляем invoice!
            update_some_data('baskets', 'additional', None, message.chat.id)

            # пробуем удалить все сообщения
            for id_mes in range(message.message_id - 2, message.message_id + 2):
                try:
                    bot.delete_message(message.chat.id, id_mes)
                except:
                    pass

            bot.send_message(chat_id=message.chat.id,
                             text='Интернет-оплата отменена!\nВы в главном меню:',
                             reply_markup=inline_keyboards.start_keyboard(message))
            update_user_stage('main_menu', message.chat.id)
        except:
            pass

    else:
        if marker is None and get_user_stage(message.chat.id) is None:  # если первый раз нажимает на старт

            # Добавление нового пользователя в таблицу users
            insert_data_to_tables.insert_user_to_table(message)

            # отправляем приветствие
            # bot.send_sticker(message.chat.id, open(config.path_image_logo, 'rb'))

            marker = f"{text_message(1, 1)}"

            bot.send_message(chat_id=message.chat.id,
                             text=marker,
                             reply_markup=inline_keyboards.start_keyboard(message))
            update_user_stage('main_menu', message.chat.id)
        else:
            if get_some_data('baskets',
                             'order_payment',
                             message.chat.id) != 'internet_payment_approved':  # если оплачен но не завершен заказ
                try:
                    bot.edit_message_text(chat_id=message.chat.id,
                                          message_id=message.message_id,
                                          text=marker,
                                          reply_markup=inline_keyboards.start_keyboard(message))

                except ApiException as e:
                    if e.result.content == b'{"ok":false,"error_code":400,"description":"Bad Request: message is not modified: specified new message content and reply markup are exactly the same as a current content and reply markup of the message"}':
                        pass
                    else:
                        bot.send_message(chat_id=message.chat.id,
                                     text='Вы в главном меню:',
                                     reply_markup=inline_keyboards.start_keyboard(message))
                update_user_stage('main_menu', message.chat.id)
            else:
                bot.send_message(message.chat.id, text_message(6, 1))
                order_registration_3(message, bot)


@bot.message_handler(content_types=["contact"])
def contact(message):
    if message.chat.id == message.contact.user_id:
        number = message.contact.phone_number
        update_some_data('users', 'telephone', number, message.chat.id)
        bot.delete_message(message.chat.id,message.message_id)
        order_registration_4(message, bot)
    else:
        bot.send_message(message.chat.id, "Вы передали сторонний контакт, передайте пожалуйста свой:")


@bot.message_handler(commands=['help'])
def help_func(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_start = types.KeyboardButton("/start")
    markup.row(button_start)
    bot.send_message(message.chat.id,
                     text_message(2, 1),
                     reply_markup=markup, parse_mode='markdown')


@bot.message_handler(content_types=['text'])
def func_1(message):
    stage = get_user_stage(message.chat.id)
    if stage == 'adding_new_admin':
        adding_new_admin(message, bot)

    elif stage == 'get_user_info':
        show_user_data(message, bot)

    elif message.text[0] == '0' \
            and get_user_stage(message.chat.id) == 'inserting_phone' \
            and message.text.isdigit() \
            and len(message.text) == 10:
        update_some_data('users', 'telephone', f'38{message.text}', message.chat.id)
        bot.delete_message(message.chat.id, message.message_id)
        order_registration_4(message, bot)

    if message.text != get_some_data('users', 'telephone',message.chat.id).lstrip('38') \
            and get_user_stage(message.chat.id) == 'entering_address':
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass
        update_some_data('baskets', 'temp_address', message.text, message.chat.id)
        bot_message = bot.edit_message_text(chat_id=message.chat.id,
                                            message_id=get_some_data('baskets', 'additional', message.chat.id),
                                            disable_web_page_preview=False,
                                            text=f'{text_message(4, 2).split("_")[0]}\n\n{message.text}\n\n{text_message(4, 2).split("_")[1]}',
                                            reply_markup=inline_keyboards.remember_address_keyboard(),
                                            parse_mode='html')
        update_some_data('baskets', 'additional', bot_message.message_id,message.chat.id)




'''ПРИЕМ ОПЛАТЫ'''


@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                  error_message="Извините, что-то пошло не так.")


@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    money_received = message.successful_payment.total_amount / 100
    update_user_totally_buy(money_received, message.chat.id)
    try:
        bot.delete_message(message.chat.id, message_id=message.message_id - 2)
    except Exception as e:
        print(e)
    update_some_data('baskets', 'order_payment', 'internet_payment_approved', message.chat.id)
    order_registration_3(message, bot, 'internet_payment')


'''/ПРИЕМ ОПЛАТЫ'''


@bot.callback_query_handler(func=lambda call: True)
def main_menu(call):
    stage = get_user_stage(call.message.chat.id)
    if call.message and get_some_data('baskets', 'order_payment', call.message.chat.id) != 'internet_payment_approved':

        if call.data.split('_')[1] == '◀Меню':
            start(call.message, text_message(1, 2))

        elif call.data.split('_')[1] == '⬅Назад':
            if stage == 'admin_manager':
                admin_pan(call, bot)
            elif stage == 'adding_new_admin':
                admin_manager(call, bot)
            elif stage == 'adding_role_new_admin':
                admin_manager(call, bot)
            elif stage == 'get_user_info':
                admin_pan(call, bot)

        elif call.data.split('_')[0] == 'PastOrders':
            show_past_order(call, bot)

        elif call.data.split('_')[0] == 'manageAdmin':
            admin_manage(call, bot)

        elif call.data.split('_')[0] == 'manageRole':
            id_new_admin = call.data.split('_')[2]
            update_some_data('admins', 'level', call.data.split('_')[1], id_new_admin)
            name_admin = get_some_data('users', 'user_name', id_new_admin)
            update_some_data('admins', 'name', f'@{name_admin}', id_new_admin)
            admin_manager(call, bot)

        elif call.data.split('_')[1] == '🤠О нас':
            update_user_stage('about_us', call.message.chat.id)
            start(call.message, text_message(3, 1))

        elif call.data.split('_')[1] == 'Доставка/оплата':
            update_user_stage('shipping_payments', call.message.chat.id)
            start(call.message, text_message(8, 1))

        elif call.data.split('_')[0] == 'delete':
            deleting_from_basket(f"{call.data.split('_')[1]}_{call.data.split('_')[2]}", call, bot)

        elif call.data.split('_')[1] == '✏Изменить':
            basket_redact(call, bot)

        elif call.data.split('_')[0] == 'admin1':
            admin_work(call, bot)

        elif call.data.split('_')[1][0] == '📦':
            in_basket(call, bot)

        # функция генерации кнопок в категории блюд
        elif call.data.split('_')[1] in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'] \
                and call.data.split('_')[0] != 'address':
            big_cifr_func(call, bot)

        elif call.data.split('_')[0] == 'first':
            menu(call, bot)

        elif call.data.split('_')[0] == 'param':
            pass

        elif call.data.split('_')[0] == 'basket':
            list_menu_names = {'sup', 'salads', 'noodles', 'garnish', 'burger', 'sweets'}
            if stage.split('_')[0] in list_menu_names:
                basket_work(call, bot)

            else:
                print(f'{stage} is not in {list_menu_names}')

        elif call.data.split('_')[1] == '☑Оформить':
            order_registration_1(call, bot)

        elif call.data.split('_')[0] == 'payment1':
            order_registration_2(call, bot)
    if call.message:
        if call.data.split('_')[0] == 'address':
            finish_funk(call, bot)

        if call.data == 'save_address':
            new_address = get_some_data('baskets', 'temp_address', call.message.chat.id)
            new_address = re.sub(r","," ", new_address)
            new_address = re.sub(r"  ", " ", new_address)
            adding_address(new_address,call.message.chat.id)
            update_some_data('baskets', 'address', new_address, call.message.chat.id)
            order_registration_4(call.message,bot)



if __name__ == '__main__':
    try:
        bot.polling()

    except Exception as e:
        print(f"bot_poling - {e}")
