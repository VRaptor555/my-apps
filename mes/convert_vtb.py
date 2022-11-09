import pandas as pd
import os

# Каталог с файликами, относительно данного файла
catalog = 'vtb/'

def period_pay(values): # Если период формы 622.00, возвращаем '0622'. Если 1022.00 - возращаем '1022'
    if len(values)>5:
        return values[:4]
    else:
        return '0'+values[:3]

def vtb_convert_to_xlsx(vtb_catalog, vtb_file):
    vtb_data = pd.read_table(vtb_catalog+vtb_file+'.txt', sep=';', header=None)

    # Ищем строчку итога, кидаем в другой DS
    vtb_itog = vtb_data[vtb_data[0].str.contains('=')]
    vtb_itog = vtb_itog.drop([6,7,8,9,10,11], axis=1)
    vtb_itog.columns = ['Количество', 'Сумма операции', 'Сумма перевода', 'Сумма комиссии', '№п/п', 'Дата'] # Обзываем колонки
    vtb_itog['Количество'] = vtb_itog['Количество'].apply(lambda s: s[1:4])

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
        return 1

    # Запихиваем все в Excel
    sh_name = 'Реестр'
    writer = pd.ExcelWriter(vtb_catalog+vtb_file+'.xlsx', engine='xlsxwriter', datetime_format='dd.mm.yyyy')
    vtb_data.to_excel(writer, sheet_name=sh_name, index=False)

    workbook = writer.book
    worksheet = writer.sheets[sh_name]
    money_format = workbook.add_format({'num_format': '# ##0.00'})
    date_format = workbook.add_format({'num_format': 'dd.mm.yyyy'})
    sum_format = workbook.add_format({'bold': True})

    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'top',
        'align': 'center',
        'fg_color': '#D7E4BC',
        'border': 1})
    for col_num, value in enumerate(vtb_data.columns.values):
        worksheet.write(0, col_num, value, header_format)
    (max_row, max_col) = vtb_data.shape

    header_columns = []
    for col_name in vtb_data.columns:
        head_dict = dict(header=col_name)
        header_columns.append(head_dict)
    
    worksheet.set_column(0, 0, 12, date_format)
    worksheet.set_column(5, 7, 15, money_format)
    worksheet.set_column(2, 3, 50)

    worksheet.write(max_row+1, 5, '=SUM(F2:F{})'.format(max_row+1), sum_format)
    worksheet.write(max_row+1, 6, '=SUM(G2:G{})'.format(max_row+1), sum_format)
    worksheet.write(max_row+1, 7, '=SUM(H2:H{})'.format(max_row+1), sum_format)
    
    worksheet.add_table(0, 0, max_row, max_col-1, {'columns': header_columns})

    writer.save()
    writer.close()
    return 0

# Определяем список файлов в папке
files = os.listdir(catalog)
reestry = list(filter(lambda x: x.endswith('.txt'), files))
for txt_file in reestry:
    vtb_file, vtb_ext = os.path.splitext(txt_file)
    if vtb_convert_to_xlsx(catalog, vtb_file) != 0:
        print('Ошибка при конвертации')
        break
print('Конвертация прошла успешно!')