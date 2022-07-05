import pandas as pd
import zipfile as zip
import os

catalog = 'data/'
# Загружаем реестры (или один реестр)

def read_write_csv (files):
    pays = []
    ierror = 0
    for ind, fil in enumerate(files):
        pays.append(pd.read_csv('data/' + fil, header=None, sep=';', encoding='Windows-1251'))
        if len(pays[ind].columns) < 13:
            ierror = -1
        pays[ind] = pays[ind].drop(8, axis=1)
        pays[ind].to_csv('data/' + fil, header=None, sep=';', encoding='Windows-1251', index=False)
    return ierror

files = os.listdir(catalog)
reestry = list(filter(lambda x: x.endswith('.txt'), files))

ires = read_write_csv(reestry)
if ires == 0:
    print('Удаление столбца прошло без ошибок!')
else:
    print('При удалении столбца произошла ошибка, возможно столбец уже удален!')