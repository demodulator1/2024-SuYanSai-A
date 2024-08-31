import numpy as np

#系数和截距
intercept = 10622.53453
coefficients = {
    '树脂含量': -233.822679,
    '固化温度': -88.785737,
    '减量程度': 20.464182,
    '树脂含量^2': 2.374558,
    '树脂含量 固化温度': 0.354642,
    '树脂含量 减量程度': 1.728879,
    '固化温度^2': 0.386926,
    '固化温度 减量程度': -0.477996,
    '减量程度^2': 0.063604
}

# 更新后的回归方程
def regression_function(x1, x2, x3):
    return (intercept +
            coefficients['树脂含量'] * x1 +
            coefficients['固化温度'] * x2 +
            coefficients['减量程度'] * x3 +
            coefficients['树脂含量^2'] * x1**2 +
            coefficients['树脂含量 固化温度'] * x1 * x2 +
            coefficients['树脂含量 减量程度'] * x1 * x3 +
            coefficients['固化温度^2'] * x2**2 +
            coefficients['固化温度 减量程度'] * x2 * x3 +
            coefficients['减量程度^2'] * x3**2)

# 定义搜索范围
x1_range = np.linspace(15, 30, 150)  # 树脂含量范围，取150个值
x2_range = np.linspace(100, 130, 300) # 固化温度范围，取300个值
x3_range = np.linspace(0, 30, 300)    # 减量程度范围，取300个值

# 初始化最大值和对应的参数
max_strength = -np.inf
best_params = (None, None, None)

# 遍历所有可能的参数组合
for x1 in x1_range:
    for x2 in x2_range:
        for x3 in x3_range:
            strength = regression_function(x1, x2, x3)
            if strength > max_strength:
                max_strength = strength
                best_params = (x1, x2, x3)

print(f'Optimal Parameters:')
print(f'树脂含量 = {best_params[0]}')
print(f'固化温度 = {best_params[1]}')
print(f'减量程度 = {best_params[2]}')
print(f'透湿率 = {max_strength}')
