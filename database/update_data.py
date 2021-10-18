from contextlib import closing
from datetime import datetime

import psycopg2

from config import config


def update_data_in_tables(text):
    with closing(psycopg2.connect(dbname=config.name_DB,
                                  user=config.user_DB,
                                  password=config.password_DB,
                                  host=config.host_DB)) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(text)


def update_user_stage(stage, user_id):
    text = f'''update users set stage = '{stage}' where user_id = {user_id};'''
    update_data_in_tables(text)


# добавить в таблицу статус корзины
def update_basket_stage(stage, user_id):
    text = f'''update users set basket = '{stage}' where user_id = {user_id};'''
    update_data_in_tables(text)


def adding_into_basket(value, user_id):
    text = f'''UPDATE baskets SET basket = basket || '{{{value}}}' where user_id = {user_id} and order_time IS NULL;'''
    update_data_in_tables(text)


def delete_item_in_basket(item, user_id):
    text = f'''UPDATE baskets set basket = array_remove(basket,'{item}')where user_id = {user_id} and order_time is null;'''
    update_data_in_tables(text)


# Обновить любые данные в любой таблице
def update_some_data(table_name, column, inserting_data, user_id):
    text = f'''update {table_name} set {column} = '{inserting_data}' where user_id = {user_id};'''
    update_data_in_tables(text)


# добавить сумму всех заказов
def update_user_totally_buy(inserting_data, user_id):
    text = f'''update users set user_totally_buy = user_totally_buy+{inserting_data} where user_id = {user_id};'''
    update_data_in_tables(text)


# Обновить любые данные в любой таблице
def update_final_data(address, user_id):
    time_now = datetime.now()
    text = f'''update baskets set order_time='{time_now}', order_done='done!', address='{address}' where user_id={user_id};'''
    update_data_in_tables(text)


# очистка заказа в корзине
def delete_data(user_id):
    text = f'''delete from baskets where user_id={user_id};'''
    update_data_in_tables(text)


# Добавить в таблицу адрес
def adding_address(value, user_id):
    text = f'''UPDATE address SET address = address.address || '{{{value}}}' where user_id = {user_id};'''
    update_data_in_tables(text)