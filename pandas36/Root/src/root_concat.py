from numpy import NaN
import pandas as pd
import os

def concat_users_files(path):
    """
    Вам необходимо написать функцию concat_user_files(path), параметром которой является path - путь до директории. 
    Функция должна объединить информацию из предоставленных вам файлов в один DataFrame и вернуть его. 
    Не забудьте обновить индексы результирующей таблицы после объединения.
    Учтите тот момент, что в результате объединения могут возникнуть дубликаты, от которых необходимо будет избавиться. 
    """
    file_list = os.listdir(path)
    file_list.sort()
    for ind, filename in enumerate(file_list):
        filepath = path + filename
        if ind == 0:
            result_df = pd.read_csv(filepath, sep=',')
        else:
            second_df = pd.read_csv(filepath, sep=',')
            result_df = pd.concat([result_df, second_df], ignore_index=True)
    result_df = result_df.drop_duplicates(ignore_index=True)
    return result_df


if __name__ == '__main__':
    data = concat_users_files('./pandas36/Root/users/')
    print(data)