import pandas as pd
import pymssql as psq
import psycopg2.extras
from email_validate import validate, validate_or_fail
import email_validate.exceptions as eex
import time
from progress.bar import IncrementalBar

# Соединяемся с базой стека
mes_conn = psq.connect(server='192.168.9.10', user='LUBCHANSKIY', password='789456', database='Magadan_stack', charset='utf8')

# Функция запроса е-маил физиков
def email_fizlic(s_conn):
    cursor = s_conn.cursor()
    sql_srting = "SELECT лс.Номер лицевой, св.Примечание email FROM stack.Свойства св join stack.[Лицевые счета] лс ON лс.ROW_ID = св.[Счет-Параметры] where [Виды-Параметры]=177"
    cursor.execute(sql_srting)
    row = cursor.fetchone()
    data = []
    while row:
        data.append([row[0], row[1].encode('windows-1251').decode()])
        row = cursor.fetchone()      
    return data

# Функция запроса е-маил юриков
def email_ulorg(s_conn):
    cursor = s_conn.cursor()
    cursor.execute("SELECT Название, орг.email FROM stack.[Организации] орг where email is not null and email != ''")
    row = cursor.fetchone()
    data = []
    while row:
        data.append([row[0].encode('ISO-8859-1').decode('windows-1251'), row[1]]) # Перекодируем строчку со странной кодировкой принятой с БД
        row = cursor.fetchone()      
    return data

# Запрашиваем таблички e-mail физиков и юриков
fiz_email_list = email_fizlic(mes_conn)
ul_email_list = email_ulorg(mes_conn)

# Функция проверки e-mail адресов
def valid_email(email):
    try:
        validate_or_fail(
            email_address=email,
            check_format=True,
            check_blacklist=False,
            check_dns=True,
            dns_timeout=10,
            check_smtp=True,
            smtp_debug=False
        )
    except eex.DomainNotFoundError:
        return 'Адрес домена не найден'
    except eex.NoNameserverError:
        return '' # Почему то ругается на многие нормальные адреса, поэтому отключил
    except eex.DNSTimeoutError:
        return 'Истекло время ожидания при запросе сервера имен.'
    except eex.DNSConfigurationError:
        return 'Сервер имен настроен неправильно.'
    except eex.NoMXError:
        return 'Сервер имен не содержит записей MX для домена.'
    except eex.NoValidMXError:
        return 'Сервер имен перечисляет записи MX для домена, но ни одна из них не является допустимой.'
    except eex.AddressFormatError:
        return 'Формат адреса не соответствует требованиям'
    except eex.DomainBlacklistedError:
        return 'Адрес домена в черном списке!'
    except eex.SMTPError:
        return 'Ошибка доставки по адресу, адрес не существует'
    else:
        return ''
    

# Проверяем физиков
email_errors = []
bar = IncrementalBar('Countdown', max = len(fiz_email_list))
for email_ls in fiz_email_list:
    res = valid_email(email_ls[1])
    if res != '':
        email_errors.append([email_ls[0], email_ls[1], res])
    bar.next()
bar.finish()
email_df = pd.DataFrame(email_errors)


# Проверяем юриков
ul_email_errors = []
bar = IncrementalBar('Countdown', max = len(ul_email_list))
for email_ls in ul_email_list:
    if ';' in email_ls[1]:
        spl_res = email_ls[1].split(';')
        for eml in spl_res:
            res = valid_email(eml)
            if res != '':
                ul_email_errors.append([email_ls[0], eml, res])
    elif  ',' in email_ls[1]:
        spl_res = email_ls[1].split(',')
        for eml in spl_res:
            res = valid_email(eml)
            if res != '':
                ul_email_errors.append([email_ls[0], eml, res])
    else:
        res = valid_email(email_ls[1])
        if res != '':
            ul_email_errors.append([email_ls[0], email_ls[1], res])
    bar.next()
bar.finish()            
ulemail_df = pd.DataFrame(ul_email_errors)

# Запихиваем все в Excel
sh_name_fl = 'Ошибки физиков'
sh_name_ul = 'Ошибки юриков'
writer = pd.ExcelWriter('email_error.xlsx', engine='xlsxwriter')

email_df.to_excel(writer, sheet_name=sh_name_fl, index=False)
ulemail_df.to_excel(writer, sheet_name=sh_name_ul, index=False)

writer.save()
writer.close()

