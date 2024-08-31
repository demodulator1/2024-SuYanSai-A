import numpy as np

# 断裂强力回归方程
def fracture_strength(resin_content, curing_temp, reduction_degree):
    return 1840.003261 + (0.269734 * resin_content) + (-2.442865 * curing_temp) + (-6.512045 * reduction_degree) \
        + (-0.002773 * resin_content ** 2) + (0.002722 * resin_content * curing_temp) + (
                    -0.020057 * resin_content * reduction_degree) \
        + (0.049659 * curing_temp ** 2) + (0.034738 * curing_temp * reduction_degree) + (
                    0.015217 * reduction_degree ** 2)

# 断裂伸长量回归方程
def elongation(resin_content, curing_temp, reduction_degree):
    return 0.074934 + (-0.000312 * resin_content) + (0.000065 * curing_temp) + (0.000410 * reduction_degree) \
        + (0.000000 * resin_content ** 2) + (-0.000000 * resin_content * curing_temp) + (
                    -0.000000 * resin_content * reduction_degree) \
        + (0.000000 * curing_temp ** 2) + (0.000000 * curing_temp * reduction_degree) + (
                    0.000000 * reduction_degree ** 2)

# 撕裂强力回归方程
def tear_strength(resin_content, curing_temp, reduction_degree):
    return 240.809183 + (-3.401894 * resin_content) + (0.551013 * curing_temp) + (-3.170159 * reduction_degree) \
        + (-0.022140 * resin_content ** 2) + (-0.020169 * resin_content * curing_temp) + (
                    0.073350 * resin_content * reduction_degree) \
        + (-0.008494 * curing_temp ** 2) + (0.014356 * curing_temp * reduction_degree) + (
                    -0.008118 * reduction_degree ** 2)

# 透气率回归方程
def air_permeability(resin_content, curing_temp, reduction_degree):
    return 654.596534 + (0.042795 * resin_content) + (-4.425432 * curing_temp) + (-20.034932 * reduction_degree) \
        + (-0.370575 * resin_content ** 2) + (0.227257 * resin_content * curing_temp) + (
                    -0.135007 * resin_content * reduction_degree) \
        + (-0.026606 * curing_temp ** 2) + (0.281106 * curing_temp * reduction_degree) + (
                    -0.393256 * reduction_degree ** 2)

# 透湿率回归方程
def moisture_permeability(resin_content, curing_temp, reduction_degree):
    return 10622.534531 + (-233.822679 * resin_content) + (-88.785737 * curing_temp) + (20.464182 * reduction_degree) \
        + (2.374558 * resin_content ** 2) + (0.354642 * resin_content * curing_temp) + (
                    1.728879 * resin_content * reduction_degree) \
        + (0.386926 * curing_temp ** 2) + (-0.477996 * curing_temp * reduction_degree) + (
                    0.063604 * reduction_degree ** 2)

# 柔软度回归方程
def softness(resin_content, curing_temp, reduction_degree):
    return 1.49625 + (-0.04875 * resin_content) + (0.005625 * curing_temp) + (0.067875 * reduction_degree)

# 折皱回复率回归方程
def wrinkle_recovery(resin_content, curing_temp, reduction_degree):
    return 88.232665 + (2.362457 * resin_content) + (0.567772 * curing_temp) + (0.653567 * reduction_degree) \
        + (-0.038973 * resin_content ** 2) + (-0.005583 * resin_content * curing_temp) + (
                    0.004328 * resin_content * reduction_degree) \
        + (-0.001423 * curing_temp ** 2) + (0.000496 * curing_temp * reduction_degree) + (
                    -0.013223 * reduction_degree ** 2)

# 目标函数
def objective(x):
    resin_content, curing_temp, reduction_degree = x
    fracture = fracture_strength(resin_content, curing_temp, reduction_degree)
    elongation_val = elongation(resin_content, curing_temp, reduction_degree)
    tear = tear_strength(resin_content, curing_temp, reduction_degree)
    air_perm = air_permeability(resin_content, curing_temp, reduction_degree)
    moisture_perm = moisture_permeability(resin_content, curing_temp, reduction_degree)
    soft = softness(resin_content, curing_temp, reduction_degree)
    wrinkle = wrinkle_recovery(resin_content, curing_temp, reduction_degree)

    # 归一化到 [0, 1] 范围
    fracture_normalized = (fracture - 1840) / (2000 - 1840)
    elongation_normalized = (elongation_val - 0) / (0.2 - 0)
    tear_normalized = (tear - 240) / (300 - 240)
    air_perm_normalized = (air_perm - 654) / (700 - 654)
    moisture_perm_normalized = (moisture_perm - 10622) / (11000 - 10622)
    soft_normalized = (soft - 1.49625) / (2 - 1.49625)
    wrinkle_normalized = (wrinkle - 88.232665) / (100 - 88.232665)

    # 返回所有指标的负平均值
    return - (fracture_normalized + elongation_normalized + tear_normalized + air_perm_normalized +
              moisture_perm_normalized + soft_normalized + wrinkle_normalized) / 7

# 网格搜索函数
def grid_search(bounds, step_size=0.5):
    best_score = float('inf')
    best_params = None
    for resin_content in np.arange(bounds[0][0], bounds[0][1], step_size):
        for curing_temp in np.arange(bounds[1][0], bounds[1][1], step_size):
            for reduction_degree in np.arange(bounds[2][0], bounds[2][1], step_size):
                score = objective((resin_content, curing_temp, reduction_degree))
                if score < best_score:
                    best_score = score
                    best_params = (resin_content, curing_temp, reduction_degree)
    return best_params, best_score

# 定义搜索范围
bounds = [(15, 30), (100, 130), (0, 30)]

# 执行网格搜索
best_params, best_score = grid_search(bounds, step_size=0.5)

# 输出结果
print(f"树脂含量: {best_params[0]}")
print(f"固化温度: {best_params[1]}")
print(f"减量程度: {best_params[2]}")

# 计算优化后的目标值
print(f"断裂强力: {fracture_strength(*best_params)}")
print(f"断裂伸长量: {elongation(*best_params)*10}")
print(f"撕裂强力: {tear_strength(*best_params)}")
print(f"透气率: {air_permeability(*best_params)}")
print(f"透湿率: {moisture_permeability(*best_params)}")
print(f"柔软度: {softness(*best_params)}")
print(f"折皱回复率: {wrinkle_recovery(*best_params)}")
