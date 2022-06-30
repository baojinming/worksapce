import numpy as np
from numpy import random
import pandas as pd
import matplotlib.pyplot as plt
import os
import math
import seaborn as sns
import xml.etree.ElementTree as ET
sns.set()

def getheatmap(matrix):
    fig = plt.figure()
    sns_plot = sns.heatmap(matrix,square=True,annot=True,robust=True,fmt="d")

    #sns_plot = sns.heatmap(R)
    sns_plot.tick_params(labelsize=10) # heatmap 刻度字体大小
    plt.title("heatmap")

	# fig.savefig("heatmap.pdf", bbox_inches='tight') # 减少边缘空白
    plt.show()




if __name__ == "__main__":

    # 源文件夹
    sourceDir = "C:/Users/BJM/Desktop/auto_label/Annotation2/"
    # sourceDir ="D:/data/smokeandphone/paper_data_ngsample/Annotations/"
    # 结果保存文件夹
    matrix = np.zeros((10, 10),dtype=np.int)
    # print(a)
    #targetDir = "D:/data/smoke_and_phone-Retraction/"
    #start(sourceDir, targetDir, 400, 400)
    #for root, dir1, filenames in os.walk(sourceDir):
    for filename in os.listdir(sourceDir):
        xml_name = os.path.join(sourceDir, filename)     
        # read_xml(xml_name)
        etree = ET.parse(xml_name)
        root = etree.getroot()
        for obj in root.iter('size'):
            width = obj.find('width').text
            height = obj.find('height').text
        
        for obj in root.iter('object'):
            xmin,ymin,xmax,ymax = (x.text for x in obj.find('bndbox'))
            box_w = int(xmax) - int(xmin)
            box_h = int(ymax) - int(ymin)
            valu_w = int(box_w * 10/ float(width))
            valu_h = int(box_h * 10/ float(height))
            matrix[valu_h, valu_w] = matrix[valu_h, valu_w] + 1

    print(matrix)
    print(matrix.sum())
    getheatmap(matrix)
    print('完成！')





