import json
import requests
import sqlite3
import logging
import time


from decouple import config
url = config('Url')

def create_json(cursor):
    # Выполнение запроса для извлечения данных
    cursor.execute('SELECT * FROM rsi_table')
    rows = cursor.fetchall()
    # Преобразование данных в формат JSON
    data = []
    for row in rows:
        if float(row[1]) > 30.0:
            norm = False
        else:
            norm = True
        # print(row)
        item = {
            'site': 'bibyt',
            'pair': row[0],
            'pair_up': row[3],
            'pair_down': row[4], 
            'pair_price' : row[2],
            'pair_rsi' : row[1],
            'norm': norm
            # Добавьте другие поля здесь
        }
        data.append(item)
    # Создание JSON файла
    with open('data_rsi.json', 'w') as file:
        json.dump(data, file)

def takelogin(user,password):
    try:
        urllogin = f'{url}api-token-auth/'
        print(urllogin)
        data = {'username': user, 'password': password}  # Замените на фактическое имя пользователя и пароль
        
        print('start апи')
        response = requests.post(urllogin, data=data)
        print(response)
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



while True:
    logging.basicConfig(filename='p_pair.log', level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Отправка файла через API
    url2 = f'{url}upload_trade_pairs_rsi'
    try:
        conn = sqlite3.connect('take_usdt_rsi.db')
        cursor = conn.cursor()
        create_json(cursor)
        files = {'file': open('data_rsi.json', 'rb')}
        token = takelogin('zahar','1234')
        headers = {'Authorization': 'Token ' + str(token)}
        response = requests.post(url2, files=files, headers=headers)
        deletetoken(token)

        # Закрытие соединения с базой данных
        conn.close()
        time.sleep(1200)
    except Exception as e:
        print(e)
        time.sleep(300)
        logging.exception("Ошибка:")


