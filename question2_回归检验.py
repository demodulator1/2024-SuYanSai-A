import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score
from sklearn.model_selection import KFold, cross_val_score
import matplotlib.pyplot as plt

# 读取数据
df = pd.read_excel("data.xlsx")

# 特征和目标变量
X = df[['树脂含量', '固化温度', '减量程度']]
y = df['折皱回复率']

# 生成二次项特征
poly = PolynomialFeatures(degree=3, include_bias=False)
X_poly = poly.fit_transform(X)

# 建立模型
model = LinearRegression()

# K折交叉验证
kf = KFold(n_splits=5, shuffle=True, random_state=42)  # 这里选择5折交叉验证，你可以根据需要调整
cross_val_scores = cross_val_score(model, X_poly, y, cv=kf, scoring='r2')

# 输出交叉验证结果
print("交叉验证R-squared的平均值:", cross_val_scores.mean())

# 训练整个模型以输出回归方程
model.fit(X_poly, y)
y_pred = model.predict(X_poly)
r_squared = r2_score(y, y_pred)

# 打印回归方程
feature_names = poly.get_feature_names_out()
coef_dict = {name: round(coef, 6) for name, coef in zip(feature_names, model.coef_)}
intercept = round(model.intercept_, 6)

print("回归方程的系数:", coef_dict)
print("回归方程的截距:", intercept)
print("训练集上的R-squared:", r_squared)
