import requests
import sqlite3

from decouple import config
url = config('Url')


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
            print('token:' + token)
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
        print("Токен успешно удален")
        pass
    else:
        print("Произошла ошибка при удалении токена")


def takeUsdt(Token):
    try:
        urltakeusdt = f'{url}setting-data/'
        headers = {'Authorization': f'Token {Token}'}
        response = requests.get(urltakeusdt, headers=headers)
        print(response)
        if response.status_code == 200:
            return response.json()[2]['balance']
        else:
            print("Произошла ошибка при удалении токена")
    except Exception as e:
        print(e)



def manage_settings(name: str, currency: str, gold_percentage: float):
  """
  Создает таблицу "setting", если ее нет, 
  и добавляет или обновляет данные о настройках.

  Args:
    name: Имя настройки.
    currency: Общая валюта.
    gold_percentage: Золотой процент.
  """

  with sqlite3.connect('settings.db') as conn:
    cursor = conn.cursor()

    # Создание таблицы, если ее нет
    cursor.execute("""
      CREATE TABLE IF NOT EXISTS setting (
        name TEXT PRIMARY KEY,
        currency TEXT,
        gold_percentage TEXT
      )
    """)

    # Используем INSERT OR REPLACE для более короткой записи
    cursor.execute(
        "INSERT OR REPLACE INTO setting (name, currency, gold_percentage) VALUES (?, ?, ?)",
        (name, currency, gold_percentage),
      )

    conn.commit()


def UpdateBalance(Token,balance):
    urlUpdateBalanse = f'{url}setting-data/'  # Замените на ваш URL
    headers = {'Authorization': f'Token {Token}'}
    data = {'balance': balance}

    response = requests.put(urlUpdateBalanse, headers=headers, json=data)

    if response.status_code == 200:
        print("Данные успешно обновлены:", response.json())
    else:
        print(f"Произошла ошибка: {response.status_code}", response.text)



token = takelogin(config('Login'),config('Password'))

UpdateBalance(token,101.01)

balance = takeUsdt(token)


manage_settings('USDT',balance, round(balance/10,1))

deletetoken(token)