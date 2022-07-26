import pandas as pd
import zipfile as zip
import os

catalog = 'data/'
# Загружаем реестры (или один реестр)

def read_write_csv (t_dir, t_file):
    pays = pd.read_csv(t_dir + t_file, header=None, sep=';', encoding='Windows-1251')
    if len(pays.columns) < 13:
        return -1
    pays = pays.drop(8, axis=1)
    pays.to_csv(t_dir + t_file, header=None, sep=';', encoding='Windows-1251', index=False)
    return 'Удаление столбца прошло без ошибок!'

def read_write_zip(z_dir, z_file):
    zipFile = zip.ZipFile(z_dir + z_file, 'r')
    if not (os.path.isdir(z_dir+'out/')):
        os.mkdir(z_dir+'out/')    
    zipFile_out = zip.ZipFile(z_dir+'out/'+z_file, 'w', compresslevel=-3)
    list_file = zipFile.namelist()
    for txt_file in list_file:
        zipFile.extract(txt_file)
        if read_write_csv('', txt_file) == -1:
            print('При удалении столбца произошла ошибка, возможно столбец уже удален!')
            zipFile.close()
            zipFile_out.close()
            return -1
        zipFile_out.write(txt_file)
        os.remove(txt_file)
    zipFile.close()
    zipFile_out.close()
    return 0

files = os.listdir(catalog)
zip_reestr = list(filter(lambda x: x.endswith('.zip'), files))
#reestry = list(filter(lambda x: x.endswith('.txt'), files))

if len(zip_reestr) > 0:
    for zipf in zip_reestr:
        print(read_write_zip(catalog, zipf))

#if len(reestry) > 0:
#    for txt_f in reestry:
#        print(read_write_csv(catalog, reestry))
