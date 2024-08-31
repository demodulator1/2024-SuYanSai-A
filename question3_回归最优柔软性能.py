import numpy as np

# 定义透气率回归方程
def air_permeability(resin_content, curing_temp, reduction_degree):
    return 654.596534 + (0.042795 * resin_content) + (-4.425432 * curing_temp) + (-20.034932 * reduction_degree) \
        + (-0.370575 * resin_content ** 2) + (0.227257 * resin_content * curing_temp) + (-0.135007 * resin_content * reduction_degree) \
        + (-0.026606 * curing_temp ** 2) + (0.281106 * curing_temp * reduction_degree) + (-0.393256 * reduction_degree ** 2)

# 定义透湿率回归方程
def moisture_permeability(resin_content, curing_temp, reduction_degree):
    return 10622.534531 + (-233.822679 * resin_content) + (-88.785737 * curing_temp) + (20.464182 * reduction_degree) \
        + (2.374558 * resin_content ** 2) + (0.354642 * resin_content * curing_temp) + (1.728879 * resin_content * reduction_degree) \
        + (0.386926 * curing_temp ** 2) + (-0.477996 * curing_temp * reduction_degree) + (0.063604 * reduction_degree ** 2)

# 目标函数
def objective(x):
    resin_content, curing_temp, reduction_degree = x
    air_perm = air_permeability(resin_content, curing_temp, reduction_degree)
    moisture_perm = moisture_permeability(resin_content, curing_temp, reduction_degree)

    # 对数据标准化
    air_perm_normalized = (air_perm - 600) / (700 - 600)  # 示例范围
    moisture_perm_normalized = (moisture_perm - 10000) / (12000 - 10000)  # 示例范围

    # 返回所有指标的负平均值，目标是最大化这些值
    return - (air_perm_normalized + moisture_perm_normalized) / 2

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
print(f"透气率: {air_permeability(*best_params)}")
print(f"透湿率: {moisture_permeability(*best_params)}")
