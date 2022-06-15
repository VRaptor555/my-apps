import pandas as pd
data = pd.DataFrame([[0,1], [1, 0], [1, 1]], columns=['А', 'B'])
print(data.shape)
list_panda = pd.Series([1, 2, 4, 2, 3, 2, 1, 5, 6])
print(list_panda.mode())