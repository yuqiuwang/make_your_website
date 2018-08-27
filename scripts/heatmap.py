# -*- coding: utf-8 -*-
"""
Author  : yuqiuwang
Mail    : yuqiuwang929@gmail.com
Website : https://www.yuqiulearn.cn
Created : 2018/8/3 11:28
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cm
import re
plt.switch_backend('agg')

class HeatMap:

    def __init__(self, data_path, save_type="png", color="RdYlBu_r"):
        self.data_path = data_path
        self.color = color
        self.save_type = save_type

    def read_data(self):
        # "C:/Users/wangyuqiu1/Desktop/test.xlsx"
        if re.findall('.xlsx$', self.data_path):
            datas = pd.read_excel(self.data_path)
        elif re.findall('.csv$', self.data_path):
            datas = pd.read_excel(self.data_path)
        elif re.findall('.txt$', self.data_path):
            datas = pd.read_table(self.data_path)
        else:
            raise IOError("only xlsx/txt/csv supported!!")
        # 提取数据中的最大值，最小值，以及header
        header = []
        data_max = 0
        data_min = 0
        for x in datas:
            header.append(str(x))
            if datas[x][np.argmax(datas[x])] > data_max:
                data_max = datas[x][np.argmax(datas[x])]
            if datas[x][np.argmin(datas[x])] < data_min:
                data_min = datas[x][np.argmin(datas[x])]
        return datas, header, data_max, data_min

    def map_color(self):
        cmap = matplotlib.cm.get_cmap(self.color, 1000)
        return cmap

    def main(self):
        datas, header, data_max, data_min = self.read_data()
        plt.figure()
        plt_tmp = plt.imshow(datas, interpolation="nearest", cmap=self.map_color(), aspect='auto', vmin=data_min, vmax=data_max)
        plt.xticks(range(len(header)), header, rotation=60)
        plt.yticks((),())
        cb = plt.colorbar(mappable=plt_tmp, cax=None, ax=None, shrink=1)
        cb.set_label('(%)')
        plt.savefig(self.data_path+"."+self.save_type)

#HeatMap("C:/Users/wangyuqiu1/Desktop/test.xlsx", save_type="png", color="RdYlBu_r").main()
