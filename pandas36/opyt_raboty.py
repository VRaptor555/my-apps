import pandas as pd

def get_experience(arg):
    """
    Напишите функцию get_experience(arg), аргументом которой является строка столбца с опытом работы. 
    Функция должна возвращать опыт работы в месяцах. Не забудьте привести результат к целому числу.
    """
    month_result = 0
    year_list = ['лет', 'год', 'года']
    month_list = ['месяц', 'месяца', 'месяцев']
    pred_s = ''
    arg_split = arg.split(' ')
    for month_year in arg_split:
        if (month_year == 'Опыт') or (month_year == 'работы'):
            continue
        if month_year in year_list:
            month_result += int(pred_s) * 12
        elif month_year in month_list:
            month_result += int(pred_s)
        pred_s = month_year
    return month_result
        

if __name__ == '__main__':
    experience_col = pd.Series([
        'Опыт работы 8 лет 3 месяца',
        'Опыт работы 3 года 5 месяцев',
        'Опыт работы 1 год 9 месяцев',
        'Опыт работы 3 месяца',
        'Опыт работы 6 лет'
        ])
    experience_month = experience_col.apply(get_experience)
    print(experience_month)