import pandas as pd
from pandas import DataFrame
from pybit.unified_trading import HTTP
import pandas_ta as pta
import matplotlib.pyplot as plt

import sqlite3


def take_rsi(symbol,interval):

    cl = HTTP(recv_window=60000,)
    r = cl.get_kline(category="spot", symbol=symbol, interval=interval)


    data = r.get('result', {}).get('list', [])
    df = pd.DataFrame(data).iloc[::-1].reset_index(drop=True)
    df.columns = list('tohlcvt')

    for col in df.columns:
        if col != 't':
            if df[col].dtype == 'object':
                try:
                    df[col] = df[col].astype(float) 
                except ValueError:
                    print(f'Не удается преобразовать столбец {col} в целочисленный тип.')



    df['rsi']  = pta.rsi(df['c'], length = 14)

    rsi_array = df['rsi'].dropna().values

    rsi_objects = [(index, round(value, 2)) for index, value in enumerate(rsi_array)]
    return rsi_objects
    


def take_trade_pair_for_rsi():

    conn = sqlite3.connect('price_pair_trade.db')
    cursor = conn.cursor()

    cursor.execute('SELECT pair_step_1, pair_step_2, pair_step_3 FROM Trade_pair')

    # Получаем результат запроса
    rows = cursor.fetchall()

    # Выводим значения
    unique_values_set = set()

    for row in rows:
        value1, value2, value3 = row
        unique_values_set.add(value1)
        unique_values_set.add(value2)
        unique_values_set.add(value3)

    unique_values = list(unique_values_set)
    conn.close()
    return unique_values

    # Закрываем соединение
    

# print(take_rsi('BTCUSDT',5))

def add_base_rsi(table, rsi_objects):
    conn = sqlite3.connect('base_rsi.db')
    cursor = conn.cursor()

    cursor.execute('DROP TABLE IF EXISTS {}'.format(table))

    cursor.execute('''CREATE TABLE IF NOT EXISTS {} (index_value INTEGER, rounded_value REAL)'''.format(table))

    # Добавление данных из массива rsi_objects в базу данных
    for obj in rsi_objects[-10:]:
        cursor.execute('INSERT INTO {} (index_value, rounded_value) VALUES (?, ?)'.format(table), (obj[0], obj[1]))

    # Сохранение изменений и закрытие соединения
    conn.commit()
    conn.close()


# for i in take_trade_pair_for_rsi():
#     add_base_rsi(i ,take_rsi(i ,5))


print(take_rsi('BTCUSDT' ,5)[-1:][0][1])


