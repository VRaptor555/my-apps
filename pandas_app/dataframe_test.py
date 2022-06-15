import pandas as pd

def create_companyDF(income, expenses, years):
    """
    Создайте функцию create_companyDF(income, expenses, years), которая  возвращает DataFrame, 
    составленный из входных данных со столбцами “Income” и “Expenses” и индексами, соответствующим годам рассматриваемого периода.
    """
9707

def get_profit(df, year):
    
    """
    А также напишите функцию get_profit(df, year), которая возвращает разницу между доходом и расходом, записанных в таблице df, за год year.
    Учтите, что если информация за запрашиваемый год не указана в вашей таблице вам необходимо вернуть None. 
    """
    if year in df.index:
        ser = df.loc[year, ['Income', 'Expenses']]
        profit = ser[0] - ser[1]
        return profit
    else:
        return None

if __name__ == '__main__':
    expenses = [156, 130, 270]
    income = [478, 512, 196]
    years = [2018, 2019, 2020]
    
    scienceyou = create_companyDF(income, expenses, years)
    print(get_profit(scienceyou, 2020)) #-74
