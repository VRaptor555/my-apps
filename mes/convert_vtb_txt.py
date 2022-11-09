import pandas as pd
import os

# Каталог с файликами, относительно данного файла
catalog = 'mes/vtb/'

def period_pay(values): # Если период формы 622.00, возвращаем '0622'. Если 1022.00 - возращаем '1022'
    if len(values)>5:
        return values[:4]
    else:
        return '0'+values[:3]

def vtb_convert_to_xlsx(vtb_catalog, vtb_file):
    vtb_data = pd.read_table(vtb_catalog+vtb_file+'.txt', sep=';', header=None)

    # Ищем строчку итога, кидаем в другой DS
    vtb_itog = vtb_data[vtb_data[0].str.contains('=')]
    vtb_itog2 = vtb_itog.drop([7,8,9,10,11], axis=1)
    vtb_itog = vtb_itog.drop([6,7,8,9,10,11], axis=1)
    vtb_itog.columns = ['Количество', 'Сумма операции', 'Сумма перевода', 'Сумма комиссии', '№п/п', 'Дата'] # Обзываем колонки
    vtb_itog['Количество'] = vtb_itog['Количество'].apply(lambda s: s[1:3])

    # Оставляем в основном DS все кроме итога
    vtb_data = vtb_data[~vtb_data[0].str.contains('=')]
    vtb_data = vtb_data.drop([1, 2, 3, 4], axis=1)
    vtb_data.columns = ['Дата платежа', 'ЛС', 'ФИО', 'Адрес', 'Период оплаты', 'Сумма операции', 'Сумма перевода', 'Сумма комиссии'] # обзываем колонки
    vtb_data['Период оплаты'] = vtb_data['Период оплаты'].astype('str') # Корректируем период оплаты
    vtb_data['Период оплаты'] = vtb_data['Период оплаты'].apply(period_pay)
    vtb_data['Дата платежа'] = pd.to_datetime(vtb_data['Дата платежа'], dayfirst=True) # Дату платежа в формат datetime
    vtb_data = vtb_data.sort_values('ЛС') # Сортируем по ЛС

    # Подсчитываем суммы для сверки с итоговой строкой
    sum_oper = round(vtb_data['Сумма операции'].sum(), 2)
    sum_pere = round(vtb_data['Сумма перевода'].sum(), 2)
    sum_komi = round(vtb_data['Сумма комиссии'].sum(), 2)

    if float(vtb_itog['Сумма операции'].astype('float')) == sum_oper and float(vtb_itog['Сумма перевода'].astype('float')) == sum_pere and \
            float(vtb_itog['Сумма комиссии'].astype('float')) == sum_komi and int(vtb_itog['Количество'].astype('float')) == len(vtb_data):
            print('Все в порядке')
    else:
        print(f"Сумма операции {vtb_itog['Сумма операции'].astype('float').sum()} | Сумма таблицы опер {sum_oper}")
        print(f"Сумма операции {vtb_itog['Сумма перевода'].astype('float').sum()} | Сумма таблицы перев {sum_pere}")
        print(f"Сумма операции {vtb_itog['Сумма комиссии'].astype('float').sum()} | Сумма таблицы комисс {sum_komi}")
        print(f"Сумма операции {vtb_itog['Количество'].astype('float').sum()} | Количество таблицы {len(vtb_data)}")
        return 1

    # Добавляем колонки в соответствии с форматом стека
    # NAME - Наименование, SOURCE - Номер колонки
    # NAME="Дата" SOURCE="4"/>3
    # NAME="Лицевой" SOURCE="10"/>9
    # NAME="Сумма" SOURCE="12"/>11
    # NAME="ФИО" SOURCE="13"/>12
    # NAME="Адрес" SOURCE="16"/>15
    # NAME="Показание" SOURCE="19"/>18
    vtb_data.insert(2, 'Сумма', vtb_data['Сумма операции']) # Сумму вставляем между ЛС и ФИО
    vtb_data = vtb_data.drop(['Период оплаты', 'Сумма операции', 'Сумма перевода','Сумма комиссии'], axis=1) # Удаляем лишнее
    vtb_data.insert(5, "Кол6", " ")
    """
    vtb_data.insert(0, "Кол1", " ")
    vtb_data.insert(1, "Кол2", " ")
    vtb_data.insert(2, "Кол3", " ")
    # 3 Здесь будет Дата
    vtb_data.insert(4, "Кол5", " ")
    
    vtb_data.insert(6, "Кол7", " ")
    vtb_data.insert(7, "Кол8", " ")
    vtb_data.insert(8, "Кол9", " ")
    # 9 Здесь будет Лицевой
    vtb_data.insert(10, "Кол11", " ")
    # 11 Здесь будет Сумма
    # 12 Здесь будет ФИО
    vtb_data.insert(13, "Кол14", " ")
    vtb_data.insert(14, "Кол15", " ")
    # 15 Здесь будет Адрес
    vtb_data['Кол16'] = " "
    vtb_data['Кол17'] = " "
    vtb_data['Показание'] = " "
    #vtb_data['Кол19'] = ""
    """

    vtb_file = str.replace(vtb_file, "VTB", "VTB24")
    vtb_data.to_csv(vtb_catalog+'out/'+vtb_file+'.txt', sep=';', header=False, index=False, decimal='.', date_format='%d-%m-%Y', encoding='cp1251')
    #vtb_itog2[1] = pd.to_numeric(vtb_itog2[1])
    #vtb_itog2.to_csv(vtb_catalog+'out/'+vtb_file+'.txt', sep=';', header=False, index=False, decimal=',', date_format='%d-%m-%Y', mode='a', encoding='cp1251')
    return 0

# Определяем список файлов в папке
files = os.listdir(catalog)
reestry = list(filter(lambda x: x.endswith('.txt'), files))
for txt_file in reestry:
    vtb_file, vtb_ext = os.path.splitext(txt_file)
    if vtb_convert_to_xlsx(catalog, vtb_file) != 0:
        print('Ошибка при конвертации')
    else:
        print('Конвертация прошла успешно!')