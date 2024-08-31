import pandas as pd
import numpy as np
from pyswarm import pso
from sklearn.preprocessing import MinMaxScaler

# 读取Excel文件
df = pd.read_excel('data.xlsx')

# 提取数据列
resin_content = df['树脂含量'].values
curing_temperature = df['固化温度'].values
reduction_degree = df['减量程度'].values
fracture_strength = df['断裂强力'].values
fracture_elongation = df['断裂伸长量'].values
tear_strength = df['撕裂强力'].values

# 数据归一化
scaler = MinMaxScaler()
target_data = np.vstack([fracture_strength, fracture_elongation, tear_strength]).T
target_data_normalized = scaler.fit_transform(target_data)

# 反归一化
def denormalize(value, scaler):
    return scaler.inverse_transform(np.array([[value]]))[0, 0]

# 计算目标函数（最大化归一化后的断裂强力、断裂伸长量和撕裂强力的加权和）
def objective_function(x):
    resin, temp, reduction = x
    distances = np.abs(resin_content - resin) + np.abs(curing_temperature - temp) + np.abs(reduction_degree - reduction)
    idx = np.argmin(distances)

    # 获取归一化后的目标值
    normalized_targets = target_data_normalized[idx]

    # 目标是最大化这三个指标的加权和
    return -np.sum(normalized_targets)  # 使用负号因为pso最小化目标函数

# 边界条件
lb = [resin_content.min(), curing_temperature.min(), reduction_degree.min()]
ub = [resin_content.max(), curing_temperature.max(), reduction_degree.max()]

# 粒子群优化
xopt, fopt = pso(objective_function, lb, ub, swarmsize=50, maxiter=100)

# 输出结果
optimal_resin, optimal_temp, optimal_reduction = xopt
optimal_idx = np.argmin(np.abs(resin_content - optimal_resin) + np.abs(curing_temperature - optimal_temp) + np.abs(reduction_degree - optimal_reduction))

# 反归一化目标值
final_targets_normalized = target_data_normalized[optimal_idx]
final_targets = scaler.inverse_transform(final_targets_normalized.reshape(1, -1))

print(f"树脂含量: {optimal_resin}")
print(f"固化温度: {optimal_temp}")
print(f"减量程度: {optimal_reduction}")

print(f"断裂强力: {final_targets[0, 0]}")
print(f"断裂伸长量: {final_targets[0, 1]}")
print(f"撕裂强力: {final_targets[0, 2]}")
