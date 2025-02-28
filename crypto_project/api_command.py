import requests
from datetime import datetime
from datetime import  timedelta
import time
from os import getenv

def takelogin(user,password):
    urllogin = 'http://127.0.0.1:8000/api-token-auth/'
    data = {'username': user, 'password': password}  # Замените на фактическое имя пользователя и пароль

    response = requests.post(urllogin, data=data)

    if response.status_code == 200:
        token = response.json()['token']
        print('token:' + token)
        return token
    else:
        print("Произошла ошибка при получении токена")


def deletetoken(token):
    urldel = 'http://127.0.0.1:8000/api-token-delete/'
    headers = {'Authorization': f'Token {token}'}

    response = requests.delete(urldel, headers=headers)
    if response.status_code == 204:
        print("Токен успешно удален")
    else:
        print("Произошла ошибка при удалении токена")
        

def updatedata(token,obj,id):

    # Обновление данных
    url = f'http://127.0.0.1:8000/api/numberdata/{id}/'  # Замените на фактический URL вашего API-эндпоинта и ID записи, которую вы хотите обновить
    headers = {'Authorization': f'Token {token}'}
     # Замените на актуальные данные для обновления

    response = requests.put(url, data=obj, headers=headers)

    if response.status_code == 200:
        print("Данные успешно обновлены")
    else:
        print("Произошла ошибка при обновлении данных")


def getdata(token,site,pair):
    url = f'http://127.0.0.1:8000/api/numberdata/{site}/{pair}/'
    headers = {'Authorization': f'Token {token}'}  # Замените на фактический URL вашего API-эндпоинта
    response = requests.get(url,headers=headers)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Произошла ошибка при получении данных")


def gifkucoin(token):
    print('start kucoin')
    data = requests.get("https://api.kucoin.com/api/v1/market/allTickers").json()
    objdata = {}
    for ss in data['data']['ticker']:
        objdata['site'] = 'kucoin'
        objdata['pair'] = ss['symbolName'].replace('-', '')
        try:
            changedata(token,ss,objdata)
        except Exception as e:
            print(e)
        # createUpData(objdata)
    print('Stop kucoin')


def changedata(token,ss,obj):
    datajd = getdata(token,obj['site'],obj['pair'])[0]
    datajd['askPrice'] = ss['sell']
    datajd['askSize'] = ss['bestBidSize']
    datajd['priсe'] = ss['last']
    datajd['bidSize'] = ss['bestAskSize']
    datajd['bid'] = ss['buy']
    t1m = timechak(datajd,'1m',1)
    datajd['datetime_1m'] = t1m['datetime_1m']
    datajd['priсe_1m'] = t1m['priсe_1m']
    t5m = timechak(datajd,'5m',5)
    datajd['datetime_5m'] = t5m['datetime_5m']
    datajd['priсe_5m'] = t5m['priсe_5m']
    t15m = timechak(datajd,'15m',15)
    datajd['datetime_15m'] = t15m['datetime_15m']
    datajd['priсe_15m'] = t15m['priсe_15m']
    t30m = timechak(datajd,'30m',30)
    datajd['datetime_30m'] = t30m['datetime_30m']
    datajd['priсe_30m'] = t30m['priсe_30m']
    t1h = timechak(datajd,'1h',60)
    datajd['datetime_1h'] = t1h['datetime_1h']
    datajd['priсe_1h'] = t1h['priсe_1h']
    t3h = timechak(datajd,'3h',180)
    datajd['datetime_3h'] = t3h['datetime_3h']
    datajd['priсe_3h'] = t3h['priсe_3h']
    t6h = timechak(datajd,'6h',360)
    datajd['datetime_6h'] = t6h['datetime_6h']
    datajd['priсe_6h'] = t6h['priсe_6h']
    t12h = timechak(datajd,'12h',720)
    datajd['datetime_12h'] = t12h['datetime_12h']
    datajd['priсe_12h'] = t12h['priсe_12h']
    t1d = timechak(datajd,'1d',1440)
    datajd['datetime_1d'] = t1d['datetime_1d']
    datajd['priсe_1d'] = t1d['priсe_1d']

    # print(datajd['id'])
    updatedata(token,datajd,datajd['id'])

def timechak(obj,time,ctime):
    # print(obj)
    testodj = {}
    try:
        datetimed = 'datetime_' + time
        priсe = 'priсe_' + time
        current_time = datetime.now() + timedelta(hours=3)
        if obj[datetimed] is not None:
            obj[datetimed] = datetime.fromisoformat(obj[datetimed])  # Преобразование строки в объект datetime
            
            time_difference = current_time - obj[datetimed].replace(tzinfo=None)  # Убираем информацию о смещении времени

            if time_difference > timedelta(minutes=ctime):
                testodj[priсe] = obj['priсe']
                testodj[datetimed] = current_time
                return testodj
            else:
                testodj[priсe] = obj[priсe]
                testodj[datetimed] = obj[datetimed]
                return testodj
    except Exception as e:
        print(e)
        pass




token = takelogin(getenv('Login'),getenv('Password'))


gifkucoin(token)



deletetoken(token)
