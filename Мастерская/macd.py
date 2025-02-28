import pandas as pd
from pybit.unified_trading import HTTP
import pytz



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

    # print(df_2.tail(10))

    def check_last_row_change(df):
        last_value = df['buysell'].iloc[-1]  # Получаем значение последней строки в столбце 'buysell'
        if len(df) > 1 and df['buysell'].iloc[-2] != last_value:
            return df.tail(3)[['ms', 'buysell']].values.tolist()
        else:
            return df.tail(1)[['ms', 'buysell']].values.tolist()
    print(check_last_row_change(df_2))

take_macd("BTCUSDT",5)
