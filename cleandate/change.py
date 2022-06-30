import cv2
import os
inputpath = "C://Users//ylc//Desktop//point1//"
outputpath = "C://Users//ylc//Desktop//new//"
for file_name in os.listdir(inputpath):
	img=cv2.imread(inputpath + file_name,cv2.IMREAD_GRAYSCALE)
	cv2.imwrite(outputpath+file_name,img)