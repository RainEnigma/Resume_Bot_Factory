from config.from_exel_file import text_message
from database.get_data import get_some_data, get_all_data, get_all_data_by_identifier
from database.insert_data_to_tables import insert_order_to_orders_done
from database.update_data import update_some_data, update_final_data, delete_data


def finish_funk(call, bot):
    address = get_some_data('address', 'address.address', call.message.chat.id)
    address_numb = int(call.data.split('_')[1])
    update_final_data(address[address_numb], call.message.chat.id)
    # Отправка сообщения администраторам
    admins = get_all_data('admins', 'user_id')
    order_data = get_all_data_by_identifier('baskets', '*', call.message.chat.id)[0]
    person_data = get_all_data_by_identifier('users', '*', call.message.chat.id)[0]

    text_order = f'Заказ № {order_data[0]} ... status - "open"\n\n' \
                 f'🕔 {"{:%H:%M}".format(order_data[3])} 🗓 {"{:%d.%m.%Y}".format(order_data[3])}\n' \
                 f'👤 - {person_data[2]}, {person_data[3]}, {person_data[4]}\n' \
                 f'☎ - {person_data[5]}\n' \
                 f'DISCOUNT - {round((person_data[10]-1)*100)}%\n' \
                 f'🏡 - {order_data[6]}\n' \
                 f'💵 - {order_data[5]} ({order_data[4]}грн.)\n\n' \
                 f'----ДАННЫЕ ЗАКАЗА----' \
                 f'{order_data[8].replace("<b>Ваш заказ</b>","").lstrip("/n/n")}'

    for admin in admins:
        try:
            bot.send_message(admin[0], text_order, parse_mode='html')
        except:
            pass

    insert_order_to_orders_done(call.message.chat.id)
    update_some_data('orders_done', 'order_status', 'open', call.message.chat.id)

    delete_data(call.message.chat.id)
    update_some_data('users', 'basket', None, call.message.chat.id)




    from main import start
    start(call.message, text_message(7, 1))