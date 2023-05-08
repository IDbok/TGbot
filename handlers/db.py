# Импортируем библиотеку, соответствующую типу нашей базы данных
import sqlite3


def db_function(message_info, list_to_db):

    user_id = message_info[0]
    username = message_info[1]
    first_name = message_info[2]
    text_message = message_info[3]
    date_message = message_info[4]

    ex_amount = list_to_db[0]
    ex_currency = list_to_db[1]
    ex_category = list_to_db[2]
    ex_note = list_to_db[3]

    sql_statement_table_exists = f"SELECT EXISTS (SELECT * FROM Expenses_{user_id});"
    sql_statement_user_exists = f"SELECT EXISTS(SELECT id FROM Users WHERE id = {user_id})"  # Проверка на наличие пользователя в БД (bool)
    sql_statement_insert_operation = f"insert into Expenses_{user_id} values (\
        NULL, '{date_message}', {ex_amount}, '{ex_currency}', '{ex_category}', '{ex_note}'\
        );"

    sql_statement_create_table = f"CREATE TABLE Expenses_{user_id} (\
        id       INTEGER PRIMARY KEY\
                         UNIQUE\
                         NOT NULL,\
        date     TEXT    NOT NULL,\
        amount   NUMERIC NOT NULL,\
        currency TEXT    DEFAULT лар\
                         NOT NULL,\
        category TEXT    NOT NULL,\
        note     TEXT\
        );"

    send_message = ['','']
    error_message = ''

    try:
        # print('Подключение к БД')
        conn = sqlite3.connect("venv/test.db")
        cursor = conn.cursor()
        # print("Проверка допуска (наличие в таблицы users)")
        # Проверка допуска (наличие в таблицы users)
        if cursor.execute(sql_statement_user_exists).fetchall()[0] == (1,):
            # print("Проверка доступа пройдена")
            # print("Проверка наличия таблицы в базе")
            # Проверка наличия таблицы в базе
            try:
                cursor.execute(sql_statement_table_exists)
                # print("Таблица есть, можно добавлять операцию")
            except sqlite3.Error as error:
                if str(error) == f"no such table: Expenses_{user_id}":
                    # print("Таблицы нет, надо создать")
                    cursor.execute(sql_statement_create_table)
                    send_message[0] = 'Была созданна новая таблица'
                    # print("Была созданна новая таблица")

            # Вставляем данные в таблицу расходов
            # print("Вставляем данные в таблицу расходов")
            cursor.execute(sql_statement_insert_operation)
            # print(f'Запрос к БД:\n{sql_statement_insert_operation}')
            if ex_note !='':
                send_message[1] = f'Новая запись была добавленна:' \
                                 f'\n{ex_category}: {ex_amount} {ex_currency}' \
                                 f'\nПримечание: {ex_note}'
            else:
                send_message[1] = f'Новая запись была добавленна:' \
                                  f'\n{ex_category}: {ex_amount} {ex_currency}'

            # Подтверждение изменений
            # print("Подтверждение изменений")
            conn.commit()

        else:
            error_message = 'Для Вас нет разрешение на использование бота. Сорри'
            # print(error_message)

        if error_message != '':
            send_message[1] = error_message

        # print(send_message[0])
        # print(send_message[1])



    except sqlite3.Error as error:
        print("Error", error)

    finally:
        conn.close()

    return send_message
