import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

# 读取数据
df = pd.read_excel("data.xlsx")

# 特征和目标变量
X = df[['树脂含量', '固化温度', '减量程度']]
y = df['断裂强力']

# 生成二次项特征
poly = PolynomialFeatures(degree=1, include_bias=False)
X_poly = poly.fit_transform(X)

# 建立模型并训练
model = LinearRegression()
model.fit(X_poly, y)

# 预测和计算R-squared
y_pred = model.predict(X_poly)
r_squared = r2_score(y, y_pred)

# 打印回归方程
feature_names = poly.get_feature_names_out()
coef_dict = dict(zip(feature_names, model.coef_))
print("回归方程的系数:", coef_dict)
print("回归方程的截距:", model.intercept_)
print("R-squared:", r_squared)




