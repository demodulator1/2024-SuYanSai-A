import pandas as pd
from scipy.stats import spearmanr
import seaborn as sns
import matplotlib.pyplot as plt

# 设置中文字体
plt.rcParams['font.family'] = ['Microsoft YaHei']

# 读取Excel文件
df = pd.read_excel('scaled_data.xlsx')

# 选择要分析的列
columns = ['树脂含量（wt%）', '固化温度(℃)', '减量程度（%）', '断裂强力', '断裂伸长量', '撕裂强力', '透气率', '透湿率', '柔软度', '折皱回复率']
data = df[columns]

# 计算斯皮尔曼相关系数
correlation_matrix, p_values = spearmanr(data)

# 将相关系数矩阵转换为DataFrame以便于查看
correlation_df = pd.DataFrame(correlation_matrix, index=columns, columns=columns)

# 绘制热力图
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_df, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
plt.title('工艺参数与产品性能之间的斯皮尔曼相关性热力图')
plt.show()
