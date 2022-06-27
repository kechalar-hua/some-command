import pandas as pd
import numpy as np
# from sklearn import metrics
# import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN
from sklearn import preprocessing
# 导入数据
pd.set_option('display.width', None)  # 设置数据展示宽度
pd.set_option('display.max_rows', None)  # 设置数据展示宽度
beer = pd.read_csv('data.txt', sep='\t')
predictors = ["identity", "mismatch", "allele-tag"]
X = preprocessing.scale(beer[predictors])
X = pd.DataFrame(X)

# 寻找最佳参数
res = []
# 迭代不同的eps值
for eps in np.arange(0.001, 1, 0.001):
    # 迭代不同的min_samples值
    for min_samples in range(1, 10):
        dbscan = DBSCAN(eps=eps, min_samples=min_samples)
        # 模型拟合
        dbscan.fit(X)
        # 统计各参数组合下的聚类个数（-1表示异常点）
        n_clusters = len([i for i in set(dbscan.labels_) if i != -1])
        # 异常点的个数
        outliners = np.sum(np.where(dbscan.labels_ == -1, 1, 0))
        # 统计每个簇的样本个数
        stats = str(pd.Series([i for i in dbscan.labels_ if i != -1], dtype='float64').value_counts().values)
        res.append({'eps': eps, 'min_samples': min_samples, 'n_clusters': n_clusters,
                    'outliners': outliners, 'stats': stats})
# 将迭代后的结果存储到数据框中
df = pd.DataFrame(res)

# 根据条件筛选合理的参数组合
# var = df.loc[df.n_clusters == 2, :]
print(df)
# df.to_csv('factor_list.txt', index=False, header=False)

# # 用最佳参数作图
# # 设置半径为10，最小样本量为2，建模
# dbscan = DBSCAN(eps=0.05, min_samples=2)
# db = dbscan.fit(X)
# labels = db.labels_
# beer['cluster_db'] = labels  # 在数据集最后一列加上经过DBSCAN聚类后的结果
# beers = beer.sort_values('cluster_db')  # 根据数据集最后一列升序排序
# print(beer.groupby('cluster_db').mean())
#print(pd.plotting.scatter_matrix(X, c=beer.cluster_db.tolist(), figsize=(10, 10), s=200))
#plt.show()
# # 就是下面这个函数可以计算轮廓系数来评估聚类效果
# score = metrics.silhouette_score(X, beer.cluster_db)
# print(score)
# # pandas的dataFrame写入文件
# beers.to_csv('data_cluster.txt', index=False, header=False)
