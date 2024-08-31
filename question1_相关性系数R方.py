import pandas as pd
import numpy as np

df = pd.read_excel('scaled_data.xlsx')

# Python中列索引从0开始，所以第2列是索引1，第3列是索引2，第4列是索引3，以此类推
cols_x = df.iloc[:, 1:4]  # 第2-4列
cols_y = df.iloc[:, 4:11]  # 第5-11列

# 计算相关性系数（R方值）
r_squared = pd.DataFrame(index=cols_x.columns, columns=cols_y.columns)

for x_col in cols_x.columns:
    for y_col in cols_y.columns:
        # 计算相关性系数
        correlation_matrix = np.corrcoef(cols_x[x_col], cols_y[y_col])
        correlation = correlation_matrix[0, 1]
        # 计算R方值
        r_squared.loc[x_col, y_col] = correlation ** 2

print(r_squared)
