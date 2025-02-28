import sqlite3
import pandas as pd
from pybit.unified_trading import HTTP
import pandas_ta as pta
import time
import json

from telegram import Bot

import asyncio


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

def take_pair_base(token):
    urldel = f'{url}trading-pairs/'
    urldel2 = f'{url}trading-pairs-rsi/'
    headers = {'Authorization': f'Token {token}'}
    data = {}
    data2 = {}

    response = requests.get(urldel, headers=headers)
    response2 = requests.get(urldel2, headers=headers)
    if response.status_code == 200:
            data = response.json()
            
    else:
        print(response.status_code)
        print("Произошла ошибка при получении токена")

    if response2.status_code == 200:
            data2 = response2.json()
            
    else:
        print(response2.status_code)
        print("Произошла ошибка при получении токена")

    
    if len(data) == 0:
        return data2
    elif len(data2) == 0:
        return data
    else:
        return data + data2




def off_take_pair(token):
    urldel = f'{url}off-trade-pairs'
    
    headers = {'Authorization': f'Token {token}'}

    response = requests.get(urldel, headers=headers)
    # print(response.text)
    if response.status_code == 200:
            data = response.json()
            
    else:
        print(response.status_code)
        print("Произошла ошибка при получении токена")
    
    data_pair = [item['pair'] for item in data]

    return data_pair



def take_rsi(symbol,interval):
    try:
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
    except Exception as e:
        rsi_objects = 50

    
    return rsi_objects[-1:][0][1],  data[0][4]



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


def take_data_usdt():
    conn = sqlite3.connect('take_usdt_rsi.db')
    cursor = conn.cursor()
    token = takelogin(config('Login'),config('Password'))
    off_pair = off_take_pair(token)
    print(len(off_pair))
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
    data = []
    for pair in off_pair:
        try:
           
            rsi, price = take_rsi(pair, 5)
            item = {
                'site': 'bibyt',
                'pair': pair,
                'pair_price' : price,
                'pair_rsi' : rsi,
                # Добавьте другие поля здесь
            }
            data.append(item)
            cursor.execute(
                "INSERT OR REPLACE INTO rsi_table (pair, rsi, price) VALUES (?, ?,?)",
                (pair, rsi, price )  # Распаковка значений rsi_values
            ) 
            conn.commit()
        except Exception as e:
            print(f"Ошибка при обработке пары {pair}: {e}")

    # Сохранение изменений и закрытие соединения
    db_off = take_pair_base(token)
    db_pair_off = list(item['lisen_pair'] for item in db_off)
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
       
    except Exception as e:
        print(e)
    
    send_mess(user_bot['zahar'],data,db_pair_off)
    deletetoken(token)

token_bot= config('token_bot')

user_bot = config('user_bot')

# Замените 'YOUR_BOT_TOKEN' на реальный токен вашего бота


async def send_telegram_message(chat_id_r,message):
    bot = Bot(token_bot)

    await bot.send_message(chat_id=chat_id_r, text=message)

def send_mess(chat_id,arr_pair,off_pair):
    message = ""
    for i in arr_pair:
        if i['pair'] not in off_pair:
            if i["pair_rsi"] < 30:
                message = message + f'pair: {i["pair"]}, Цена {i["pair_price"]}, rsi: {i["pair_rsi"]}' + '\n'
                asyncio.run(send_telegram_message(chat_id,message))



while True:
    try:
        take_data_usdt()
        time.sleep(30)
    except Exception as e:
        time.sleep(30)

