from contextlib import closing

import psycopg2

from config import config


def create_tables(text, text_2=None):
    with closing(psycopg2.connect(dbname=config.name_DB,
                                  user=config.user_DB,
                                  password=config.password_DB,
                                  host=config.host_DB)) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(text)
            if text_2 is not None:
                cursor.execute(text_2)


# Создание таблицы пользователей
def create_table_users(table_name):
    text = f"""create table if not exists {table_name} (numb SERIAL PRIMARY KEY,
                                                        user_id bigint,
                                                        name varchar, 
                                                        user_name varchar,
                                                        last_name varchar,
                                                        telephone varchar,
                                                        date_add varchar,
                                                        language varchar, 
                                                        stage varchar, 
                                                        basket varchar, 
                                                        discount float,
                                                        user_totally_buy float,
                                                        additional varchar)"""
    create_tables(text)


# Создание таблицы меню
def create_table_menu(table_name):
    text = f"""create table if not exists {table_name} (numb SERIAL PRIMARY KEY,
                                                        dish_id varchar,
                                                        dish_name varchar, 
                                                        dish_category varchar,
                                                        dish_cost real,
                                                        additional varchar)"""
    create_tables(text)


# Создание таблицы администраторов
def create_table_admins(table_name):
    text = f"""create table if not exists {table_name} (numb SERIAL PRIMARY KEY,
                                                        user_id bigint,
                                                        level varchar,
                                                        name varchar,
                                                        given_name varchar,
                                                        date_add varchar, 
                                                        language varchar, 
                                                        additional varchar)"""
    create_tables(text)


# Таблица корзин
def create_table_baskets(table_name):
    text = f"""create table if not exists {table_name} (numb SERIAL PRIMARY KEY,
                                                        user_id bigint,
                                                        basket varchar [],
                                                        order_time timestamp,
                                                        total_price varchar,
                                                        order_payment varchar,
                                                        address varchar,
                                                        order_done varchar,
                                                        order_text varchar,
                                                        temp_address varchar,
                                                        additional varchar)"""
    create_tables(text)


# Таблица адресов клиентов
def create_table_address(table_name):
    text = f"""create table if not exists {table_name} (numb SERIAL PRIMARY KEY,
                                                        user_id bigint,
                                                        address varchar [],
                                                        additional varchar)"""
    create_tables(text)


# Таблица готовых заказов
def create_table_orders_done(table_name):
    text = f"""create table if not exists {table_name} (numb integer,
                                                        user_id bigint,
                                                        basket varchar [],
                                                        order_time timestamp,
                                                        total_price varchar,
                                                        order_payment varchar,
                                                        address varchar,
                                                        order_done varchar,
                                                        order_text varchar,
                                                        order_status varchar,
                                                        additional varchar)"""
    create_tables(text)
