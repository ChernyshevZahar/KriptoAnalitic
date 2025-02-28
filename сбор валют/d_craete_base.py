import requests
import sqlite3
import pytz
import time
import datetime
import traceback

"""
Сбор данных с биржи kucoin
"""

def gifkucoin():
    
    data = requests.get("https://api.kucoin.com/api/v1/market/allTickers").json()
    
    for ss in data['data']['ticker']:
        sql_base(ss,'kucoin_data_2.db','kucoin')
        # print(ss)
        # break
        
    # time.sleep(time)

 # придумай чтобы создавалась 3 базы на 5 15 и 30 минут чтобы проверялось если время ещё не прошло не указвать туду если прошло записывать данные как в по секундные базы

def sql_base(base, name,site):
    conn = sqlite3.connect(name)
    conn2 = sqlite3.connect('pair_base.db')
    conn_5 = sqlite3.connect('min_5_base.db')
    conn_15 = sqlite3.connect('min_15_base.db')
    conn_30 = sqlite3.connect('min_30_base.db')
    cursor = conn.cursor()
    cursor2 = conn2.cursor()
    cursor5 = conn_5.cursor()
    cursor15 = conn_15.cursor()
    cursor30 = conn_30.cursor()
    try:
        if "1"  in base['symbolName']:
            base['symbolName'] = base['symbolName'].replace("1", "one")
        name_pair  = base['symbolName'].split("-")
        
        table_name = base['symbolName'].replace("-", "_")

        cursor2.execute('''CREATE TABLE IF NOT EXISTS {} (name_pair1 TEXT, name_pair2 TEXT, nametable TEXT , website TEXT)'''.format(name_pair[0]))
        cursor2.execute('SELECT * FROM {} WHERE name_pair2 = ?'.format(name_pair[0]), (name_pair[1],))
        result = cursor.fetchone()
        if not result:
            cursor2.execute('INSERT INTO {} (name_pair1, name_pair2, nametable,website) VALUES (?, ?, ?,?)'.format(name_pair[0]), (name_pair[0], name_pair[1], table_name,site))
            conn2.commit()
            conn2.close()
        
        create_str(table_name,cursor, base,60)
        delete_old_records(table_name,cursor)
        create_str(table_name+"_5",cursor5, base,300)
        delete_old_records(table_name+"_5",cursor5)
        create_str(table_name+"_15",cursor15, base,900)
        delete_old_records(table_name+"_15",cursor15)
        create_str(table_name+"_30",cursor30, base,1800)
        delete_old_records(table_name+"_30",cursor30)
        
        

            
        
    except Exception as e:
        print(e)
        # traceback.print_exc()
    
    conn_5.commit()
    conn_5.close()
    conn_15.commit()
    conn_15.close()
    conn_30.commit()
    conn_30.close()

    conn.commit()
    conn.close()

def create_str(name, crusorr,base,time):
   
    current_time_moscow = datetime.datetime.now()
    current_time_moscow = current_time_moscow + datetime.timedelta(hours=3)
    try:
            crusorr.execute('SELECT price FROM {} ORDER BY event_date DESC LIMIT 1'.format(name))
            result = crusorr.fetchone()
            last_price = float(result[0])
            price_diff = round(((float(base['last']) - last_price) / last_price) * 100,2) if last_price != 0.0 else 0.0
           
            crusorr.execute('SELECT event_date FROM {} ORDER BY event_date DESC LIMIT 1'.format(name))
            last_added_time_str =  crusorr.fetchone()[0].split('.')[0]
            
            last_added_time = datetime.datetime.strptime(last_added_time_str, '%Y-%m-%d %H:%M:%S')
    except Exception as e:
            price_diff = 0.0
            last_added_time = None

      

    
       
    if last_added_time is None: 

        crusorr.execute('''CREATE TABLE IF NOT EXISTS {} (price REAL, event_date DATE, price_diff REAL)'''.format(name))
    
        crusorr.execute('INSERT INTO {} (price, event_date,price_diff) VALUES (?, ?, ?)'.format(name),
                        (float(base['last']), current_time_moscow, price_diff )) 
    else:
        time_difference = current_time_moscow - last_added_time
        if time_difference.total_seconds() > time:
            # print(name)
            crusorr.execute('''CREATE TABLE IF NOT EXISTS {} (price REAL, event_date DATE, price_diff REAL)'''.format(name))
    
            crusorr.execute('INSERT INTO {} (price, event_date,price_diff) VALUES (?, ?, ?)'.format(name),
                            (float(base['last']), current_time_moscow, price_diff ))

def delete_old_records(table_name,cursorrr):
    
    try:
        # Вычисляем время, старше которого нужно удалить записи (48 часов назад)
        cutoff_time = datetime.datetime.now() - datetime.timedelta(hours=48)
        
        # Удаляем записи, которые старше cutoff_time
        cursorrr.execute('DELETE FROM {} WHERE event_date < ?'.format(table_name), (cutoff_time,))
        
    except Exception as e:
        print(e)
    
def add_data(table_name, data):
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM {} WHERE column2 = ?'.format(table_name), (data[1],))
    result = cursor.fetchone()
    if not result:
        cursor.execute('INSERT INTO {} (column1, column2, website) VALUES (?, ?, ?)'.format(table_name), (data[0], data[1], data[2]))
        conn.commit()


while True:
    try:
        
        gifkucoin()
        
        # break
    except Exception as e:
        # print(e)
        time.sleep(3)