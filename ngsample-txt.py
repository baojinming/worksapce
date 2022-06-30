import os  
import io  
import math
import sys
import cv2
import shutil
import random
import numpy as np
from collections import namedtuple, OrderedDict  

def get_files(dir, suffix): 
    res = []
    for root, directory, files in os.walk(dir):
        for filename in files:
            name, suf = os.path.splitext(filename) 

            if suf in suffix:
                #res.append(filename)
                res.append(os.path.join(root, filename))
    return res

def random_filter_image(list_path,random_rate):
    image_list = get_files(list_path, ['.jpg'])
    total_len = len(image_list)
    print('total_label_len', total_len)
    for i in range(0, total_len):
        #随机过滤图片
        '''
        gen_rate = random.random()
        if (gen_rate < random_rate):
            pass
        else:
            os.remove(image_list[i])
            continue
        '''
        #生成负样本txt文件
        image_file = image_list[i]
        file_name, type_name = os.path.splitext(image_file)
        file_txt_name = file_name + '.txt'
        with open(file_txt_name,"w",encoding="utf-8") as f_w:
            pass

    random.shuffle(image_list)

def main():  
    global random_rate
    #list_path = r'C:\Users\Administrator\Desktop\negative_image\101\outsourcing_data\201210'
    list_path = r'D:\\data\\cloth&helmet'

    # save_base_dir= r'D:/data/xml/'
    random_rate = 0.25
    random_filter_image(list_path,random_rate)
if __name__ == '__main__':  

    main()
