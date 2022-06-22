import pandas as pd

items_df = pd.DataFrame({
'item_id': [417283, 849734, 132223, 573943, 19475, 3294095, 382043, 302948, 100132, 312394], 
'vendor': ['Samsung', 'LG', 'Apple', 'Apple', 'LG', 'Apple', 'Samsung', 'Samsung', 'LG', 'ZTE'],
'stock_count': [54, 33, 122, 18, 102, 43, 77, 143, 60, 19]
})

purchase_df = pd.DataFrame({
    'purchase_id': [101, 101, 101, 112, 121, 145, 145, 145, 145, 221],
    'item_id': [417283, 849734, 132223, 573943, 19475, 3294095, 382043, 302948, 103845, 100132], 
    'price': [13900, 5330, 38200, 49990, 9890, 33000, 67500, 34500, 89900, 11400]
})
"""
Сформируйте DataFrame merged, в котором в результате объединения
purchase_df и items_df останутся модели, которые учтены на складе и имели продажи. 
"""
merged = items_df.merge(purchase_df, on='item_id')
"""
Найдите из таблицы merged суммарную выручку, которую можно было бы получить 
от продажи всех товаров, которые есть на складе. 
Результат занесите в переменную income.
"""
merged['total'] = merged['price'] * merged['stock_count']
income = merged['total'].sum()