# -*- coding: utf-8 -*-
"""
Author  : yuqiuwang
Mail    : yuqiuwang929@gmail.com
Website : https://www.yuqiulearn.cn
Created : 2017/11/17 12:30
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.cluster import KMeans
import os
import re
plt.switch_backend('agg')

"""
用于数据聚类后绘图
输入csv文件，excel格式如下：
--------------------------------------------
sample_name	day1	day2	day3	day4	day5	day6
sample1	2.1	2.13	2.2	1.1	2.3	2.1
sample2	2.1	2.13	3	1.1	2	3
sample3	7	2.13	2.2	2	2.3	2.1
sample4	2.1	2.13	2.2	1.1	5	1
sample5	2.1	2.13	5	5	2.3	2.1
...
--------------------------------------------
输出png格式图片，及聚类后的详细信息
"""
"""
#USAGE:
#    python K_means.py -i your.csv -n cluster_num
#e.g.
#    python K_means.py -i c:/User/shenmegui/Desktop/sample.csv -n 10
#    python K_means.py -i ./sample.csv -n 10
"""

class ClusterPlot:

    def __init__(self,sample_path,cluster_num):
        self.sample_path = sample_path
        self.cluster_num = cluster_num
        
    def read_data(self):
        if re.findall('.xlsx$', self.sample_path):
            data = pd.read_excel(self.sample_path)
        elif re.findall('.csv$', self.sample_path):
            data = pd.read_excel(self.sample_path)
        elif re.findall('.txt$', self.sample_path):
            data = pd.read_table(self.sample_path)
        else:
            raise IOError("only xlsx/txt/csv supported!!")
        col_names = data.columns
        col_names = col_names[1:].tolist()
        data = np.array(data)
        return col_names,data

    def data_cluster(self,data):
        cluster_idx = KMeans(n_clusters=self.cluster_num).fit_predict(data[:,1:])
        reshape_data = []
        cluster_name = []
        for x in range(0,self.cluster_num):
            reshape_data.append([])
            cluster_name.append([])
            for y in range(0,len(cluster_idx)):
                if cluster_idx[y] == x:
                    reshape_data[-1].append(data[y,1:].tolist())
                    cluster_name[-1].append(data[y,0])
        reshape_data = np.array(reshape_data)
        return cluster_name,reshape_data
    
    def mean_data(self,reshape_data):
        mean_cluster = []
        for x in range(0,len(reshape_data)):
            tmp_data = reshape_data[x]
            tmp_data = np.array(tmp_data)
            mean_cluster.append(np.mean(tmp_data[:,:],axis = 0))
        mean_cluster = np.array(mean_cluster)
        return mean_cluster
    
    def data_plot(self,*args):
        cluster_name,reshape_data,mean_cluster,col_names = args
        my_xticks = range(len(col_names))
        total_cols = int(self.cluster_num/4) +1
        fig = plt.figure(figsize=(21,5*total_cols))
        for x in range(0,self.cluster_num):
            ax = fig.add_subplot(total_cols,4,x+1)
            for y in reshape_data[x]:
                ax.plot(y,"gray")
            ax.plot(mean_cluster[x],"blue")
            ax.set_title("cluster%s" % str(x+1))
            ax.set_xticks(my_xticks)
            ax.set_xticklabels(col_names,rotation=45,fontsize= 'small')
        save_path = self.sample_path.replace("csv","png").replace("xlsx","png").replace("txt","png")
        plt.savefig(save_path,bbox_inches='tight')

    def main(self):
        col_names,data = self.read_data()
        cluster_name,reshape_data = self.data_cluster(data)
        save_path = self.sample_path.replace(".csv","_cluster.csv").replace(".xlsx","_cluster.csv").replace(".txt","_cluster.csv")
        f = open(save_path,'w')
        for x in range(0,len(cluster_name)):
            for y in range(0,len(cluster_name[x])):
                tmp_data = [str(i) for i in reshape_data[x][y]]
                f.writelines(["cluster_",str(x+1),",",str(cluster_name[x][y]),",",",".join(tmp_data),"\n"])
        f.close()
        mean_cluster = self.mean_data(reshape_data)
        self.data_plot(cluster_name,reshape_data,mean_cluster,col_names)
        os.system("zip %s %s*" % (self.sample_path.replace(".csv", ".zip").replace(".xlsx", ".zip").replace(".txt", ".zip"), self.sample_path.replace(".csv", "").replace(".xlsx", "").replace(".txt", "")))

'''
if __name__ == "__main__":
    parser = optparse.OptionParser()
    prog_base = os.path.split(sys.argv[0])[1]
    parser.add_option("-i", "--input", action = "store", type = "string", dest = "input_sample_path", help = "the sample path")
    parser.add_option("-n", "--num", action = "store", type = "int", dest = "cluster_num", help = "the cluster num")
    (options, args) = parser.parse_args()
    if (options.input_sample_path is None or options.cluster_num is None):
        print (prog_base + ": error: missing required command-line argument.")
        parser.print_help()
        sys.exit(0)
    Input_sample = options.input_sample_path
    Cluster_num = options.cluster_num
    my_class = cluster_plot(Input_sample,Cluster_num)
    data = my_class.main()
    print ("it's ok!")
'''
