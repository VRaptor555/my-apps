"""
            Параметры загрузки файла с помощью pd.read_csv()

    header = None — загрузить без строки с заголовком;
    skiprows=n — пропустить n строк (часто у документов бывает техническая «шапка»);
    encoding — загрузить в конкретной кодировке;
    na_values — список значений, который нужно заменить на NaN (специальный объект, обозначающий пропущенное значение).
"""

import pandas as pd

# Загружаем данные log
log = pd.read_csv("./bukmecker/data/log.csv", header = None)

# Меняем название столбцов
log.columns = ['user_id','time','bet','win']

# Убираем ошибки в user_id
log = log[~log.user_id.str.contains("error", na=False)]

def get_user_id(s): # Функция достает ID пользователя вида "user_N" где N — значение идентификатора.
    pos = s.find("user")
    if pos > -1:
        return s[pos:]
    else:
        return ""

# Оставим в поле user_id значение типа "user_N"
log['user_id'] = log.user_id.apply(get_user_id)

# Уберем начальную скобку из поля time.
log['time'] = log[log.time.str.match("\[", na=False)]['time'].apply(lambda t: str(t).replace('[', ''))

# преобразуем колонку 'time' в формат datetime
log['time'] = pd.to_datetime(log['time'])
#users = pd.read_csv("data/users.csv", encoding="KOI8-R", sep="	")
#users.columns = ['user_id','email','geo']
