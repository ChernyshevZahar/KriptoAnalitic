from pybit import exceptions
from pybit.unified_trading import HTTP
from decouple import config


API_KYE = config('API_KYE')
SEKRET_KYE = config('SEKRET_KYE')


def main():

    cl = HTTP(
        api_key=API_KYE,
        api_secret=SEKRET_KYE,
        recv_window=60000,
        max_retries=1,
    )

   

    try:

    

        r = cl.place_order(
            category="spot",
            symbol="DOTUSDT",
            side="Buy",
            orderType="Limit",  # Количество указывается в USDT
            qty=1/5,                  # Покупаем DOT на сумму 1 USDT
            price=5,                # По цене 5 USDT за DOT
        )


      

        print(r)

    except exceptions.InvalidRequestError as e:
        print("ByBit API Request Error", e.status_code, e.message, sep=" | ")
    except exceptions.FailedRequestError as e:
        print("HTTP Request Failed", e.status_code, e.message, sep=" | ")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    print('Hola, AzzraelCode YT Subs!')
    main()