from contextlib import closing
import psycopg2
from config import config


def add_user_to_table_HM(tab_name, **kwargs):
    forming_string = ''
    for item in kwargs.items():
        forming_string += f'{item[0]}={item[1]},'
        break
    forming_string = forming_string.rstrip(',')

    with closing(psycopg2.connect(dbname=config.name_DB,
                                  user=config.user_DB,
                                  password=config.password_DB,
                                  host=config.host_DB)) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(f"""select user_id from {tab_name} where ({forming_string})""")
            is_user_in_table = cursor.fetchone()

    if is_user_in_table is None:

        forming_keys = ''
        forming_values = []
        for item in kwargs.items():
            forming_keys += f'{item[0]}, '
            forming_values.append(item[1])
        forming_keys = forming_keys.rstrip(', ')
        forming_values = tuple(forming_values)
        with closing(psycopg2.connect(dbname=config.name_DB,
                                      user=config.user_DB,
                                      password=config.password_DB,
                                      host=config.host_DB)) as conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute(f"""insert into {tab_name} ({forming_keys}) values {forming_values} """)
