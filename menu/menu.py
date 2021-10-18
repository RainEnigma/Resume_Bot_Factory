from config.from_exel_file import text_message
from database import update_data, get_data
from database.get_data import get_past_orders
from func_return_column_dishes import column_dishes
from get_user_info import get_user_info
from keyboards import inline_keyboards
from keyboards.inline_keyboards import buttons_past_order


def menu(call, bot):
    if call.data.split('_')[1] == '✅Вып. заказы':
        update_data.update_user_stage('past_orders', call.message.chat.id)
        past_orders = get_past_orders(call.message.chat.id)
        generated_data = buttons_past_order(past_orders)
        text = generated_data[0]
        markup = generated_data[1]
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=text,
                              reply_markup=markup,
                              parse_mode='html')

    elif call.data.split('_')[1] == '🥗Салаты':
        update_data.update_user_stage('salads_1', call.message.chat.id)
        # bot.edit_message_reply_markup(chat_id=call.message.chat.id,
        #                               message_id=call.message.message_id,
        #                               reply_markup=inline_keyboards.salads())

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=f'<a href = "{text_message(17, 3)}" class = "ssilka" >   </a>\n {text_message(1, 3)}',
                              reply_markup=inline_keyboards.buttons_generator(
                                  get_data.get_user_stage(call.message.chat.id).split('_')[1], 'salads', call),
                              parse_mode='html')

    elif call.data.split('_')[1] == '🍜Супы':
        update_data.update_user_stage('sup_1', call.message.chat.id)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=f'<a href = "{text_message(17, 5)}" class = "ssilka" >   </a>\n {text_message(1, 5)}',
                              reply_markup=inline_keyboards.buttons_generator(get_data.get_user_stage(call.message.chat.id).split('_')[1], 'sup', call),
                              parse_mode='html')

    elif call.data.split('_')[1] == '🥡Лапша':
        update_data.update_user_stage('noodles_1', call.message.chat.id)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=f'<a href = "{text_message(17, 7)}" class = "ssilka" >   </a>\n {text_message(1, 7)}',
                              reply_markup=inline_keyboards.buttons_generator(get_data.get_user_stage(call.message.chat.id).split('_')[1], 'noodles', call),
                              parse_mode='html')

    elif call.data.split('_')[1] == '🍟Гарниры':
        update_data.update_user_stage('garnish_1', call.message.chat.id)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=f'<a href = "{text_message(17, 9)}" class = "ssilka" >   </a>\n {text_message(1, 9)}',
                              reply_markup=inline_keyboards.buttons_generator(
                                  get_data.get_user_stage(call.message.chat.id).split('_')[1], 'garnish', call),
                              parse_mode='html')

    elif call.data.split('_')[1] == '🍔Бургеры':
        update_data.update_user_stage('burger_1', call.message.chat.id)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=f'<a href = "{text_message(17, 11)}" class = "ssilka" >   </a>\n {text_message(1, 11)}',
                              reply_markup=inline_keyboards.buttons_generator(
                                  get_data.get_user_stage(call.message.chat.id).split('_')[1], 'burger', call),
                              parse_mode='html')

    elif call.data.split('_')[1] == '🍩Сладости':
        update_data.update_user_stage('sweets_1', call.message.chat.id)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=f'<a href = "{text_message(17, 13)}" class = "ssilka" >   </a>\n {text_message(1, 13)}',
                              reply_markup=inline_keyboards.buttons_generator(
                                  get_data.get_user_stage(call.message.chat.id).split('_')[1], 'sweets', call),
                              parse_mode='html')

    elif call.data.split('_')[1] == '🛠Админпанель':
        admin_pan(call, bot)


def big_cifr_func(call, bot, activator=None):
    if activator is None:
        update_data.update_user_stage(call.data, call.message.chat.id)

    dish_category = get_data.get_user_stage(call.message.chat.id).split('_')[0]
    dish_numb = get_data.get_user_stage(call.message.chat.id).split('_')[1]

    list_columns = column_dishes(dish_category)

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=f'<a href = "{text_message(int(dish_numb)+16, list_columns[0])}" class = "ssilka" >   </a>\n {text_message(int(dish_numb), list_columns[0])}',

                          reply_markup=inline_keyboards.buttons_generator(dish_numb, dish_category, call),
                          parse_mode='html')

def admin_pan(call, bot):
    update_data.update_user_stage('admin_panel', call.message.chat.id)

    status = get_data.get_some_data('admins', 'level', call.message.chat.id)
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=f'{text_message(6, 2)}{status}',
                          reply_markup=inline_keyboards.admin_pan_1_keyboard(status),
                          parse_mode='html')