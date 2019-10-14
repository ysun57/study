# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 17:16:11 2019

@author: sunyue
"""

"""
步骤：
1. 输入X,Y
2. 计算协方差矩阵
3. 将协方差矩阵进行特征值分解
4. 取特征值和特征向量。如取10个特征，就选择最大的10个特征值和其对应的特征向量 n_components = 10
5. 将得到的特征值和特征向量向原空间映射
"""




"""
下面代码是使用sklearn中的一个样例数据集进行PCA,将64维矩阵化为2维并展示出来
"""

import numpy as np
from sklearn import datasets
import matplotlib.pyplot as plt
import matplotlib.colors as colors




"""
生成PCA的类
"""
class PCA():
    def calculate_covariance_matrix(self, X, Y=None):
        # 2.计算协方差矩阵

        m = X.shape[0]
        X = X - np.mean(X, axis=0)
        Y = X if Y == None else Y - np.mean(Y, axis=0)
        
        print(X.shape, Y.shape)
        
        return 1 / m * np.matmul(X.T, Y)

    def transform(self, X, n_components):
        # 设n=X.shape[1]，将n维数据降维成n_component维
        # 2. 计算协方差矩阵
        covariance_matrix = self.calculate_covariance_matrix(X)

        # 3. 获取特征值，和特征向量
        eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)

        # 4. 对特征向量排序，并取最大的前n_component组
        idx = eigenvalues.argsort()[::-1]
        eigenvectors = eigenvectors[:, idx]
        eigenvectors = eigenvectors[:, :n_components]

        # 5. 转换
        return np.matmul(X, eigenvectors)

"""
PCA结束
"""

# 1. 读取数据
data = datasets.load_digits()
X = data.data
y = data.target

# PCA
# 原题中此处nComponent应为10
# nCoponentms = 2
nCoponentms = 2
X_trans = PCA().transform(X, nCoponentms)


"""
PCA 效果展示
"""

x1 = X_trans[:, 0]
x2 = X_trans[:, 1]

cmap = plt.get_cmap('viridis')
colors = [cmap(i) for i in np.linspace(0, 1, len(np.unique(y)))]

class_distr = []
# Plot the different class distributions
for i, l in enumerate(np.unique(y)):
    _x1 = x1[y == l]
    _x2 = x2[y == l]
    _y = y[y == l]
    class_distr.append(plt.scatter(_x1, _x2, color=colors[i]))

# Add a legend
plt.legend(class_distr, y, loc=1)

# Axis labels
plt.suptitle("PCA Dimensionality Reduction")
plt.title("Digit Dataset")
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.show()
