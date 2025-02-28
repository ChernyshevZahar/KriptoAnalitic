import requests
import time

import pandas as pd
from pybit.unified_trading import HTTP
import pandas_ta as pta

from telegram import Bot

import asyncio
from decouple import config
url = config('Url')

roi = 0.01


def takelogin(user,password):
    try:
        urllogin = f'{url}api-token-auth/'
        # print(urllogin)
        data = {'username': user, 'password': password}  # Замените на фактическое имя пользователя и пароль
        
        # print('start апи')
        response = requests.post(urllogin, data=data)
        # print(response)
        if response.status_code == 200:
            token = response.json()['token']
            # print('token:' + token)
            return token
        else:
            print("Произошла ошибка при получении токена")
            print(response)
    except Exception as e:
        print(e)

def deletetoken(token):
    urldel = f'{url}api-token-delete/'
    headers = {'Authorization': f'Token {token}'}

    response = requests.delete(urldel, headers=headers)
    if response.status_code == 204:
        # print("Токен успешно удален")
        pass
    else:
        print("Произошла ошибка при удалении токена")



def take_pair(token):
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


def take_price(symbol,interval):
    cl = HTTP(recv_window=60000,)
    r = cl.get_kline(category="spot", symbol=symbol, interval=interval)
    data = r.get('result', {}).get('list', [])
    return data[0][4]

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
    return rsi_objects[-1:][0][1]



def take_macd(symbol,time):
    cl = HTTP(recv_window=60000,)
    r = cl.get_kline(category="spot", symbol=symbol, interval=time)


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

    df['Date'] = pd.to_datetime(df['Date'].astype(float), unit='ms')


    df.set_index('Date', inplace=True)


    df['ma_fast'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['ma_slow'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['macd'] = df['ma_fast'] - df['ma_slow']
    df['signail'] = df['macd'].ewm(span=9, adjust=False).mean()
    df['ms'] = df['macd'] - df['signail']

    def determine_signal(row):
        if row['ms'] > 0:
            return 'buy'
        elif row['ms'] < 0:
            return 'sell'
        else:
            return 'hold'

    df['buysell'] = df.apply(determine_signal, axis=1)

    df_2 = df[['macd', 'signail','ms','buysell']]

    def check_last_row_change(df):
        last_value = df['buysell'].iloc[-1]  # Получаем значение последней строки в столбце 'buysell'
        if len(df) > 1 and df['buysell'].iloc[-2] != last_value:
            return df.tail(3)[['ms', 'buysell']].values.tolist()
        else:
            return df.tail(1)[['ms', 'buysell']].values.tolist()

    return check_last_row_change(df_2)

# token = takelogin('zahar',1234)
# take_pair(token)

# deletetoken(token)
token_bot= config('token_bot')

user_bot = config('user_bot')

# Замените 'YOUR_BOT_TOKEN' на реальный токен вашего бота


async def send_telegram_message(chat_id_r,message):
    bot = Bot(token_bot)

    await bot.send_message(chat_id=chat_id_r, text=message)

def send_mess(pair,num1,num2,pay_price,price_now,proc_price,chat_id):
    message = f'''pair: {pair}
Цена покупки: {pay_price}
процент: {proc_price} %
Цена сейчас: {price_now}
rsi: {num1}
macd: {num2} '''
    asyncio.run(send_telegram_message(chat_id,message))



def take_pair_site(token):
    data = take_pair(token)
    data_list = {}
    unique_values = set(item['lisen_pair'] for item in data)
    for i in data:
        if i['lisen_pair'] in data_list:
            list_d =  data_list[i['lisen_pair']]
            list_d.append([i['way_pair'],i['price_pair'],i['user']])
            data_list[i['lisen_pair']] = list_d
        else:
            data_list[i['lisen_pair']] = [[i['way_pair'],i['price_pair'],i['user']]]
             # тут какая то херня
    result = list(unique_values)
    deletetoken(token)
    return result , data_list

def take_rsi_macd(list):
    list_pair = []
    for pair in list:
        rsi = take_rsi(pair,5)
        macd = take_macd(pair,5)
        list_pair.append({'pair': pair,'rsi': rsi,'macd': macd })
    return list_pair

while True:
    list_price = {}
    try:
        token = takelogin('zahar','7170902a')
        r, f=take_pair_site(token)
        list_pair = take_rsi_macd(r)
        pribl = 0
        # print(f)
        # print(list_pair)

        for pair in list_pair:
            price_now = take_price(pair['pair'],1)
            for ent in f[pair['pair']]: 
                if ent[0] == "1":
                    if pair['rsi'] < 30:
                            # print(pair['rsi'])
                            pribl = round( 1 -  float(ent[1]) / float(price_now), 10)
                            
                            send_mess(pair['pair'],pair['rsi'],pair['macd'],ent[1],price_now,round(pribl*100,2),user_bot[ent[2]])
                elif ent[0] == "0":
                    if len(pair['macd'])> 2:
                        pribl = round( 1 -  float(ent[1]) / float(price_now), 10)
                        send_mess(pair['pair'],pair['rsi'],pair['macd'],ent[1],price_now,round(pribl*100,2),user_bot[ent[2]])
                    elif pribl > roi:
                            pribl = round( 1 -  float(ent[1]) / float(price_now), 10)
                            send_mess(pair['pair'],pair['rsi'],pair['macd'],ent[1],price_now,round(pribl*100,2),user_bot[ent[2]])
                    
            

        time.sleep(120)
    except Exception as e:
        print(e)
        print('Error')
        time.sleep(30)