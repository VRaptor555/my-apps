import pandas as pd

log = pd.read_csv("data/log.csv", header = None)
users = pd.read_csv("data/users.csv", encoding="KOI8-R", sep="	")

log.columns = ['user_id','time','bet','win']
users.columns = ['user_id','email','geo']

# Приведём признак user_id к одному формату в обоих датасетах
users.user_id = users.user_id.apply(lambda x: x.lower())

# Избавимся от ошибок в user_id
log = log[log.user_id != "#error"]
log.user_id = log.user_id.str.split(" - ").apply(lambda x: x[1])

log_users = pd.merge(log, users, on='user_id')

sample2 = log_users.groupby('geo').user_id.count()