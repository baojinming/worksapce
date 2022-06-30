#coding=utf-8
import numpy as np
import cv2
import os
inputpath = 'C://Users//ylc//Desktop//workspace//go//00//'
outputpath = 'C://Users//ylc//Desktop//workspace//go//cut//'
for file_name in os.listdir(inputpath):
    img =cv2.imread(inputpath + file_name,cv2.COLOR_BGR2RGB)#,cv2.IMREAD_GRAYSCALE)
    img1 = img[0:1024,0:1024]
    img2 = img[0:1024,1024:2048]
    cv2.imwrite(outputpath+"L"+file_name, img1)
    cv2.imwrite(outputpath+"R"+file_name, img2)