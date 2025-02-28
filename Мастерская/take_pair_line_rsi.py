import sqlite3
import numpy as np
import pandas as pd
from pybit.unified_trading import HTTP
import json

import timeit
import time

import datetime

import requests

from decouple import config
url = config('Url')


def takelogin(user,password):
    try:
        urllogin = f'{url}api-token-auth/'
        # print(urllogin)
        data = {'username': user, 'password': password}  # Замените на фактическое имя пользователя и пароль
        
        print('start апи')
        response = requests.post(urllogin, data=data)
        # print(response)
        if response.status_code == 200:
            token = response.json()['token']
            print('token:' + token)
            return token
        else:
            print("Произошла ошибка при получении токена")
    except Exception as e:
        print(e)

def deletetoken(token):
    urldel = f'{url}api-token-delete/'
    headers = {'Authorization': f'Token {token}'}

    response = requests.delete(urldel, headers=headers)
    if response.status_code == 204:
        print("Токен успешно удален")
    else:
        print("Произошла ошибка при удалении токена")


def add_pair_list(pair_step):

    try:
        # Получаем значения pair_step_1_price_line_up и pair_step_1_price_line_down для данного pair_step_1 (здесь предполагается, что вы знаете, какие значения нужно добавить)
        levelsl_1,levelsh_1,price = sort_pair_line(60,pair_step)
        levelsl_5,levelsh_5,price2 = sort_pair_line(240,pair_step)
        levelsl_15,levelsh_15,price3 = sort_pair_line(360,pair_step)

        list_down = []
        list_up = []
        
        if predict_next_number(levelsl_1[-6:]) > 0:
            list_down.append(predict_next_number(levelsl_1[-6:]))
        if predict_next_number(levelsl_5[-6:]) > 0:
            list_down.append(predict_next_number(levelsl_5[-6:]))
        if predict_next_number(levelsl_15[-6:]) > 0:
            list_down.append(predict_next_number(levelsl_15[-6:]))
        if predict_next_number(levelsh_1[-6:]) > 0:
            list_up.append(predict_next_number(levelsh_1[-6:]))
        if predict_next_number(levelsh_5[-6:]) > 0:
            list_up.append(predict_next_number(levelsh_5[-6:]))
        if predict_next_number(levelsh_15[-6:]) > 0:
            list_up.append(predict_next_number(levelsh_15[-6:]))

        # print(list_down)
        # print(list_up)

        if len(list_down)>2:
            data = {'list_down': list_down}
            df = pd.DataFrame(data)
            pair_step_1_price_line_down = "{:.3f}".format(df['list_down'].mean()) if abs(df['list_down'].mean()) >= 1 else "{:.8f}".format(df['list_down'].mean())
        elif len(list_down)== 0:
            pair_step_1_price_line_down = 0
        else:
            pair_step_1_price_line_down = "{:.3f}".format(list_down[0]) if abs(list_down[0]) >= 1 else "{:.8f}".format(list_down[0])


        if len(list_up)>1:
            data2 = {"list_up" : list_up}
            df2 = pd.DataFrame(data2)
            pair_step_1_price_line_up = "{:.3f}".format(df2['list_up'].mean()) if abs(df2['list_up'].mean()) >= 1 else "{:.8f}".format(df2['list_up'].mean())
        elif len(list_up)== 0:
            pair_step_1_price_line_up = 0
        else:
            pair_step_1_price_line_up = "{:.3f}".format(list_up[0]) if abs(list_up[0]) >= 1 else "{:.8f}".format(list_up[0])

        
        return price , pair_step_1_price_line_up , pair_step_1_price_line_down
    except Exception as e:
        print(e)
def sort_pair_line(time,pair):

    

    df,price = take_pair(time,pair)

    levelsL = []
    levelsh = []
    for i in range(2,df.shape[0]-2):
      if isSupport(df,i):
        levelsL.append([i,df['Low'][i],df['Date'][i]])
      elif isResistance(df,i):
        levelsh.append([i,df['High'][i],df['Date'][i]])
    return levelsL,levelsh,price


def isResistance(df,i):
  resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] \
  and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2] 

  return resistance

def isSupport(df,i):
  support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] \
  and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]

  return support

def predict_next_number(data):
    try :
      df = pd.DataFrame(data, columns=['id', 'number', 'timestamp'])
      df['timestamp'] = df['timestamp'].astype(np.int64)

      df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

      df.set_index('timestamp', inplace=True)

      resampled_data = df['number'].resample('5min').mean().interpolate(method='linear')

      next_number = resampled_data.iloc[-1]

      return next_number
    except Exception as e:
      return 0 
    
def take_pair(time,pair):
   
    cl = HTTP(recv_window=60000,)
    r = cl.get_kline(category="spot", symbol=pair, interval=time)
    data = r.get('result', {}).get('list', [])
    df = pd.DataFrame(data).iloc[::-1].reset_index(drop=True)

    df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'volume', 'Turnover']

    for col in df.columns:
        if col != 'Date':
            if df[col].dtype == 'object':  # Проверяем, является ли тип данных в столбце строковым
                try:
                    df[col] = df[col].astype(float)  # Преобразуем значения столбца в целочисленный тип
                except ValueError:
                    print(f'Не удается преобразовать столбец {col} в целочисленный тип.')
    return df,data[0][4]




def off_take_pair(token):
    urldel = f'{url}off-trade-pairs/'
    urldel2 = f'{url}off-trade-pairs/2'
    
    headers = {'Authorization': f'Token {token}'}

    response = requests.get(urldel, headers=headers)
    response2 = requests.get(urldel2, headers=headers)

    data = response.json() if response.status_code == 200 else []
    data2 = response2.json() if response2.status_code == 200 else []

    data_pair = [item['pair'] for item in data]
    data_pair2 = [item['pair'] for item in data2]

    combined_data = data_pair + data_pair2

    return combined_data



def take_data_usdt():
    conn = sqlite3.connect('take_usdt_rsi.db')
    cursor = conn.cursor()
    token = takelogin(config('Login'),config('Password'))
    off_pair = off_take_pair(token)

    # Создание таблицы, если её не существует
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rsi_table (
            pair TEXT PRIMARY KEY,
            rsi TEXT,  -- замените на ваши названия столбцов
            price TEXT,
            price_up TEXT,
            price_down TEXT
        )
    ''')
    # print(off_pair)
    data = []
    for pair in off_pair:
        try:
            
            price , price_up, price_down = add_pair_list(pair)  
            item = {
                'site': 'bibyt',
                'pair': pair,
                'price_up' : price_up,
                'price_down' : price_down,
                # Добавьте другие поля здесь
            }
            data.append(item)
            cursor.execute(
                "INSERT OR REPLACE INTO rsi_table (pair, price_up,price_down, price) VALUES (?, ?, ?,?)",
                (pair, price_up, price_down, price )  # Распаковка значений rsi_values
            ) 
            conn.commit()
        except Exception as e:
            print(f"Ошибка при обработке пары {pair}: {e}")

    # Сохранение изменений и закрытие соединения
    
    conn.close()
    try:
        json_data = json.dumps(data)
        url2 = f'{url}upload_trade_pairs_rsi'
        headers = {
        'Authorization': 'Token ' + str(token),
        'Content-Type': 'application/json'  # Добавь заголовок для JSON
        }
        response = requests.post(url2, data=json_data, headers=headers)
        # print(response)
        deletetoken(token)
    except Exception as e:
        print(e)


while True:
    try:
        take_data_usdt()
        time.sleep(120)
    except Exception as e:
        time.sleep(30)

# execution_time = timeit.timeit("take_data_usdt()", globals=globals(), number=1) 
# print("Время выполнения:", execution_time, "секунд (450 повторений)")