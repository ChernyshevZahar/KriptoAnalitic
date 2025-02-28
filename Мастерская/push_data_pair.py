import json
import requests
import sqlite3
import logging
import time
from decouple import config

def create_json(cursor):
    # Выполнение запроса для извлечения данных
    cursor.execute('SELECT * FROM Trade_pair')
    rows = cursor.fetchall()

    # Преобразование данных в формат JSON
    data = []
    for row in rows:
        # print(row)
        item = {
            'site': row[0],
            'pair_step_1': row[1],
            'pair_step_1_pair1': row[2],
            'pair_step_1_pair2': row[3], 
            'pair_step_1_price' : row[4],
            'pair_step_1_price_line_up' : row[5],
            'pair_step_1_price_line_down' : row[6],
            'pair_step_2' : row[7],
            'pair_step_2_pair1' : row[8],
            'pair_step_2_pair2' : row[9],
            'pair_step_2_price' : row[10],
            'pair_step_2_price_line_up' : row[11],
            'pair_step_2_price_line_down' : row[12],
            'pair_step_3'  : row[13],
            'pair_step_3_pair1' : row[14],
            'pair_step_3_pair2' : row[15],
            'pair_step_3_price' : row[16],
            'pair_step_3_price_line_up' : row[17],
            'pair_step_3_price_line_down' : row[18],
            'dohod_go' : row[19],
            'dohod_back' : row[20],
            # Добавьте другие поля здесь
        }
        data.append(item)
    # Создание JSON файла
    with open('data.json', 'w') as file:
        json.dump(data, file)

def takelogin(user,password):
    try:
        urllogin = 'http://f91624gm.beget.tech/api-token-auth/'
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
    urldel = 'http://f91624gm.beget.tech/api-token-delete/'
    headers = {'Authorization': f'Token {token}'}

    response = requests.delete(urldel, headers=headers)
    if response.status_code == 204:
        print("Токен успешно удален")
    else:
        print("Произошла ошибка при удалении токена")



while True:
    logging.basicConfig(filename='p_pair.log', level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Отправка файла через API
    url = 'http://f91624gm.beget.tech/upload_trade_pairs'
    try:
        conn = sqlite3.connect('price_pair_trade.db')
        cursor = conn.cursor()
        create_json(cursor)
        files = {'file': open('data.json', 'rb')}
        token = takelogin(config('Login'),config('Password'))
        headers = {'Authorization': 'Token ' + str(token)}
        response = requests.post(url, files=files, headers=headers)
        deletetoken(token)

        # Закрытие соединения с базой данных
        conn.close()
        time.sleep(30)
    except Exception as e:
        time.sleep(30)
        logging.exception("Ошибка:")