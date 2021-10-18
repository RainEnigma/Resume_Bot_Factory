
# Получаем данные о ID клиента
from database.get_data import get_user_inf, get_some_data
from database.update_data import update_user_stage, update_some_data
from keyboards.inline_keyboards import get_user_id_keyboard


def get_user_info(call, bot):
    update_user_stage('get_user_info', call.message.chat.id)

    text = 'Введите телеграм-ID человека для получения информации по нему:'

    message_id = bot.edit_message_text(chat_id=call.message.chat.id,
                                       message_id=call.message.message_id,
                                       text=text,
                                       reply_markup=get_user_id_keyboard())
    update_some_data('admins', 'additional', message_id.message_id, call.message.chat.id)


def show_user_data(message, bot):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        pass

    if message.text.isdigit():
        try:
            answer = get_user_inf(message.text)
            if answer is None:
                text = 'Пользователя с таким ID нет в базе данных.'

            else:


                text = f'ID - {answer[1]}\n\n' \
                       f'Имя:\n' \
                       f'{answer[2]}, @{answer[3]}, {answer[4]}\n\n' \
                       f'дата добавления:\n' \
                       f'{answer[6]}\n\n' \
                       f'Телефон - {answer[5]} грн.\n' \
                       f'Скидка клиента - {(answer[10]-1)*100}% грн.\n' \
                       f'Общая сумма заказов ' \
                       f'{answer[11]} грн.\n\n' \
                       f'Адреса клиента:\n'
                address = get_some_data('address', 'address.address', int(message.text))
                if address is not None:
                    for addr in address:
                        text += f'- {addr}\n'
        except:
            text = 'Извините, произошел технический сбой. Данные о нем уже переданы для рассмотрения.'
        try:
            bot.edit_message_text(chat_id=message.chat.id,
                                  message_id=get_some_data('admins', 'additional', message.chat.id),
                                  text=text)

        except:
            pass

    else:
        text = 'Вы ввели неверный номер ID телеграм, попробуйте снова:'
    try:
        bot.edit_message_text(chat_id=message.chat.id,
                              message_id=get_some_data('admins', 'additional', message.chat.id),
                              text=text,
                              reply_markup=get_user_id_keyboard(),
                              parse_mode='html')
    except:
        pass