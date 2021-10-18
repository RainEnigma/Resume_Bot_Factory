from contextlib import closing

import psycopg2

from config import config


def tables_exists(list_tab_names):
    with closing(psycopg2.connect(dbname=config.name_DB,
                                  user=config.user_DB,
                                  password=config.password_DB,
                                  host=config.host_DB)) as conn:
        conn.autocommit = True
        with conn.cursor() as cursor:
            list_answer = []
            for tab in list_tab_names:
                cursor.execute(f"select * from information_schema.tables where table_name='{tab}'")
                if bool(cursor.rowcount):
                    pass
                else:
                    list_answer.append(tab)
        return list_answer
