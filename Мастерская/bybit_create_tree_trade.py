from pybit.unified_trading import HTTP
import sqlite3
import time
import logging



test_obg = {}

balance = 10

def take_traid_pait():
    conn = sqlite3.connect('pair_base_make_traide.db')
    cursor = conn.cursor()


    cursor.execute("SELECT pair FROM pair")

    column_values = [row[0] for row in cursor.fetchall()]

    conn.close()

    return column_values


def take_pair_price_close(symbol,interval=1,limit=1):

    cl = HTTP(recv_window=60000,)
    r = cl.get_kline(category="spot", symbol=symbol, interval=interval, limit=limit)

    data = r.get('result', {}).get('list', [])

    return(data[0][3])




def price_pair_trade(list_trade):
        conn = sqlite3.connect('pair_base_2.db')
        cursor = conn.cursor()
        
        list_pair = []
        for table in list_trade:

            cursor.execute("SELECT * FROM {}".format(table))
            
            result = [[row[0],row[1],row[2].replace('_', '')] for row in cursor.fetchall()]

            
            # print(result)
            list_pair_price  = [ ]
            try:
                for pair in result:
                    if pair[1] in ['USDT','BTC','ETH']:
                        if pair[1] == "BTC":
                            obj_1 = { "pair": pair[2] ,"pair1": pair[0] ,"pair2": pair[1] , "price" : take_pair_price_close(pair[2])}
                            list_pair_price.append(obj_1)
                            obj_1 = { "pair": "BTCUSDT" ,"pair1": "BTC" ,"pair2": "USDT" , "price" : take_pair_price_close("BTCUSDT")}
                            list_pair_price.append(obj_1)
                        elif pair[1] == "ETH":
                            obj_1 = { "pair": pair[2] ,"pair1": pair[0] ,"pair2": pair[1] , "price" : take_pair_price_close(pair[2])}
                            list_pair_price.append(obj_1)
                            obj_1 = { "pair": "ETHUSDT" ,"pair1": "ETH" ,"pair2": "USDT" , "price" : take_pair_price_close("ETHUSDT")}
                            list_pair_price.append(obj_1)
                        elif pair[1] == "USDT":
                            obj_1 = { "pair": pair[2] ,"pair1": pair[0] ,"pair2": pair[1] , "price" : take_pair_price_close(pair[2])}
                            list_pair_price.insert(0,obj_1)
                        
                if len(list_pair_price)>2:
                    obj_trade_pair = {
                        "site": 'bibyt',
                        "pair_step_1": list_pair_price[0]['pair'],
                        "pair_step_1_pair1": list_pair_price[0]['pair1'],
                        "pair_step_1_pair2": list_pair_price[0]['pair2'],
                        "pair_step_1_price": list_pair_price[0]['price'],
                        
                        "pair_step_2": list_pair_price[1]['pair'],
                        "pair_step_2_pair1": list_pair_price[1]['pair1'],
                        "pair_step_2_pair2": list_pair_price[1]['pair2'],
                        "pair_step_2_price": list_pair_price[1]['price'],

                        "pair_step_3": list_pair_price[2]['pair'],
                        "pair_step_3_pair1": list_pair_price[2]['pair1'],
                        "pair_step_3_pair2": list_pair_price[2]['pair2'],
                        "pair_step_3_price": list_pair_price[2]['price'],

                        "Dohod_go": round((balance/float(list_pair_price[0]['price'])*float(list_pair_price[1]['price'])*float(list_pair_price[2]['price']))-balance,9),
                        "Dohod_back": round((balance/float(list_pair_price[2]['price'])/float(list_pair_price[1]['price'])*float(list_pair_price[0]['price']))-balance,9)

                    }
                    # print(obj_trade_pair)
                    conn2 = sqlite3.connect('price_pair_trade.db')
                    cursor2 = conn2.cursor()

                    # Создаем таблицу, если она не существует
                    cursor2.execute('''
                        CREATE TABLE IF NOT EXISTS Trade_pair (
                            site TEXT,
                            pair_step_1 TEXT,
                            pair_step_1_pair1 TEXT,
                            pair_step_1_pair2 TEXT,
                            pair_step_1_price TEXT,
                            pair_step_1_price_line_up TEXT,
                            pair_step_1_price_line_down TEXT,
                            pair_step_2 TEXT,
                            pair_step_2_pair1 TEXT,
                            pair_step_2_pair2 TEXT,
                            pair_step_2_price TEXT,
                            pair_step_2_price_line_up TEXT,
                            pair_step_2_price_line_down TEXT,
                            pair_step_3 TEXT,
                            pair_step_3_pair1 TEXT,
                            pair_step_3_pair2 TEXT,
                            pair_step_3_price TEXT,
                            pair_step_3_price_line_up TEXT,
                            pair_step_3_price_line_down TEXT,
                            Dohod_go TEXT,
                            Dohod_back TEXT
                        )
                    ''')

                    # Проверяем наличие данных по столбцу pair_step_1_pair1
                    pair_step_1_pair1 = obj_trade_pair['pair_step_1_pair1']  # Пример значения для проверки
                    cursor2.execute('SELECT * FROM Trade_pair WHERE pair_step_1_pair1 = ?', (pair_step_1_pair1,))
                    existing_data = cursor2.fetchone()

                    # Если данные уже существуют, обновляем их
                    if existing_data:
                        # Выполняем UPDATE запрос для обновления данных
                        new_pair_step_1_price = float(obj_trade_pair['pair_step_1_price'])  # Пример нового значения
                        new_pair_step_2_price = float(obj_trade_pair['pair_step_2_price'])  # Пример нового значения
                        new_pair_step_3_price = float(obj_trade_pair['pair_step_3_price'])  # Пример нового значения
                        new_dohod_go = obj_trade_pair['Dohod_go']  # Пример нового значения
                        new_dohod_back = obj_trade_pair['Dohod_back']  # Пример нового значения
                        cursor2.execute('''
                            UPDATE Trade_pair 
                            SET pair_step_1_price = ?, 
                                pair_step_2_price = ?, 
                                pair_step_3_price = ?,
                                Dohod_go = ?,
                                Dohod_back = ?
                            WHERE pair_step_1_pair1 = ?
                        ''', (new_pair_step_1_price, new_pair_step_2_price, new_pair_step_3_price, new_dohod_go, new_dohod_back, pair_step_1_pair1))
                        conn2.commit()
                        print('Данные обновлены')
                    else:
                        # Если данных нет, добавляем новую запись
                        cursor2.execute('''
                            INSERT INTO Trade_pair (
                                site, pair_step_1, pair_step_1_pair1, pair_step_1_pair2, pair_step_1_price,
                                pair_step_2, pair_step_2_pair1, pair_step_2_pair2, pair_step_2_price,
                                pair_step_3, pair_step_3_pair1, pair_step_3_pair2, pair_step_3_price,
                                Dohod_go, Dohod_back
                            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                            obj_trade_pair['site'],
                            obj_trade_pair['pair_step_1'],
                            obj_trade_pair['pair_step_1_pair1'],
                            obj_trade_pair['pair_step_1_pair2'],
                            obj_trade_pair['pair_step_1_price'],
                            obj_trade_pair['pair_step_2'],
                            obj_trade_pair['pair_step_2_pair1'],
                            obj_trade_pair['pair_step_2_pair2'],
                            obj_trade_pair['pair_step_2_price'],
                            obj_trade_pair['pair_step_3'],
                            obj_trade_pair['pair_step_3_pair1'],
                            obj_trade_pair['pair_step_3_pair2'],
                            obj_trade_pair['pair_step_3_price'],
                            obj_trade_pair['Dohod_go'],
                            obj_trade_pair['Dohod_back']
                        ))
                        conn2.commit()
                        print('Новые данные добавлены')

                    # Закрываем соединение
                    conn2.close()
                    
                    # print(obj_trade_pair)
                    list_pair.append(list_pair_price)
            except Exception as e:
                 print(e)
                 print('error')

        conn.commit()
        conn.close()
        return list_pair

while True:
    logging.basicConfig(filename='с_pair.log', level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    try:
        price_pair_trade(take_traid_pait())
        time.sleep(5)
    except Exception as e:
        time.sleep(5)
        logging.exception("Ошибка:")