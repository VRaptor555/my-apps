import pandas as pd
log = pd.read_csv("./bukmecker/data/log.csv", header = None)
log.columns = ['user_id','time','bet','win']
log = log[~log.user_id.str.contains("error", na=False)]
log['user_id'] = log.user_id.str.replace('Запись пользователя № - ', '')
log['time'] = log.time.str.replace('[', '')
log.dropna(axis=0, subset=['user_id', 'time'])
log['time'] = pd.to_datetime(log['time'])
log['hour'] = log.time.dt.hour