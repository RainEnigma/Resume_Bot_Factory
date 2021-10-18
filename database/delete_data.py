from contextlib import closing

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


# Удаление не о конца созданного пользователя
def delete_admin(column, data_column):
    text = f'''DELETE FROM admins where {column} = {data_column};'''
    update_data_in_tables(text)
