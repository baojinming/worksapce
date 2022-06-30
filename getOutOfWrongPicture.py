#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import os
import cv2
from glob import glob
from scipy import misc

def load_image_cv(path_img):
    file_names = glob(path_dir + '/*.jpg')
    with open(r'invailfile3.txt', 'w+') as txt:

        for file in file_names:
            try:
                img_raw = cv2.imread(file, flags=-1)
                cv2.imwrite(file, img_raw)
            except:
                print("fail load" + file + '\n')
    return

def load_save_image_misc(path_dir):
    file_names = glob(path_dir+'/*.jpg')
    with open(r'invailfile3.txt', 'w+') as txt:
        for file in file_names:
            print(file + '\n')
            try:
                img_raw = misc.imread(file)
                misc.imsave(file, img_raw)
            except:
                txt.write(file+'\n')
                print("fail load" + file + '\n')

    return

if __name__ == '__main__':
    # ----imread to imwrite-----------------------------------------------------------
    path_dir = "D:/data/cloth&helmet/dataset/paperdata_suits&person/images"   # 数据存放的目录
    # load_save_image_misc(path_dir)
    img=misc.imread("D:\\data\\cloth&helmet\\dataset\\paperdata_suits&person\\images\\cloth3853.jpg")
    cv2.imshow("image",img)
    cv2.waitKey(0)
    # load_image_cv((path_dir))
