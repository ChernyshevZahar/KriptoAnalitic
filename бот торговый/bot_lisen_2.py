import requests
import time
import asyncio


from pybit import exceptions
from pybit.unified_trading import HTTP

import sqlite3

import math

import pandas as pd
from pybit.unified_trading import HTTP
import pandas_ta as pta

from telegram import Bot
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from decouple import config


API_KYE = config('API_KYE')
SEKRET_KYE = config('SEKRET_KYE')

token_bot= config('token_bot')

user_bot = config('user_bot')

roi = 0.01

url = config('Url')

bot = Bot(token=token_bot)
dp = Dispatcher(bot)


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
        print(f"Произошла ошибка при удалении токена:{response.json()}")
        


def update_pair(token, lisen_pair, way_pair, price_pair):
    """
    Функция для обновления way_pair и price_pair по lisen_pair.

    Args:
        token: Токен аутентификации.
        lisen_pair: Значение lisen_pair для поиска пары.
        way_pair: Новое значение way_pair.
        price_pair: Новое значение price_pair.
    """

    url_update_site = f'{url}trading-pairs-rsi/'  # Замените ВАШ_URL на фактический URL

    headers = {'Authorization': f'Token {token}'}
    data = {'lisen_pair': lisen_pair, 'way_pair': way_pair, 'price_pair': price_pair}

    response = requests.put(url_update_site, headers=headers, json=data)

    if response.status_code == 200:
        print(f"Пара {lisen_pair} успешно обновлена.")
    else:
        print(f"Ошибка при обновлении пары {lisen_pair}: {response.status_code} {response.text}")


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

async def send_telegram_message(chat_id_r,message):
    bot = Bot(token_bot)

    await bot.send_message(chat_id=chat_id_r, text=message)

async def send_mess(pair, num1, num2, pay_price, price_now, proc_price, chat_id,have=0):
    message = f'''pair: {pair}
Цена покупки: {pay_price}
процент: {proc_price} %
Цена сейчас: {price_now}
rsi: {num1}
macd: {num2} 
купленно: {have}'''
    keyboard = create_buy_sell_keyboard(pair)
    await bot.send_message(chat_id=chat_id, text=message, reply_markup=keyboard)

async def send_mess_order_Filled(pair, chat_id):
    bot = Bot(token_bot)
    message = f'''Ордер на покупку {pair} Исполнен'''
   
    await bot.send_message(chat_id=chat_id, text=message)   

def create_buy_sell_keyboard(pair):
    keyboard = InlineKeyboardMarkup() # Используем InlineKeyboardMarkup
    buy_button = InlineKeyboardButton(text=f"Купить {pair}", callback_data=f"buy_{pair}")
    sell_button = InlineKeyboardButton(text=f"Продать 1.2% {pair}", callback_data=f"sell1_{pair}")
    sell_button_now = InlineKeyboardButton(text=f"Продать сейчас{pair}", callback_data=f"sellnow_{pair}")
    keyboard.add(buy_button, sell_button,sell_button_now)
    return keyboard

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

def BuyPair(pair,covo,prise):

    cl = HTTP(
        api_key=API_KYE,
        api_secret=SEKRET_KYE,
        recv_window=60000,
        max_retries=1,
    )

    try:

        order = cl.get_instruments_info(category='spot', symbol = pair)
        obl = order['result']['list'][0]['lotSizeFilter']['basePrecision']
        if float(obl) >= 1: 
            qty2 = round(covo,0) 
        else:

            qty2 = round(covo,len(obl.split(".")[1]))  
        print(order)
        print(covo)
        print(qty2)
        
        r = cl.place_order(
            category="spot",
            symbol=pair,
            side="Buy",
            orderType="Limit",  # Количество указывается в USDT
            qty=qty2,                  # Покупаем DOT на сумму 1 USDT
            price=prise                # По цене 5 USDT за DOT
        )

        order = cl.get_open_orders(category='spot', orderId=r['result']['orderId'])
        # r = cl.get_open_orders(category='spot')
        # r = cl.get_open_orders(category='spot', orderId='1615447093214975232')
        # r = cl.cancel_order(category="spot", orderId='xxx')
        # r = cl.cancel_all_orders(category="spot")

        return order

    except exceptions.InvalidRequestError as e:
        print("ByBit API Request Error", e.status_code, e.message, sep=" | ")
    except exceptions.FailedRequestError as e:
        print("HTTP Request Failed", e.status_code, e.message, sep=" | ")
    except Exception as e:
        print(e)

def SellPair(pair,covo,prise):

    cl = HTTP(
        api_key=API_KYE,
        api_secret=SEKRET_KYE,
        recv_window=60000,
        max_retries=1,
    )

    try:

        order = cl.get_instruments_info(category='spot', symbol = pair)
        obl = order['result']['list'][0]['lotSizeFilter']['basePrecision']
        if float(obl) >= 1: 
            qty2 = round(covo,0) 
        else:

            qty2 = round(covo,len(obl.split(".")[1])) 

        r = cl.place_order(
            category="spot",
            symbol=pair,
            side="sell",
            orderType="Limit",  # Количество указывается в USDT
            qty=qty2,                  # Покупаем DOT на сумму 1 USDT
            price=prise,                # По цене 5 USDT за DOT
        )


        # order = cl.get_open_orders(category='spot')
        order = cl.get_open_orders(category='spot', orderId=r['result']['orderId'])
        # r = cl.cancel_order(category="spot", orderId='xxx')
        # r = cl.cancel_all_orders(category="spot")
        # price = cl.get_tickers(category="spot", symbol=pair).get('result').get('list')
        # print(f' лимит на продажу{order}')
        # closeorder = cl.cancel_order(category="spot", orderId=r['result']['orderId'])
        # print(f'закрыт {closeorder}')
        if order:
            return order
        else:
            return None
        

    except exceptions.InvalidRequestError as e:
        print("ByBit API Request Error", e.status_code, e.message, sep=" | ")
    except exceptions.FailedRequestError as e:
        print("HTTP Request Failed", e.status_code, e.message, sep=" | ")
    except Exception as e:
        print(e)

def get_dohod(colwo_buy,prise_buy,prise_sell):
    dohod = round(prise_sell * colwo_buy - prise_buy*colwo_buy,3)
    return dohod


def get_assets(cl : HTTP, coin):
    """
    Получаю остатки на аккаунте по конкретной монете
    :param cl:
    :param coin:
    :return:
    """
    r = cl.get_wallet_balance(accountType="UNIFIED")
    assets = {
        asset.get('coin') : float(asset.get('availableToWithdraw', '0.0'))
        for asset in r.get('result', {}).get('list', [])[0].get('coin', [])
    }
    return assets.get(coin, 0.0)

def update_balance(token,dohod):
    url_update_site = f'{url}setting-data/'  # Замените ВАШ_URL на фактический URL

    headers = {'Authorization': f'Token {token}'}

    response = requests.get(url_update_site, headers=headers)

    if response.status_code == 200:
        print("Данные баланса взяты")

        for item in response.json():
            if item['name'] == 'My_USDT':
                my_usdt_balance = item['balance']
                break  # Выходим из цикла, как только нашли нужный элемент
    else:
        print(f"Ошибка при обновлении пары : {response.status_code} {response.text}")
    balanse = my_usdt_balance  + dohod
    print(balanse)
    data = {'balance':balanse}
    response = requests.put(url_update_site, headers=headers,json=data)

    if response.status_code == 200:
        print("Данные баланса обновлены")
    else:
        print(f"Ошибка при обновлении пары : {response.status_code} {response.text}")


def round_down_to_decimals(number, decimals):
  """Округляет число в меньшую сторону до заданного количества знаков после запятой.

  Args:
    number: Число, которое нужно округлить.
    decimals: Количество знаков после запятой.

  Returns:
    Округленное число.
  """

  factor = 10 **decimals
  return math.floor(number*factor ) / factor


def take_info_order(token):


    list_order_id = get_all_num_id_order()
    list_end_order = []
    for orderId in list_order_id:
        try:
            cl = HTTP(
                api_key=API_KYE,
                api_secret=SEKRET_KYE,
                recv_window=60000,
                max_retries=1,
            )
            order = cl.get_open_orders(category='spot', orderId=orderId[0])
            # print(order)
       
            if order['result']['list'][0]['orderStatus'] == 'Filled':
                if orderId[1] == 'buy':
                    balanse = get_assets(cl,order['result']['list'][0]['symbol'].replace("USDT", ""))
                    # time.sleep(2)
                    order2 = cl.get_instruments_info(category='spot', symbol = order['result']['list'][0]['symbol'])
                    # print(order2)
                    obl = order2['result']['list'][0]['lotSizeFilter']['basePrecision']
                    if float(obl) >= 1: 
                        qty2 = round_down_to_decimals(balanse,0) 
                    else:

                        qty2 = round_down_to_decimals(balanse,len(obl.split(".")[1]))

                     
                    sprice =  get_balance_data(order['result']['list'][0]['symbol'])
                    
                    # print(order['result']['list'][0])
                    
                    if sprice is not None:
                        ocerg = sprice[2]
                        balanse2 =  sprice[1]
                                
                    else:
                        print(qty2)
                        balanse2 = qty2
                        sell_price = float(order['result']['list'][0]['price'])*1.014
                        # print(sell_price)
                        obl3 = order['result']['list'][0]['price']
                        if float(obl3) >= 1: 
                            ocerg = round_down_to_decimals(sell_price,0) 
                        else:

                            ocerg = round_down_to_decimals(sell_price,len(obl3.split(".")[1])) 
                        
                    print(qty2)
                    print(ocerg)
                    print(balanse2)
                    result_sell = SellPair(order['result']['list'][0]['symbol'],balanse2,ocerg)
                    print(result_sell)
                    if result_sell is not None:
                        create_lots_db(order['result']['list'][0]['symbol'],result_sell['result']['list'][0]['orderId'],result_sell['result']['list'][0]['orderStatus'],'sell')

                    create_data_orders_db(order['result']['list'][0]['symbol'],order['result']['list'][0]['price'],qty2,ocerg)
                    delete_lots_order(order['result']['list'][0]['orderId'])
                    list_end_order.append(order['result']['list'][0]['symbol'])
                    data_have = get_balance_data(order['result']['list'][0]['symbol'])
                    try:
                        update_pair(token,order['result']['list'][0]['symbol'],0,data_have[0])
                    except Exception as e:
                        print(e)
                        pass
                elif orderId[1] == 'sell':

                    
                    
                    prise_buy = get_price_from_db(order['result']['list'][0]['symbol']) 

                    dohod = get_dohod(order['result']['list'][0]['leavesQty'],prise_buy,order['result']['list'][0]['basePrice'])
                    update_balance(token,dohod)
                    delete_data_orders_row(order['result']['list'][0]['symbol'])
                    delete_lots_order(order['result']['list'][0]['orderId'])
                    list_end_order.append(order['result']['list'][0]['symbol'])
        except Exception as e:
            print(e)
    return list_end_order

def create_table_and_update_or_insert(name, currency, gold_percentage):
    """Создает таблицу setting (если не существует) 
       и обновляет/вставляет данные.

    Args:
        name: Значение для столбца 'name'.
        currency: Значение для столбца 'currency'.
        gold_percentage: Значение для столбца 'gold_parcentage'.
    """

    conn = sqlite3.connect('settings.db')  # Подключение к базе данных
    cursor = conn.cursor()

    try:
        # Создание таблицы setting, если она не существует
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS setting (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE,
                currency TEXT,
                gold_parcentage REAL
            )
        ''')

        # Проверка, есть ли уже запись с таким именем
        cursor.execute("SELECT 1 FROM setting WHERE name = ?", (name,))
        exists = cursor.fetchone()

        if exists:
            # Если запись существует, обновляем ее
            cursor.execute("""
                UPDATE setting 
                SET currency = ?, gold_parcentage = ? 
                WHERE name = ?
            """, (currency, gold_percentage, name))
            print(f"Запись с name = '{name}' обновлена.")
        else:
            # Если записи нет, вставляем новую
            cursor.execute("""
                INSERT INTO setting (name, currency, gold_parcentage) 
                VALUES (?, ?, ?)
            """, (name, currency, gold_percentage))
            print(f"Новая запись с name = '{name}' добавлена.")

        conn.commit()

    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")

    finally:
        conn.close()

def get_gold_percentage(name="My_USDT"):
  """
  Получает значение gold_percentage из базы данных settings.db 
  для записи с указанным name.

  Args:
      name: Имя записи в таблице 'setting' (по умолчанию "USDT").

  Returns:
      Значение gold_percentage (float) или None, если запись не найдена.
  """
  with sqlite3.connect('settings.db') as conn:
    cursor = conn.cursor()

    cursor.execute("SELECT gold_parcentage FROM setting WHERE name = ?", (name,))
    row = cursor.fetchone()

    if row:
      return row[0]  # gold_percentage - первый (и единственный) элемент в кортеже row
    else:
      return None

# Обработчик кнопки "Купить"
@dp.callback_query_handler(lambda c: c.data.startswith('buy_'))
async def handle_buy(callback_query: types.CallbackQuery):
    pair = callback_query.data.split("_")[1]
    message_text = callback_query.message.text  # Получаем текст сообщения
    
    # Парсинг данных из сообщения 
    lines = message_text.splitlines()
    pair = lines[0].split(": ")[1]
    current_price = lines[3].split(": ")[1]
    
    usdt_10 = get_gold_percentage()
    pay=float(usdt_10)/float(current_price)
    # print(pay)
    result_buy = BuyPair(pair,pay, round(float(current_price),len(current_price.split(".")[1])) )
    print(result_buy)
    # print(f"{pair,result_buy['result']['list'][0]['orderId'],result_buy['result']['list'][0]['orderStatus']}")
    create_lots_db(pair,result_buy['result']['list'][0]['orderId'],result_buy['result']['list'][0]['orderStatus'],'buy')

    # Формируем текст ответа с данными
    response_text = f"Статус покупки {result_buy['retMsg']}\n" \
                    f"Номер ордера: {result_buy['result']['list'][0]['orderId']}\n" \
                    

    await bot.answer_callback_query(callback_query.id, text=response_text, show_alert=True)

# Обработчик кнопки "Продать"
@dp.callback_query_handler(lambda c: c.data.startswith('sell1_'))
async def handle_sell_12(callback_query: types.CallbackQuery):
    pair = callback_query.data.split("_")[1]
    message_text = callback_query.message.text
    # Парсинг данных из сообщения 
    lines = message_text.splitlines()
    pair = lines[0].split(": ")[1]
    pair_1 = lines[1].split(": ")[1]
    # current_price = float(lines[3].split(": ")[1])
    obem = lines[6].split(": ")[1]
    

   
    result_buy = SellPair(pair,float(obem), round(float(pair_1)*1.015,len(pair_1.split(".")[1])))
    # print(f"{pair,result_buy['result']['list'][0]['orderId'],result_buy['result']['list'][0]['orderStatus']}")
    create_lots_db(pair,result_buy['result']['list'][0]['orderId'],result_buy['result']['list'][0]['orderStatus'],'sell')
    # print(result_buy)
    # Формируем текст ответа с данными
    response_text = f"Статус покупки {result_buy['retMsg']}\n" \
                    f"Номер ордера: {result_buy['result']['list'][0]['orderId']}\n" \
                    

    await bot.answer_callback_query(callback_query.id, text=response_text, show_alert=True)


@dp.callback_query_handler(lambda c: c.data.startswith('sellnow_'))
async def handle_sell_now(callback_query: types.CallbackQuery):
    pair = callback_query.data.split("_")[1]
    message_text = callback_query.message.text
    # Парсинг данных из сообщения 
    lines = message_text.splitlines()
    pair = lines[0].split(": ")[1]
    current_price = float(lines[3].split(": ")[1])
    obem = lines[6].split(": ")[1]
    

   
    result_buy = SellPair(pair,float(obem), round(float(current_price),len(current_price.split(".")[1])))
    # print(f"{pair,result_buy['result']['list'][0]['orderId'],result_buy['result']['list'][0]['orderStatus']}")
    create_lots_db(pair,result_buy['result']['list'][0]['orderId'],result_buy['result']['list'][0]['orderStatus'],'sell')
    # print(result_buy)
    # Формируем текст ответа с данными
    response_text = f"Статус покупки {result_buy['retMsg']}\n" \
                    f"Номер ордера: {result_buy['result']['list'][0]['orderId']}\n" \
                    

    await bot.answer_callback_query(callback_query.id, text=response_text, show_alert=True)


def create_lots_db(pair, num_id_order, status,type):
    conn = sqlite3.connect('lots.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lots_order (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pair TEXT NOT NULL,
            num_id_order INTEGER UNIQUE,
            status TEXT,
            type TEXT
        )
    ''')


    try:
        cursor.execute(
            '''
            INSERT INTO lots_order (pair, num_id_order, status,type)
            VALUES (?, ?, ?, ?)
            ''',
            (pair, num_id_order, status, type)
        )
        conn.commit()
        print(f'Запись с номером ордера {num_id_order} успешно добавлена.')
    except sqlite3.IntegrityError:
        print(f'Запись с номером ордера {num_id_order} уже существует.')
    finally:
        conn.close()


def get_price_from_db(pair):
    """Получает значение price из базы данных для заданной пары.

    Args:
        pair: Строка, представляющая торговую пару (например, 'BTCUSDT').

    Returns:
        float: Значение price из базы данных для указанной пары или None, 
               если пара не найдена.
    """

    conn = sqlite3.connect('Data_orders.db')
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT price FROM balance WHERE pair = ?", (pair,))
        result = cursor.fetchone()

        if result:
            return result[0]  # Возвращаем первое (и единственное) значение из кортежа
        else:
            print(f"Пара '{pair}' не найдена в базе данных.")
            return None

    except sqlite3.Error as e:
        print(f"Ошибка при получении цены из базы данных: {e}")
        return None

    finally:
        conn.close()

def delete_lots_order(num_id_order):
    conn = sqlite3.connect('lots.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        DELETE FROM lots_order
        WHERE num_id_order = ?
        ''',
        (num_id_order,)
    )
    conn.commit()
    conn.close()
    print(f'Запись с номером ордера {num_id_order} удалена.')

def get_all_num_id_order():

    try:
        """
        Функция для получения всех num_id_order из таблицы lots_order.
        """
        conn = sqlite3.connect('lots.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT num_id_order, type FROM lots_order
        ''')

        # Получаем все результаты запроса
        results = cursor.fetchall()

        # Извлекаем num_id_order из кортежей результатов
        num_id_orders = [[row[0],row[1]] for row in results]

        conn.close()

        return num_id_orders
    except Exception as e:
        print(e)
        return None

def create_data_orders_db(pair, price, clowo,sellprice):
    conn = sqlite3.connect('Data_orders.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS balance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pair TEXT UNIQUE,
            price REAL,
            clowo REAL,
            sellprice REAL
        )
    ''')

    try:
        cursor.execute(
            '''
            INSERT INTO balance (pair, price, clowo,sellprice)
            VALUES (?, ?, ?,?)
            ''',
            (pair, price, clowo,sellprice)
        )
        conn.commit()
        print(f'Новая пара {pair} добавлена.')
    except sqlite3.IntegrityError:
        cursor.execute('SELECT price, clowo FROM balance WHERE pair = ?', (pair,))
        existing_price, existing_clowo = cursor.fetchone()
        new_price = (float(existing_price) + float(price)) / 2
        
        cursor.execute(
            '''
            UPDATE balance
            SET price = ?, clowo = ?
            WHERE pair = ?
            ''',
            (new_price, clowo, pair)
        )
        conn.commit()
        print(f'Пара {pair} обновлена.')
    finally:
        conn.close()


def delete_data_orders_row(pair):
    conn = sqlite3.connect('Data_orders.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM balance WHERE pair = ?', (pair,))
    conn.commit()
    conn.close()
    print(f'Пара {pair} удалена.')


def get_balance_data(pair):
    """
    Получает данные из таблицы balance по заданной паре.

    Args:
        pair: Имя пары (например, 'BTCUSDT').

    Returns:
        Кортеж (price, clowo) или None, если пара не найдена.
    """
    conn = sqlite3.connect('Data_orders.db')
    cursor = conn.cursor()

    cursor.execute('SELECT price, clowo, sellprice FROM balance WHERE pair = ?', (pair,))
    data = cursor.fetchone()

    conn.close()

    if data:
        return data  # Возвращаем кортеж (price, clowo)
    else:
        return None  # Пара не найдена

def take_balanse():

    token1 = takelogin(config('Login'),config('Password'))

    url_update_site = f'{url}setting-data/'  # Замените ВАШ_URL на фактический URL

    headers = {'Authorization': f'Token {token1}'}

    response = requests.get(url_update_site, headers=headers)

    if response.status_code == 200:
        print("Данные баланса взяты")

        for item in response.json():
            if item['name'] == 'My_USDT':
                my_usdt_balance = item['balance']
                break  # Выходим из цикла, как только нашли нужный элемент
    else:
        print(f"Ошибка при обновлении пары : {response.status_code} {response.text}")


    create_table_and_update_or_insert('My_USDT',my_usdt_balance,round(my_usdt_balance/10,2))


    deletetoken(token1)

    pass

async def check_and_send_signals():
    take_balanse()
    while True:
        try:
            token = takelogin(config('Login'),config('Password'))
            # print(token)
            order_buying = take_info_order(token)
            # print(2)
            r, f=take_pair_site(token)
            list_pair = take_rsi_macd(r)
            # print(3)
            pribl = 0
            # deletetoken(token)


            for pair in list_pair:
                if order_buying:
                    if pair['pair'] in order_buying: 
                        await send_mess_order_Filled(pair['pair'],user_bot['zahar'])

                price_now = take_price(pair['pair'],1)
                # print(4)
                for ent in f[pair['pair']]: 

                    if ent[0] == "1":
                        if pair['rsi'] < 30:

                            pribl = round( 1 -  float(ent[1]) / float(price_now), 10)
                            data_have = get_balance_data(pair['pair'])
                            if data_have:
                                await send_mess(pair['pair'],pair['rsi'],pair['macd'],ent[1],price_now,round(pribl*100,2),user_bot[ent[2]],data_have[1])
                            else:
                                await send_mess(pair['pair'],pair['rsi'],pair['macd'],ent[1],price_now,round(pribl*100,2),user_bot[ent[2]])
                    elif ent[0] == "0":
                        if len(pair['macd'])> 2:
                            pribl = round( 1 -  float(ent[1]) / float(price_now), 10)
                            data_have = get_balance_data(pair['pair'])
                            if data_have:
                                await send_mess(pair['pair'],pair['rsi'],pair['macd'],ent[1],price_now,round(pribl*100,2),user_bot[ent[2]],data_have[1])
                            else:
                                await send_mess(pair['pair'],pair['rsi'],pair['macd'],ent[1],price_now,round(pribl*100,2),user_bot[ent[2]])
                        elif pribl > roi:
                            pribl = round( 1 -  float(ent[1]) / float(price_now), 10)
                            data_have = get_balance_data(pair['pair'])
                            if data_have:
                                await send_mess(pair['pair'],pair['rsi'],pair['macd'],ent[1],price_now,round(pribl*100,2),user_bot[ent[2]],data_have[1])
                            else:
                                await send_mess(pair['pair'],pair['rsi'],pair['macd'],ent[1],price_now,round(pribl*100,2),user_bot[ent[2]])
                    
            await asyncio.sleep(120)  # Пауза в 120 секунд 
        except Exception as e:
            print(e)
            print('Error')
            await asyncio.sleep(5) 

async def on_startup(dp):
    print("Бот запущен!")
    
    asyncio.create_task(check_and_send_signals())

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)

