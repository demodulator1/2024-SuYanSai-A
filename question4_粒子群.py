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
breaking_strength = df['断裂强力'].values
breaking_extension = df['断裂伸长量'].values
tear_strength = df['撕裂强力'].values
air_permeability = df['透气率'].values
moisture_permeability = df['透湿率'].values
softness = df['柔软度'].values
wrinkle_recovery_rate = df['折皱回复率'].values

# 数据归一化
scaler = MinMaxScaler()
target_data = np.vstack([
    breaking_strength, breaking_extension, tear_strength, air_permeability,
    moisture_permeability, softness, wrinkle_recovery_rate
]).T
target_data_normalized = scaler.fit_transform(target_data)

# 反归一化
def denormalize(value, scaler):
    return scaler.inverse_transform(np.array([[value]]))[0, 0]

# 计算目标函数（最大化归一化后的指标的加权和）
def objective_function(x):
    resin, temp, reduction = x
    distances = np.abs(resin_content - resin) + np.abs(curing_temperature - temp) + np.abs(reduction_degree - reduction)
    idx = np.argmin(distances)

    # 获取归一化后的目标值
    normalized_targets = target_data_normalized[idx]

    # 设定透气率和透湿率的权重
    weight_air_permeability = 2.0
    weight_moisture_permeability = 2.0

    # 计算目标值的加权和
    weighted_sum = (normalized_targets[0] +
                    normalized_targets[1] +
                    normalized_targets[2] +
                    weight_air_permeability * normalized_targets[3] +
                    weight_moisture_permeability * normalized_targets[4] +
                    normalized_targets[5] +
                    normalized_targets[6])

    return -weighted_sum  # 使用负号因为pso最小化目标函数

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
print(f"透气率: {final_targets[0, 3]}")
print(f"透湿率: {final_targets[0, 4]}")
print(f"柔软度: {final_targets[0, 5]}")
print(f"折皱回复率: {final_targets[0, 6]}")
