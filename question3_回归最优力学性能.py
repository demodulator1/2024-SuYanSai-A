import numpy as np

# 定义回归方程
def fracture_strength(resin_content, curing_temp, reduction_degree):
    return 1840.838757 + (24.828373 * resin_content) + (-7.187842 * curing_temp) + (-79.999763 * reduction_degree) \
        + (0.283718 * resin_content ** 2) + (-0.336917 * resin_content * curing_temp) + (
                    0.360148 * resin_content * reduction_degree) \
        + (0.06519 * curing_temp ** 2) + (0.116717 * curing_temp * reduction_degree) + (
                    1.410783 * reduction_degree ** 2)

def elongation(resin_content, curing_temp, reduction_degree):
    return 0.117955 + (0.042182 * resin_content) + (0.008205 * curing_temp) + (-0.029932 * reduction_degree) \
        + (-0.0003 * resin_content ** 2) + (-0.000305 * resin_content * curing_temp) + (
                    0.000273 * resin_content * reduction_degree) \
        + (0.0 * curing_temp ** 2) + (2.5e-05 * curing_temp * reduction_degree) + (0.00055 * reduction_degree ** 2)

def tear_strength(resin_content, curing_temp, reduction_degree):
    return 240.830123 + (-3.392196 * resin_content) + (-0.00856 * curing_temp) + (-15.491499 * reduction_degree) \
        + (0.068722 * resin_content ** 2) + (-0.00807 * resin_content * curing_temp) + (
                    0.110209 * resin_content * reduction_degree) \
        + (-0.001647 * curing_temp ** 2) + (0.067183 * curing_temp * reduction_degree) + (
                    0.110893 * reduction_degree ** 2)

# 目标函数
def objective(x):
    resin_content, curing_temp, reduction_degree = x
    fracture = fracture_strength(resin_content, curing_temp, reduction_degree)
    elongation_val = elongation(resin_content, curing_temp, reduction_degree)
    tear = tear_strength(resin_content, curing_temp, reduction_degree)

    # 归一化到 [0, 1] 范围
    fracture_normalized = (fracture - 1840) / (2000 - 1840)
    elongation_normalized = (elongation_val - 0) / (0.2 - 0)
    tear_normalized = (tear - 240) / (300 - 240)

    # 返回所有指标的负平均值，目标是最大化这些值
    return - (fracture_normalized + elongation_normalized + tear_normalized) / 3

# 遍历范围的网格搜索
def grid_search(bounds, step_size=1.0):
    resin_range = np.arange(bounds[0][0], bounds[0][1] + step_size, step_size)
    temp_range = np.arange(bounds[1][0], bounds[1][1] + step_size, step_size)
    reduction_range = np.arange(bounds[2][0], bounds[2][1] + step_size, step_size)

    best_score = float('inf')
    best_params = None

    for resin_content in resin_range:
        for curing_temp in temp_range:
            for reduction_degree in reduction_range:
                score = objective([resin_content, curing_temp, reduction_degree])
                if score < best_score:
                    best_score = score
                    best_params = (resin_content, curing_temp, reduction_degree)

    return best_params, -best_score

# 变量范围
bounds = [(15, 30), (100, 130), (0, 30)]

# 执行网格搜索
best_params, best_score = grid_search(bounds, step_size=0.5)

# 输出结果
print(f"树脂含量: {best_params[0]}")
print(f"固化温度: {best_params[1]}")
print(f"减量程度: {best_params[2]}")

# 计算优化后的目标值
print(f"断裂强力: {fracture_strength(*best_params)}")
print(f"断裂伸长量: {elongation(*best_params)}")
print(f"撕裂强力: {tear_strength(*best_params)}")
