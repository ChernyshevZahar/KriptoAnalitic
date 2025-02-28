from pybit.unified_trading import HTTP
import sqlite3
import time
import logging


def take_pari_trade():
    conn2 = sqlite3.connect('pair_base_2.db')
    cursor2 = conn2.cursor()
    cl = HTTP(recv_window=60000,)
    r = cl.get_instruments_info(category="spot")
    print(len(r.get('result', {}).get('list', [])))
    for e in r.get('result', {}).get('list', []):
        try:
            cursor2.execute('''CREATE TABLE IF NOT EXISTS {} (name_pair1 TEXT, name_pair2 TEXT, nametable TEXT , website TEXT)'''.format(e.get('baseCoin')))
            # print('1')
            cursor2.execute('SELECT * FROM {} WHERE name_pair2 = ?'.format(e.get('baseCoin')), (e.get('quoteCoin'),))
            
            result = cursor2.fetchone()
            if not result:
                cursor2.execute('INSERT INTO {} (name_pair1, name_pair2, nametable,website) VALUES (?, ?, ?,?)'.format(e.get('baseCoin')), (e.get('baseCoin'), e.get('quoteCoin'), f"{e.get('baseCoin')}_{e.get('quoteCoin')}","bybit"))
                conn2.commit()
                
            # print(e.get('baseCoin'))
            # print("-----------")
        except Exception as ex:
            print(ex)
            # pass

    # Закрытие соединения
    conn2.close()




def treestr():
    conn = sqlite3.connect('pair_base_2.db')
    cursor = conn.cursor()
    conn2 = sqlite3.connect('pair_base_make_traide.db')
    cursor2 = conn2.cursor()
    # Получение списка всех таблиц
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    cursor2.execute('''CREATE TABLE IF NOT EXISTS pair (pair TEXT, count TEXT,name_site TEXT)''')
    # print(len(tables))
    # Проверка количества строк в каждой таблице
    for table in tables:
        table_name = table[0]
        cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
        count = cursor.fetchone()[0]
        if count > 1:
            cursor2.execute('INSERT INTO pair (pair, count, name_site) VALUES (?, ?, ?)', (table_name, count,"bybit"))
            
            # list_par_trade.append(table_name)

    # Закрытие соединения
    conn.commit()
    conn.close()
    conn2.commit()
    conn2.close()

while True:
    logging.basicConfig(filename='t_pair.log', level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    try:
        take_pari_trade()
        treestr()
        time.sleep(12*60*60)
    except Exception as e:
        logging.exception("Ошибка:")
        time.sleep(30)
        


