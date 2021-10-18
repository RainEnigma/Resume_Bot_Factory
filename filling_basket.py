from database import get_data
from database import insert_data_to_tables
from database.get_data import get_user_stage
from database.update_data import update_basket_stage, adding_into_basket
from menu.menu import big_cifr_func


def basket_work(call, bot):
    stage = get_user_stage(call.message.chat.id)
    basket_data = get_data.get_basket(call.message.chat.id)
    if basket_data == 'None' or basket_data is None:  # Если корзина пуста
        insert_data_to_tables.insert_user_to_baskets(call.message.chat.id, stage)
        update_basket_stage('started', call.message.chat.id)
    else:  # Если корзина не пуста
        adding_into_basket(stage, call.message.chat.id)
    big_cifr_func(call, bot, 'upgrade_buttons')
