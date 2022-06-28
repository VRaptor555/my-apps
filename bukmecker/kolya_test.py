import pandas as pd
log = pd.read_csv("log.csv", header = None)
log.columns = ['user_id','time','bet','win']
log = log.dropna(axis = 0)    
log['time'] = log.time.str.replace('[', '')
log['time'] = pd.to_datetime(log['time'])
log['hour'] =  log.time.dt.hour