# coding: utf-8
import numpy as np
import cv2
 
def motion_blur(image, degree=5, angle=45):
    image = np.array(image)
 
    # 这里生成任意角度的运动模糊kernel的矩阵， degree越大，模糊程度越高
    M = cv2.getRotationMatrix2D((degree / 2, degree / 2), angle, 1)
    motion_blur_kernel = np.diag(np.ones(degree))
    motion_blur_kernel = cv2.warpAffine(motion_blur_kernel, M, (degree, degree))
 
    motion_blur_kernel = motion_blur_kernel / degree
    blurred = cv2.filter2D(image, -1, motion_blur_kernel)
 
    # convert to uint8
    cv2.normalize(blurred, blurred, 0, 255, cv2.NORM_MINMAX)
    blurred = np.array(blurred, dtype=np.uint8)
    return blurred
 
img = cv2.imread('./ts1.jpg')
img_10 = motion_blur(img,degree=3)
img_11 = motion_blur(img,degree=7)
img_12 = motion_blur(img,degree=15)
img_13 = motion_blur(img,degree=24)
img_14 = motion_blur(img,degree=40)
img_ = cv2.GaussianBlur(img, ksize=(5, 5), sigmaX=0, sigmaY=0)
img_2 = cv2.GaussianBlur(img, ksize=(9, 9), sigmaX=0, sigmaY=0)
img_3 = cv2.GaussianBlur(img, ksize=(15, 15), sigmaX=0, sigmaY=0)
img_4 = cv2.GaussianBlur(img, ksize=(25, 25), sigmaX=0, sigmaY=0)
img_5 = cv2.GaussianBlur(img, ksize=(37, 37), sigmaX=0, sigmaY=0)
#cv2.namedWindow("1", cv2.WINDOW_NORMAL)
cv2.imshow('source',img)
#cv2.namedWindow("2", cv2.WINDOW_NORMAL)
cv2.imshow('5x5',img_)
cv2.imshow('9x9',img_2)
cv2.imshow('15x15',img_3)
cv2.imshow('25x25',img_4)
cv2.imshow('37x37',img_5)
cv2.waitKey()