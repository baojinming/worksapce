from PIL import Image
from PIL import ImageEnhance
import os
import cv2
import numpy as np
imageDir="C://Users//ylc//Desktop//left//new//" #要改变的图片的路径文件夹
saveDir="C://Users//ylc//Desktop//left//enhance//"   #要保存的图片的路径文件夹
def move(root_path,img_name,off): #平移，平移尺度为off
    img = Image.open(os.path.join(root_path, img_name))
    offset = img.offset(off,0)
    return offset

def flip(root_path,img_name):   #翻转图像
    img = Image.open(os.path.join(root_path, img_name))
    #filp_img = img.transpose(Image.FLIP_LEFT_RIGHT)#左右翻转
    filp_img = img.transpose(Image.FLIP_TOP_BOTTOM)#上下翻转
    # filp_img.save(os.path.join(root_path,img_name.split('.')[0] + '_flip.jpg'))
    return filp_img

def rotation(root_path, img_name):#旋转图像
    img = Image.open(os.path.join(root_path, img_name))
    rotation_img = img.rotate(90) #旋转角度
    # rotation_img.save(os.path.join(root_path,img_name.split('.')[0] + '_rotation.jpg'))
    return rotation_img

i=0
for name in os.listdir(imageDir):
    i=i+1
    saveName="qipao"+str(i)+".bmp"#自定义图片名
    #saveImage=flip(imageDir,name)#选择对应的功能函数
    saveImage=rotation(imageDir,name)
    saveImage.save(os.path.join(saveDir,saveName))