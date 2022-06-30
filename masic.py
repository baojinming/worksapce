from cv2 import cv2
import numpy as np

img=cv2.imread('./ts1.jpg')

enable=False
value = 10
def call_back_size(param):
    global value
    value = cv2.getTrackbarPos('size','image') #从滑块处获取值


def call_back_draw(event,x,y,flags,param):
    global enable
    global value
    if event==cv2.EVENT_LBUTTONDOWN:
        enable=True
    elif event==cv2.EVENT_MOUSEMOVE and flags==cv2.EVENT_FLAG_LBUTTON:
        if enable:
            drawMask(y,x,value)
        elif event==cv2.EVENT_LBUTTONUP:
            enable=False
# 图像局部采样函数
def drawMask(x,y,size):
    m=np.uint8(x/size)*size
    n=np.uint8(y/size)*size

    # size大小范围内的图像像素值设置为同一个像素值
    for i in range(size):
        for j in range(size):
            img[m+i][n+j]=img[m][n]

cv2.namedWindow('image')
cv2.createTrackbar("size","image",value,100,call_back_size) #创建移动滑块，最大值为100
cv2.setMouseCallback('image',call_back_draw)

while True:
    cv2.imshow('image',img)
    if cv2.waitKey(1)==ord('q'):
        break

cv2.destroyAllWindows()