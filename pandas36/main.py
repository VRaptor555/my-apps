import pandas as pd

def delete_columns(df, col=[]):
    """
    Напишите функцию delete_columns(df, col=[]), которая удаляет столбцы из DataFrame и возвращает новую таблицу. 
    Если одного из указанных столбцов в таблице не существует, то функция должна возвращать None.
    """
    try:
        df.drop(col, axis=1, inplace=True)
    except:
        return None
    return df


if __name__ == '__main__':
    customer_df = pd.DataFrame({
        'number': [0, 1, 2, 3, 4],
        'cust_id': [128, 1201, 9832, 4392, 7472],
        'cust_age': [13, 21, 19, 21, 60],
        'cust_sale': [0, 0, 0.2, 0.15, 0.3],
        'cust_year_birth': [2008, 2000, 2002, 2000, 1961],
        'cust_order': [1400, 14142, 900, 1240, 8430]
    })
    columns_for_delete= ['number', 'cust_year_birth'] #выбранные вами столбцы
    new_df = delete_columns(customer_df, columns_for_delete)
    print(new_df)
