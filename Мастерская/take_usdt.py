import sqlite3
import time


def take_usdt():
    # Подключение к базам данных
    conn_source = sqlite3.connect('pair_base_2.db')
    conn_target = sqlite3.connect('take_usdt.db')

    cursor_source = conn_source.cursor()
    cursor_target = conn_target.cursor()

    # Создание целевой таблицы, если её не существует
    cursor_target.execute('''
        CREATE TABLE IF NOT EXISTS all_nametables (
            nametable TEXT UNIQUE,
            pair1 TEXT, 
            pair2 TEXT              
        )
    ''')

    # Получение списка таблиц в исходной базе данных
    cursor_source.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor_source.fetchall()

    # Проход по каждой таблице
    for table in tables:
        table_name = table[0]
        try: 
            cursor_source.execute(f"SELECT nametable, name_pair1, name_pair2  FROM {table_name} WHERE name_pair1='USDT' OR name_pair2='USDT'")
            rows = cursor_source.fetchall()

            # Запись в целевую таблицу
            for row in rows:
                print(row)
                nametable = row[0].replace('_', '') 
                try:
                    if "2" not in nametable:
                        if "3" not in nametable:
                            cursor_target.execute("INSERT INTO all_nametables (nametable,pair1,pair2) VALUES (?,?,?)", (nametable,row[1],row[2]))
                except sqlite3.IntegrityError:
                    # Игнорируем ошибку, если запись уже существует (UNIQUE constraint)
                    pass 
        except sqlite3.IntegrityError:
                    # Игнорируем ошибку, если запись уже существует (UNIQUE constraint)
                    pass 
        
    # Сохранение изменений и закрытие соединений
    conn_target.commit()
    conn_source.close()
    conn_target.close()

    print("Данные успешно скопированы!")



while True:
    try:
        take_usdt()
        time.sleep(43200)
    except Exception as e:
        time.sleep(30)