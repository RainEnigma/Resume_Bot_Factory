from config.from_exel_file import text_message
from database.get_data import get_items_basket
from database.update_data import update_user_stage, delete_item_in_basket, update_some_data
from func_return_column_dishes import column_dishes
from keyboards.inline_keyboards import basket_redact_keyboard


def basket_redact(call, bot):
    update_user_stage('redact_basket', call.message.chat.id)

    basket_items = get_items_basket(call.message.chat.id)
    list_normal_names = []
    list_costs = []
    for item in basket_items:
        item_category = item.split('_')[0]
        item_num = item.split('_')[1]

        list_columns = column_dishes(item_category)  # получаем колонки блюд

        normal_name = text_message(int(item_num), list_columns[0]).split('\n')[0]
        normal_name = f"❌{normal_name.strip('</b>')}"
        list_normal_names.append(f"{normal_name} {text_message(int(item_num), list_columns[1])}_{item}")
        list_costs.append(text_message(int(item_num), list_columns[1]).split('\n')[0])
    total_price = 0
    for cost in list_costs:
        total_price += int(cost)

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=call.message.message_id,
                          text=f'{text_message(2, 2)}\n\n<b>Итого:</b> {total_price}грн.',
                          reply_markup=basket_redact_keyboard(list_normal_names, call),
                          parse_mode='html')
    update_some_data('baskets', 'total_price', total_price, call.message.chat.id)


# Удаление из корзины + обновление экрана
def deleting_from_basket(item_name, call, bot):
    # удаляем значение из таблицы
    delete_item_in_basket(item_name, call.message.chat.id)
    basket_redact(call, bot)

