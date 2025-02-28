import sqlite3

# Устанавливаем соединение с базой данных
conn = sqlite3.connect('min_5_base.db')
cursor = conn.cursor()

table_name = 'BTC_USDT_5'  # Замените на фактическое название вашей таблицы

# Получаем все строки из таблицы
cursor.execute(f'SELECT * FROM {table_name}')
rows = cursor.fetchall()
list_pol = []
list_otr = []
list_end = []
# Проходим по строкам в обратном порядке (начиная с последней добавленной записи)
for row in reversed(rows):
    if float(row[2]) > 0:
        list_otr = []
        list_pol.append(row)
        if len(list_pol) > 2:
            
            sum = 0
            max = 0
            date = None
            for l in list_pol:
                if float(l[0]) > max:
                    max = float(l[0])
                    date = l[1]
                sum = sum + float(l[2])
            list_end.append([max,date,round(sum,2)])
            list_pol=[]
                   
    elif float(row[2]) < 0: 
          
        list_pol = []
        list_otr.append(row)
        if len(list_otr) > 2:
            sum = 0
            min = 100000
            date2 = 0
            for l in list_otr:
                if float(l[0]) < min:
                    min = float(l[0])
                    date2 = l[1]
                sum = sum + float(l[2])
            list_end.append([min,date,round(sum,2)])
            list_otr = []
for e in list_end:   
    print(e)    