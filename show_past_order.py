import string
from database.get_data import get_past_order
from keyboards.inline_keyboards import past_orders_button


def show_past_order(call, bot):
    order_data = get_past_order(call.data.split('_')[1], call.message.chat.id)

    if order_data[4] == 'cash':
        payment = 'Наличными курьеру'
    elif order_data[4] == 'card':
        payment = 'Картой курьеру'
    else:
        payment = 'Оплата через интернет'


    text = f'<b>Заказ №{order_data[0]} ({"{:%d.%m.%Y %H:%M}".format(order_data[1])})</b>\n' \
           f'Оплата: {payment}\n' \
           f'Адрес: {order_data[5]}' \
           f'{order_data[2].replace("<b>Ваш заказ</b>","")}'

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=text,
                          reply_markup=past_orders_button(),
                          parse_mode='html')
