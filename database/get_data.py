from contextlib import closing

import psycopg2

from config import config


def work_table(text):
    with closing(psycopg2.connect(dbname=config.name_DB,
                                  user=config.user_DB,
                                  password=config.password_DB,
                                  host=config.host_DB)) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(text)
            answer = cursor.fetchall()
            return answer


# STAGE пользователя
def get_user_stage(user_id):
    answer = work_table(f'''select stage from users where user_id = {user_id}''')
    try:
        format_answer = answer[0][0]
        return format_answer
    except:
        return None


# Список всех админов
def get_id_admins():
    answer = work_table(f'''select user_id from admin_tab''')
    format_answer = [list_id[0] for list_id in answer]
    return format_answer


# уровень админа
def get_admin_level(user_id):
    answer = work_table(f'''select level from admin_tab where user_id = {user_id}''')
    format_answer = answer[0][0]
    return format_answer


# проверяем не пустая ли корзина
def get_basket(user_id):
    answer = work_table(f'''select basket from users where user_id = {user_id}''')
    result = answer[0][0]
    if result is None or result == 'None':
        return 'None'
    else:
        return result


# Забираем колличество товаров в корзине
def get_items_basket(user_id):
    answer = work_table(f'''select basket from baskets where user_id = {user_id} and order_time IS NULL''')
    try:
        result = answer[0][0]
        return result
    except:
        return []


# Забираем сумму заказа из таблицы
def get_basket_total_price(column, user_id):
    answer = work_table(f'''select {column} from baskets where user_id = {user_id} and order_time is null''')
    result = answer[0][0]
    return result


# проверяем есть ли телефон в базе данных
def get_telephone_number(user_id):
    answer = work_table(f'''select telephone from users where user_id = {user_id}''')
    result = answer[0][0]
    return result


# собираем адреса пользователя
def get_user_address(user_id):
    answer = work_table(f'''select address.address from address where user_id = {user_id}''')
    result = answer[0][0]
    return result


def get_some_data(tab_name, selecting_item, user_id):
    answer = work_table(f'''select {selecting_item} from {tab_name} where user_id = {user_id}''')
    try:
        return answer[0][0]
    except:
        return None


# достаем старые заказы
def get_past_orders(user_id):
    answer = work_table(f'''select numb, order_time, order_text, total_price, order_payment from orders_done where user_id = {user_id}''')
    try:
        return answer
    except:
        return None

# для работы с администраторами
def get_all_data(tab_name, selecting_item):
    answer = work_table(f'''select {selecting_item} from {tab_name}''')
    try:
        return answer
    except:
        return None


# все данные по id
def get_all_data_by_identifier(tab_name, selecting_item, user_id):
    answer = work_table(f'''select {selecting_item} from {tab_name} where user_id = {user_id}''')
    try:
        return answer
    except:
        return None




# достаем старый один заказы
def get_past_order(number, user_id):
    answer = work_table(f'''select numb, order_time, order_text, total_price, order_payment, address from orders_done 
                            where user_id = {user_id} and numb = {number}''')
    try:
        return answer[0]
    except:
        return None


# достаем старый один заказы
def get_user_inf(user_id):
    answer = work_table(f'''select * from users where user_id = {user_id}''')
    try:
        return answer[0]
    except:
        return None


# для работы с администраторами
def get_all_users():
    answer = work_table(f'''select user_id from users order by numb''')
    try:
        return answer
    except:
        return None
