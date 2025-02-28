import pandas as pd
import numpy as np
from pybit.unified_trading import HTTP
import sqlite3
import logging
import time

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
    return df


def isSupport(df,i):
  support = df['Low'][i] < df['Low'][i-1]  and df['Low'][i] < df['Low'][i+1] \
  and df['Low'][i+1] < df['Low'][i+2] and df['Low'][i-1] < df['Low'][i-2]

  return support

def isResistance(df,i):
  resistance = df['High'][i] > df['High'][i-1]  and df['High'][i] > df['High'][i+1] \
  and df['High'][i+1] > df['High'][i+2] and df['High'][i-1] > df['High'][i-2] 

  return resistance


def predict_next_number(data):
    try :
      df = pd.DataFrame(data, columns=['id', 'number', 'timestamp'])
      df['timestamp'] = df['timestamp'].astype(np.int64)

      df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

      df.set_index('timestamp', inplace=True)

      resampled_data = df['number'].resample('5min').mean().interpolate(method='linear')

      next_number = resampled_data.iloc[-1]

      return next_number
    except Exception as e:
      return 0 



def sort_pair_line(time,pair):

    df = take_pair(time,pair)

    levelsL = []
    levelsh = []
    for i in range(2,df.shape[0]-2):
      if isSupport(df,i):
        levelsL.append([i,df['Low'][i],df['Date'][i]])
      elif isResistance(df,i):
        levelsh.append([i,df['High'][i],df['Date'][i]])
    return levelsL,levelsh


# levelsh,levelsL = sort_pair_line(5,"BTCUSDT")


def add_pair_list(pair_step,cursor2,line_up,line_down):
 
  cursor2.execute('SELECT {} FROM Trade_pair'.format(pair_step))
  pair_step_1_values = cursor2.fetchall()
  # Проходим по каждому значению pair_step_1 и добавляем значения pair_step_1_price_line_up и pair_step_1_price_line_down на основе этого значения
  for pair_step_1 in pair_step_1_values:
      
      # Получаем значения pair_step_1_price_line_up и pair_step_1_price_line_down для данного pair_step_1 (здесь предполагается, что вы знаете, какие значения нужно добавить)
      levelsl_1,levelsh_1 = sort_pair_line(1,pair_step_1[0])
      levelsl_5,levelsh_5 = sort_pair_line(5,pair_step_1[0])
      levelsl_15,levelsh_15 = sort_pair_line(15,pair_step_1[0])

      list_down = []
      list_up = []
      
      if predict_next_number(levelsl_1[-6:]) > 0:
         list_down.append(predict_next_number(levelsl_1[-6:]))
      if predict_next_number(levelsl_5[-6:]) > 0:
         list_down.append(predict_next_number(levelsl_5[-6:]))
      if predict_next_number(levelsl_15[-6:]) > 0:
         list_down.append(predict_next_number(levelsl_15[-6:]))
      if predict_next_number(levelsh_1[-6:]) > 0:
         list_up.append(predict_next_number(levelsh_1[-6:]))
      if predict_next_number(levelsh_5[-6:]) > 0:
         list_up.append(predict_next_number(levelsh_5[-6:]))
      if predict_next_number(levelsh_15[-6:]) > 0:
         list_up.append(predict_next_number(levelsh_15[-6:]))

      # print(list_down)
      # print(list_up)

      if len(list_down)>2:
        data = {'list_down': list_down}
        df = pd.DataFrame(data)
        pair_step_1_price_line_down = "{:.3f}".format(df['list_down'].mean()) if abs(df['list_down'].mean()) >= 1 else "{:.8f}".format(df['list_down'].mean())
      elif len(list_down)== 0:
        pair_step_1_price_line_down = 0
      else:
        pair_step_1_price_line_down = "{:.3f}".format(list_down[0]) if abs(list_down[0]) >= 1 else "{:.8f}".format(list_down[0])


      if len(list_up)>1:
        data2 = {"list_up" : list_up}
        df2 = pd.DataFrame(data2)
        pair_step_1_price_line_up = "{:.3f}".format(df2['list_up'].mean()) if abs(df2['list_up'].mean()) >= 1 else "{:.8f}".format(df2['list_up'].mean())
      elif len(list_up)== 0:
        pair_step_1_price_line_up = 0
      else:
        pair_step_1_price_line_up = "{:.3f}".format(list_up[0]) if abs(list_up[0]) >= 1 else "{:.8f}".format(list_up[0])

      
      # print(pair_step_1_price_line_up)
      # print(pair_step_1_price_line_down)
      # print('----')
      # Обновляем таблицу, добавляя значения pair_step_1_price_line_up и pair_step_1_price_line_down для данного pair_step_1
      try:
          cursor2.execute('''
              UPDATE Trade_pair
              SET {line_up} = ?,
                  {line_down} = ?
              WHERE {pair_step} = ?
          '''.format(line_up = line_up, line_down=line_down, pair_step = pair_step), (pair_step_1_price_line_up, pair_step_1_price_line_down, pair_step_1[0]))
          # Если запрос выполнен успешно, фиксируем изменения
          conn.commit()  # Фиксация изменений
      except sqlite3.Error as e:
          # Если произошла ошибка, выводим ее описание
          print("Ошибка при выполнении запроса UPDATE:", e)





while True:
    logging.basicConfig(filename='l_pair.log', level=logging.ERROR, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    try:
        conn = sqlite3.connect('price_pair_trade.db')
        cursor2 = conn.cursor()

        add_pair_list('pair_step_1',cursor2, 'pair_step_1_price_line_up','pair_step_1_price_line_down')
        add_pair_list('pair_step_2',cursor2, 'pair_step_2_price_line_up','pair_step_2_price_line_down')
        add_pair_list('pair_step_3',cursor2, 'pair_step_3_price_line_up','pair_step_3_price_line_down')
        print('r')
        conn.close()
        time.sleep(15)
    except Exception as e:
        print(e)
        time.sleep(15)
        logging.exception("Ошибка:")










# df.set_index('Date', inplace=True)

# # Создаем точки для отображения на графике
# points = levelsL
# x_values = [point[0] for point in points]
# y_values = [point[1] for point in points]

# points2 = levelsh
# x_values2 = [point[0] for point in points2]
# y_values2 = [point[1] for point in points2]

# # Строим график цен закрытия
# plt.figure(figsize=(10, 6))
# plt.plot(df.index, df['Close'], label='Close Price', marker='o', linestyle='-')
# plt.scatter(x_values, y_values, color='r', label='Points',s=100)
# plt.scatter(x_values2, y_values2, color='g', label='Points',s=100)  # Отображаем точки на графике
# plt.title('Close Price Over Time')
# plt.xlabel('Time')
# plt.ylabel('Close Price')
# plt.xticks(rotation=45)
# plt.grid(True)
# plt.legend()
# plt.show()