import requests
import time
from cryptoapp.models import CryptoCurrency

def update_crypto_data():
    while True:
        response = requests.get('https://api.cryptoexchange.com/rates')
        data = response.json()
        for currency in data:
            name = currency['name']
            price = currency['price']
            volume = currency['volume']
            CryptoCurrency.objects.create(name=name, price=price, volume=volume)
        time.sleep(300)


def gifhuobi():

    data = requests.get("https://api.huobi.pro/market/tickers").json()

    