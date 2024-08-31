import pandas as pd
import numpy as np

df=pd.read_excel('data.xlsx')

# 获取除第一列外的数据
data_to_scale = df.iloc[:, 1:]

# 计算最小值和最大值
min_vals = data_to_scale.min()
max_vals = data_to_scale.max()

# 进行标准化处理
scaled_data = (data_to_scale - min_vals) / (max_vals - min_vals)

# 将标准化的数据替换原数据
df.iloc[:, 1:] = scaled_data

# 保存结果到新Excel文件
df.to_excel('scaled_data.xlsx', index=False, engine='openpyxl')
