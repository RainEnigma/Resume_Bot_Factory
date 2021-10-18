from database import get_data
from database.delete_data import delete_admin
from database.get_data import get_all_data, get_some_data, get_all_users
from database.insert_data_to_tables import insert_new_admin
from database.update_data import update_user_stage, update_some_data
from get_user_info import get_user_info
from keyboards import inline_keyboards
from keyboards.inline_keyboards import admin_manage_keyboard, new_admin_level


def admin_work(call, bot):
    if call.data.split('_')[1] == '🕹Админ-менеджер':
        admin_manager(call, bot)

    elif call.data.split('_')[1] == 'ℹКлиент-инфо':
        get_user_info(call, bot)

    elif call.data.split('_')[1] == '👤Все клиенты':
        status = get_data.get_some_data('admins', 'level', call.message.chat.id)
        text = 'Пользователи бота:\n\n'
        users = get_all_users()
        for num, user in enumerate(users):
            text += f'{num+1} - {user[0]}\n'
        try:
            bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=text,
                              reply_markup=inline_keyboards.admin_pan_1_keyboard(status),
                              parse_mode='html')
        except:
            pass

# обработка кнопки '🕹Админ-менеджер'
def admin_manager(call, bot):
    update_user_stage('admin_manager', call.message.chat.id)

    all_admins = get_all_data('admins', '*')
    text = 'Нажмите на кнопку для удаления адиминистратора:\n\n'
    buttons = []
    for admin in all_admins:
        text += f'{admin[0]} - {admin[4]}, {admin[3]} ({admin[1]})\nуровень - {admin[2]}\n\n'
        buttons.append(f'❌{admin[0]}')

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=text,
                          reply_markup=admin_manage_keyboard(buttons),
                          parse_mode='html')


# Обработка кнопки '➕Добавить нового админа'
def admin_manage(call, bot):
    if call.data.split('_')[1] == '➕Добавить нового админа':
        update_user_stage('adding_new_admin', call.message.chat.id)
        text = 'Введите ID нового администратора и его имя через запятую:\n\nНапример:1234567823,Андрей Иванов'
        try:
            message_id = bot.edit_message_text(chat_id=call.message.chat.id,
                                               message_id=call.message.message_id,
                                               text=text,
                                               reply_markup=admin_manage_keyboard(argum='no_button_add_admin'))
            update_some_data('admins', 'additional', message_id.message_id, call.message.chat.id)
        except:
            pass
    elif call.data.split('_')[1][0] == '❌':
        delete_admin('numb', call.data.split('_')[1][1:])
        admin_manager(call, bot)



def adding_new_admin(message, bot):
    new_admin = message.text.split(',')
    bot.delete_message(message.chat.id, message.message_id)

    try:
        user_id = new_admin[0]
        user_given_name = new_admin[1]
        bot.get_user_profile_photos(user_id)
        insert_new_admin(user_id, user_given_name)
        update_user_stage('adding_role_new_admin', message.chat.id)
        bot.edit_message_text(chat_id=message.chat.id,
                              message_id=get_some_data('admins', 'additional', message.chat.id),
                              text='Укажите уровень нового администратора:',
                              reply_markup=new_admin_level(user_id))


    except:
        text = 'Вы ввели некоректный ID пользователя или пользователь еще не подключен к боту, повторите попытку:\n\n' \
               'Например:1234567823,Андрей Иванов'
        try:
            bot.edit_message_text(chat_id=message.chat.id,
                                  message_id=get_some_data('admins', 'additional', message.chat.id),
                                  text=text,
                                  reply_markup=admin_manage_keyboard(argum='no_button_add_admin'))
        except:
            pass