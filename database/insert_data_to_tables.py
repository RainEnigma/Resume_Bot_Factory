from contextlib import closing
from datetime import datetime

import psycopg2

from config import config
from database import get_data


def insert_into_tables(text):
    with closing(psycopg2.connect(dbname=config.name_DB,
                                  user=config.user_DB,
                                  password=config.password_DB,
                                  host=config.host_DB)) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(text)


def insert_user_to_table(message):
    # Проверяем существует ли пользователь в таблице пользователей, если нет - добавляем
    if get_data.get_user_stage(message.chat.id) is None:
        text = f'''insert into users (user_id, name, user_name, last_name, date_add, stage, discount, user_totally_buy)  
               values ({message.from_user.id},
                      '{message.from_user.first_name}',
                      '{message.from_user.username}',
                      '{message.from_user.last_name}',
                      '{datetime.now().date()}',
                      'main_menu',
                       1,
                       0);'''
        insert_user_to_address(message)
        insert_into_tables(text)


# добавляем пользоваеля в таблицу адресов
def insert_user_to_address(message):
    if get_data.get_user_stage(message.chat.id) is None:
        text = f'''insert into address (user_id) values ({message.from_user.id});'''
        insert_into_tables(text)


def insert_levels_users():
    list_levels = ['super_admin', 'admin', 'moderator']
    for level in list_levels:
        text = f'''insert into admin_levels (level) values ('{level}');'''
        insert_into_tables(text)


def insert_start_admins():
    text = f'''insert into admins (user_id, level) values (238008205, '🦸‍♂Супер-Админ');'''
    insert_into_tables(text)


# добавить в таблицу корзины id_пользователя
def insert_user_to_baskets(user_id, basket_data):
    text = f'''insert into baskets (user_id, basket) values ({user_id}, '{{{basket_data}}}');'''
    insert_into_tables(text)


# Перенести данные о готовом заказе в таблицу готовых заказов
def insert_order_to_orders_done(user_id):
    text = f'''INSERT INTO orders_done(numb, user_id, basket, order_time, total_price, order_payment, address, order_done, order_text, additional)  SELECT numb, user_id, basket, order_time, total_price, order_payment, address, order_done, order_text, additional FROM baskets where user_id = {user_id};'''
    insert_into_tables(text)


def insert_new_admin(user_id, given_name):
    text = f'''insert into admins (user_id, given_name) values ({user_id}, '{given_name}');'''
    insert_into_tables(text)