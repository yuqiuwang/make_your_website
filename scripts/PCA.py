# -*- coding: utf-8 -*-
"""
Author  : yuqiuwang
Mail    : yuqiuwang929@gmail.com
Created : 2018/8/13 17:24
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
plt.switch_backend('agg')

class RunPCA:

    def __init__(self, data_path, save_type="png"):
        self.data_path = data_path
        self.save_type = save_type

    def main(self):
        datas = pd.read_excel(self.data_path)
        newdatas = datas.iloc[:, 1:]
        # run PCA
        pca = PCA(n_components=2)
        newdatas = pca.fit_transform(newdatas)
        labels = list(set(list(datas.iloc[:, 0])))
        colors = ["r", "b", "g", "y", "k", "c", "m", "tan", "orange", "glod"]

        plt.figure(figsize=(16, 10))

        for idx, label in enumerate(labels):
            plt.scatter(newdatas[datas.iloc[:, 0]==label][:, 0], newdatas[datas.iloc[:, 0]==label][:, 1], c=colors[idx], label=label)

        plt.legend(loc='upper right')
        plt.savefig(self.data_path+"."+self.save_type)
