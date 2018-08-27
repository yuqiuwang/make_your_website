# -*- coding: utf-8 -*-
"""
Author  : yuqiuwang
Mail    : yuqiuwang929@gmail.com
Website : https://www.yuqiulearn.cn
Created : 2018/8/8 14:42
"""

import heatmap
import PCA
import K_means

class SqlConfig:

    host = "localhost"
    user = 'root'
    port = 3306
    passwd = 'wangyuqiu'
    dbname = 'PAPERS'
    table_name = "MY_PAPER"
    charset = 'utf8'


class WebConfig:

    items_page = 10
    
class DrawingConfig:

    def __init__(self, file_path, save_type="png", color="YdYlBu_r", clusters=2):
        self.file_path = file_path
        self.save_type = save_type
        self.color = color
        self.clusters = clusters
    
    @property
    def heatmap(self):
        return heatmap.HeatMap(self.file_path, save_type=self.save_type, color=self.color).main()
    
    @property
    def pca(self):
        return PCA.RunPCA(self.file_path, save_type=self.save_type).main()
    
    @property
    def K_means(self):
        return K_means.ClusterPlot(self.file_path, self.clusters).main()
