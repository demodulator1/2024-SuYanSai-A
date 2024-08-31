import numpy as np

# 定义柔软度回归方程
def softness(resin_content, curing_temp, reduction_degree):
    return 1.49625 - (0.04875 * resin_content) + (0.005625 * curing_temp) + (0.067875 * reduction_degree)

# 定义折皱回复率回归方程
def wrinkling_recovery_rate(resin_content, curing_temp, reduction_degree):
    return 88.232665 + (2.362457 * resin_content) + (0.567772 * curing_temp) + (0.653567 * reduction_degree) \
        + (-0.038973 * resin_content ** 2) + (-0.005583 * resin_content * curing_temp) + (0.004328 * resin_content * reduction_degree) \
        + (-0.001423 * curing_temp ** 2) + (0.000496 * curing_temp * reduction_degree) + (-0.013223 * reduction_degree ** 2)

# 目标函数
def objective(x):
    resin_content, curing_temp, reduction_degree = x
    softness_val = softness(resin_content, curing_temp, reduction_degree)
    wrinkling_rate_val = wrinkling_recovery_rate(resin_content, curing_temp, reduction_degree)

    # 对数据标准化
    softness_normalized = (softness_val - 1) / (2 - 1)
    wrinkling_rate_normalized = (wrinkling_rate_val - 80) / (100 - 80)

    # 返回所有指标的负平均值，目标是最大化这些值
    return - (softness_normalized + wrinkling_rate_normalized) / 2

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
print(f"柔软度: {softness(*best_params)}")
print(f"折皱回复率: {wrinkling_recovery_rate(*best_params)}")
