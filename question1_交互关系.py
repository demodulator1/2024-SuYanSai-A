import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

# 数据准备
data = {
    '树脂含量': [15, 15, 15, 15, 20, 20, 20, 20, 25, 25, 25, 25, 30, 30, 30, 30],
    '固化温度': [100, 110, 120, 130, 100, 110, 120, 130, 100, 110, 120, 130, 100, 110, 120, 130],
    '减量程度': [0, 10, 20, 30, 10, 0, 30, 20, 20, 30, 0, 10, 30, 20, 10, 0],
    '断裂强力': [1781.9181, 1142.4154, 1199.74011, 1218.922, 1164.56934, 1652.4389, 1211.408, 1233.107,
                 1182.962, 1248.54871, 1759.6982, 1214.9815, 1249.2589, 1250.4569, 1207.59863, 1730.8907]
}

# 创建 DataFrame
df = pd.DataFrame(data)

# 方差分析 (ANOVA) 函数
def anova(df, formula):
    model = ols(formula, data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    return anova_table

# 定义模型公式
formulas = {
    '树脂含量': '断裂强力 ~ C(树脂含量)',
    '固化温度': '断裂强力 ~ C(固化温度)',
    '减量程度': '断裂强力 ~ C(减量程度)',
    '交互效应：树脂含量*固化温度': '断裂强力 ~ C(树脂含量) * C(固化温度)',
    '交互效应：树脂含量*减量程度': '断裂强力 ~ C(树脂含量) * C(减量程度)',
    '交互效应：固化温度*减量程度': '断裂强力 ~ C(固化温度) * C(减量程度)',
}

# 计算 ANOVA
results = []
for key, formula in formulas.items():
    try:
        table = anova(df, formula)
        for source in table.index:
            results.append([key, source, table.loc[source, 'sum_sq'], table.loc[source, 'df'],
                            table.loc[source, 'mean_sq'] if 'mean_sq' in table.columns else 'N/A',
                            table.loc[source, 'F'] if 'F' in table.columns else 'N/A'])
    except Exception as e:
        print(f"Error processing formula '{key}': {e}")

# 随机误差计算
model = ols('断裂强力 ~ C(树脂含量) * C(固化温度) * C(减量程度)', data=df).fit()
anova_table = sm.stats.anova_lm(model, typ=2)
ss_total = anova_table['sum_sq'].sum()
ss_between = sum([result[2] for result in results if '交互效应' in result[0]])
ss_within = ss_total - ss_between
df_within = len(df) - len(anova_table.index)
ms_within = ss_within / df_within

results.append(['随机误差', '剩余', ss_within, df_within, ms_within, 'N/A'])

# 创建 DataFrame 并输出
results_df = pd.DataFrame(results, columns=['方差来源', '离差平方和', '自由度', '均方', 'F值'])
print(results_df)
