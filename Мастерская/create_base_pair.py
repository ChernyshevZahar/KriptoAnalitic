from pybit.unified_trading import HTTP
import sqlite3
import time
import datetime

def take_base():
    cl = HTTP(recv_window=60000,)
    r = cl.get_tickers(category="spot")
    return r.get('result', {}).get('list', [])

def update_symbol_data(db_path, data):
    """
    Обновляет данные по каждому символу в базе данных, 
    сохраняя последние 2000 записей.

    Args:
        db_path: Путь к базе данных SQLite.
        data: Массив объектов с полями 'symbol' и 'lastPrice'.
    """

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for item in data:
        try: 
            symbol = item['symbol']
            last_price = item['lastPrice']
            timestamp = datetime.datetime.now()

            # Создание таблицы, если она не существует
            cursor.execute(f'''
                CREATE TABLE IF NOT EXISTS {symbol} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    last_price REAL,
                    timestamp DATETIME
                )
            ''')

            # Добавление новой записи
            cursor.execute(f"INSERT INTO {symbol} (last_price, timestamp) VALUES (?, ?)", 
                        (last_price, timestamp))

            # Удаление старых записей, если их больше 2000
            cursor.execute(f"SELECT COUNT() FROM {symbol}")
            row_count = cursor.fetchone()[0]
            if row_count > 2000:
                cursor.execute(f"DELETE FROM {symbol} WHERE id IN (SELECT id FROM {symbol} ORDER BY timestamp LIMIT {row_count - 2000})")
        except Exception as e:
            pass

    conn.commit()
    conn.close()

while True:
    try:
        update_symbol_data('test_base.db',take_base())
        time.sleep(280)
    except Exception as e:
        time.sleep(10)