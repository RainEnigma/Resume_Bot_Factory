import re

from telebot.types import LabeledPrice

from config.from_exel_file import text_message
from database.get_data import get_basket_total_price, get_telephone_number, get_user_address, get_some_data
from database.update_data import update_some_data, update_user_stage
from keyboards import inline_keyboards
from keyboards.keyboards import contact_keyboard


# Кнопки с выбором вида оплаты (наличные, безналичные, интернет-оплата)
def order_registration_1(call, bot):
    update_user_stage('payment1_PayTypeChoice', call.message.chat.id)
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          disable_web_page_preview=False,
                          text=f'{text_message(4, 1)}',
                          reply_markup=inline_keyboards.payment_keyboard(),
                          parse_mode='html')


# слушаем кнопки (наличные, безналичные, интернет-оплата)
def order_registration_2(call, bot):
    button_pressed = call.data.split('_')[1]
    update_user_stage('payment_chosen', call.message.chat.id)
    if button_pressed == '💵Наличные':
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id+1)
        except:
            pass
        update_some_data('baskets', 'order_payment', 'cash', call.message.chat.id)
        order_registration_3(call.message, bot)

    elif button_pressed == '💳Картой курьеру':
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id+1)
        except:
            pass
        update_some_data('baskets', 'order_payment', 'card', call.message.chat.id)
        order_registration_3(call.message, bot)

    elif button_pressed == '💸Оплатить онлайн':
        pay_money(call.message, bot)

    ''' Функция по оплате'''
# Вторая часть находится в main.py


def pay_money(message, bot):
    try:
        bot.delete_message(message.chat.id, get_some_data('baskets', 'additional', message.chat.id))
    except:
        pass
    order_num = get_basket_total_price('numb', message.chat.id)
    total_price = get_basket_total_price('total_price', message.chat.id)
    total_price = int(100 * int(total_price))

    prices = [LabeledPrice(label='Он-лайн заказ кафе "Bot_Factory"', amount=total_price)]
    user_order_text = re.sub(r"[</b>]", "", get_some_data("baskets", "order_text", message.chat.id))
    mess = bot.send_invoice(message.chat.id, title=f'Он-лайн заказ №{order_num}',
                     description=f'{user_order_text}\n\nВнимание! Это тестовое пополнение. Введите следующие данные тестовой карты:\n'
                                 f'4242 4242 4242 4242\n'
                                 f'любую дату окончания карты и любой СVV код',
                     provider_token='632593626:TEST:sandbox_i79618987909',
                     currency='uah',
                     is_flexible=False,  # True If you need to set up Shipping Fee
                     prices=prices,
                     start_parameter='Buy_goods_test',
                     invoice_payload='Поздравляю')
    update_some_data('baskets', 'additional', mess.message_id, message.chat.id)


# слушаем номер телефона
def order_registration_3(message, bot, marker=None):
    update_user_stage('inserting_phone', message.chat.id)
    update_some_data('baskets', 'additional', message.message_id, message.chat.id)

    if get_telephone_number(message.chat.id) is not None:  # Если есть номер телефона то переходим в 4 шаг
        order_registration_4(message, bot)
        # ПОДУМАТЬ!!! Оставить номер без изменений или внести новый + убрать кнопку отправки номера телефона
    else:
        markup = contact_keyboard(message)
        if marker is None:
            try:
                bot.delete_message(message.chat.id, message_id=message.message_id)
            except:
                pass
        bot_message = bot.send_message(chat_id=message.chat.id,
                         text=f'{text_message(5, 1)}',
                         reply_markup=markup)
        update_some_data('baskets', 'additional', bot_message.message_id, message.chat.id)


# слушаем адрес
def order_registration_4(message, bot):
    update_user_stage('entering_address', message.chat.id)
    try:
        bot.delete_message(message.chat.id, get_some_data('baskets', 'additional', message.chat.id))
    except:
        pass
    address = get_user_address(message.chat.id)
    if address is None:
        bot_message = bot.send_message(chat_id=message.chat.id,
                         disable_web_page_preview=False,
                         text=text_message(5, 2),
                         # reply_markup=inline_keyboards.remember_address_keyboard(),
                         parse_mode='html')
        update_some_data('baskets', 'additional', bot_message.message_id, message.chat.id)

    else:
        bot_message = bot.send_message(chat_id=message.chat.id,
                         disable_web_page_preview=False,
                         text=inline_keyboards.address_keyboard(message)[1],
                         reply_markup=inline_keyboards.address_keyboard(message)[0],
                         parse_mode='html')
        update_some_data('baskets', 'additional', bot_message.message_id, message.chat.id)

