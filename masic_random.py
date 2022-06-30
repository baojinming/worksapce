import cv2
import numpy as np
import random

img=cv2.imread('./ts1.jpg')  #opencv读取的是BGR数组
size = img.shape
W = img.shape[0]
H = img.shape[1]
portion_size = (int(7*W/10), int(7*H/10))

x1 = random.randint(0, W-portion_size[0]) 
y1 = random.randint(0, H-portion_size[1]) 
x2, y2 = x1+portion_size[0], y1+portion_size[1]
roi=[x1,y1,x2,y2]  #x1,y1,x2,y2  x1,y1选择区域左上角点；x2,y2为选择区域右下角点

#正规马赛克
def do_mosaic(img, x, y, w, h, neighbor=5):
    """
    :param rgb_img
    :param int x :  马赛克左顶点
    :param int y:  马赛克左顶点
    :param int w:  马赛克宽
    :param int h:  马赛克高
    :param int neighbor:  马赛克每一块的宽
    """
    for i in range(0, h , neighbor):  
        for j in range(0, w , neighbor):
            rect = [j + x, i + y]
            color = img[i + y][j + x].tolist()  # 关键点1 tolist
            #print(color)
            left_up = (rect[0], rect[1])
            x2=rect[0] + neighbor - 1   # 关键点2 减去一个像素
            y2=rect[1] + neighbor - 1
            if x2>x+w:
                x2=x+w
            if y2>y+h:
                y2=y+h
            right_down = (x2,y2)  
            cv2.rectangle(img, left_up, right_down, color, -1)   #替换为为一个颜值值
    
    return img

x=roi[0]
y=roi[1]
w=roi[2]-roi[0]
h=roi[3]-roi[1]
img_mosaic=do_mosaic(img, x, y, w, h, neighbor=4)
#cv2.imwrite('img_mosaic.jpg',img_mosaic)
cv2.namedWindow('28%,4x4')
cv2.imshow('28%,20x20',img_mosaic)
cv2.waitKey(0)
cv2.destroyAllWindows()