from config.from_exel_file import text_message
from database.get_data import get_items_basket
from database.update_data import update_user_stage, update_some_data
from func_return_column_dishes import column_dishes
from keyboards import inline_keyboards


def in_basket(call, bot):
    update_user_stage('in_basket', call.message.chat.id)

    basket_items = get_items_basket(call.message.chat.id)
    list_normal_names = []
    list_costs = []
    for item in basket_items:
        item_category = item.split('_')[0]
        item_num = item.split('_')[1]

        list_columns = column_dishes(item_category)  # получаем колонки блюд

        normal_name = text_message(int(item_num), list_columns[0]).split('\n')[0]
        list_normal_names.append(f"{normal_name}_{text_message(int(item_num), list_columns[1])}")
        list_costs.append(text_message(int(item_num), list_columns[1]).split('\n')[0])

    dict_answer = {}
    analysis(list_normal_names, dict_answer)
    text = text_generator(dict_answer,call)
    update_some_data('baskets', 'order_text', text, call.message.chat.id)
    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=text,
                          reply_markup=inline_keyboards.basket_keyboard(),
                          parse_mode='html')


# Заполняем словарь dict_answer
def analysis(your_list, your_dict):
    for item in your_list:
        if item in your_dict:
            your_dict[item] += 1
        else:
            your_dict[item] = 1


# формируем текст корзины
def text_generator(input_dict, call):
    text = '<b>Ваш заказ</b>'
    total_price = 0
    for key, value in input_dict.items():
        text = f'{text}\n\n{key.split("_")[0]}\n{value} шт., {key.split("_")[1]} грн.'
        total_price += int(value) * int(key.split("_")[1])

    text = f'{text}\n\n<b>Итого: {total_price} грн.</b>'
    update_some_data('baskets', 'total_price', total_price, call.message.chat.id)
    return text
