import cv2
import numpy as np
import random
from matplotlib import pyplot as plt
import os
from itertools import product
import threading

# 常规规马赛克
inputpath = "D:/data/picClarityDatasets/sourcePic/"
outputpath = "D:/data/picClarityDatasets/outputPic/"


# txtfilepath = "D:/data/picClarityDatasets/txtfile/"

def do_mosaic(img, m, n, neighbor=5):
    """
    :param rgb_img
    :param int x :  马赛克左顶点
    :param int y:  马赛克左顶点
    :param int w:  马赛克宽
    :param int h:  马赛克高
    :param int neighbor:  马赛克每一块的宽
    """
    img_s4 = img.copy()
    portion_size = (int(m * W / 10), int(n * H / 10))
    if img.shape(0)==720:  ##720P图片随机范围x() y(0,40)
        x = random.randint(0, 620)
        y = random.randint(0, 40)
    elif img.shape(0)==1080:  ##1080P图片随机范围x(0,900) y(0,60)
        x = random.randint(0, 900)
        y = random.randint(0, 60)

    x1, y1 = x + portion_size[0], y + portion_size[1]
    roi = [x, y, x1, y1]  # x1,y1,x2,y2  x1,y1选择区域左上角点；x2,y2为选择区域右下角点
    # leftUp = (x,y)
    # rightDown = (x1,y1)
    x = roi[0]
    y = roi[1]
    w = roi[2] - roi[0]
    h = roi[3] - roi[1]
    for a in range(0, h, neighbor):
        for b in range(0, w, neighbor):
            rect = [b + x, a + y]
            color = img_s4[a + y][b + x].tolist()  # 关键点1 tolist
            # print(color)
            left_up = (rect[0], rect[1])
            x2 = rect[0] + neighbor - 1  # 关键点2 减去一个像素位置
            y2 = rect[1] + neighbor - 1
            if x2 > x + w:
                x2 = x + w
            if y2 > y + h:
                y2 = y + h
            right_down = (x2, y2)
            cv2.rectangle(img_s4, left_up, right_down, color, -1)  # 替换为为一个颜值值

    return img_s4


# 三原色马赛克
def do_mosaic_rgb(img, m, n, color):
    img_s2 = img.copy()
    portion_size = (int(m * W / 10), int(n * H / 10))
    x1 = random.randint(0, W - portion_size[0])
    y1 = random.randint(0, H - portion_size[1])
    x2, y2 = x1 + portion_size[0], y1 + portion_size[1]
    img_s2[x1:x2, y1:y2] = color
    # i=0
    # 增加随机度
    # while (i<5):
    #     img_s2[x1+random.randint(0,W-portion_size[0]):x2+random.randint(0,W-portion_size[0]),y1+random.randint(0,H-portion_size[1]):y2+random.randint(0,H-portion_size[1])] = color
    #     i=i + 1
    return img_s2


# 椒盐噪点
def addsalt_pepper(img, SNR):
    img_ = img.copy()
    c, h, w = img_.shape
    mask = np.random.choice((0, 1, 2), size=(1, h, w), p=[SNR, (1 - SNR) / 2., (1 - SNR) / 2.])
    mask = np.repeat(mask, c, axis=0)  # 按channel 复制到 与img具有相同的shape
    img_[mask == 1] = 255  # 盐噪声
    img_[mask == 2] = 0  # 椒噪声

    return img_


# 运动模糊
def motion_blur(image, degree=5, angle=135):
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


# 高斯模糊
def GaussianBlur(img, n):
    img_ = cv2.GaussianBlur(img, ksize=n, sigmaX=0, sigmaY=0)
    return img_


# ==========================
# 打分函数
# =========================
# 不同程度椒盐噪点自定义评分函数
def saltPepper_Score(i):
    score = 0
    if 940 < i <= 1000:
        score = round(100 - 500 * (1 - i / 1000))
    elif 860 < i <= 940:
        score = round(70 - 250 * (0.94 - i / 1000))
    elif 700 < i <= 860:
        score = round(50 - 125 * (0.86 - i / 1000))
    elif 400 < i <= 700:
        score = round(30 - 100 * (0.7 - i / 1000))
    return score


# 不同程度高斯滤波自定义评分函数
def GaussianBlur_Score(i):
    score = 0
    if 0 <= i <= 6:
        score = round(100 - 5 * i, 2)
    elif 6 < i <= 11:
        score = round(70 - (i - 6) * 4, 2)
    elif 11 < i <= 36:
        score = round(50 - (i - 11) * 2, 2)
    return score


# 不同程度同色马赛克自定义评分函数
def mosaic_rgb_Score(m, n):
    score = 0
    if m * n <= 5:
        score = round(90 - 2 * m * n, 2)
    elif 5 < m * n <= 15:
        score = round(80 - 2 * (m * n - 5), 2)
    elif 15 < m * n <= 25:
        score = round(60 - 3 * (m * n - 15), 2)
    elif 25 < m * n <= 35:
        score = round(30 - 3 * (m * n - 25), 2)
    return score


# 不同程度常规马赛克自定义评分函数
def do_mosaic_Score(m, n, k):
    score = 0
    if m * n <= 25:
        score = round(100 - m * n - 0.5 * k, 2)
    elif 25 < m * n <= 45:
        score = round(100 - 1.66 * m * n - 0.5 * k, 2)
    return score


if __name__ == "__main__":
    for pic_name in os.listdir(inputpath):
        img = cv2.imread(inputpath + pic_name, cv2.COLOR_BGR2RGB)
        file_name = pic_name.split('.')[0]
        folder_name = outputpath + file_name
        os.makedirs(folder_name, exist_ok=True)
        pic_path = folder_name + '/'
        # img=cv2.imread('./family15.jpg')  #opencv读取的是BGR数组
        size = img.shape
        W = img.shape[0]
        H = img.shape[1]

        # 椒盐噪点设置
        sub_plot = [231, 232, 233, 234, 235, 236]
        sub_plot1 = [131, 132, 133]
        # 运动模糊程度设置
        # 高斯模糊程度卷积核大小设置
        ksizeList = [(1, 1), (3, 3), (5, 5), (7, 7), (9, 9), (11, 11), (13, 13), (15, 15), (17, 17), (19, 19), (21, 21),
                     (23, 23),
                     (25, 25), (27, 27), (29, 29), (31, 31), (33, 33), (35, 35), (37, 37), (39, 39), (41, 41), (43, 43),
                     (45, 45), (47, 47), (49, 49),
                     (51, 51), (53, 53), (55, 55), (57, 57), (59, 59), (61, 61), (63, 63), (65, 65), (67, 67), (69, 69),
                     (71, 71), (73, 73)]
        # 马赛克块大小设置
        neighborList = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50]
        angleList = [30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360]
        # 整块马赛克颜色
        colorList = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]

        for i in range(len(neighborList)):
            for m in range(1, 10):
                for n in range(1, 6):
                    img_s4 = do_mosaic(img, m, n, neighbor=neighborList[i])
                    cv2.imwrite(pic_path + file_name + 'do_mosaic-neighbor={}-area={}'.format(neighborList[i],
                                                                                              m * n / 100) + '.jpg',
                                img_s4)
                    name = pic_path + file_name + "do_mosaic-neighbor={}-area={}".format(neighborList[i], m * n / 100)
                    file_path = name + '.txt'
                    file = open(file_path, 'w')
                    score_mosaic = do_mosaic_Score(m, n, neighborList[i])
                    file.write("method:mosaic" + '\n' + "neighbor={}".format(neighborList[i]) + '\n' + "area={}".format(
                        m * n / 100) + '\n' + "score:{}".format(score_mosaic)+"height:".format(img_s4.shape(0))+'\n'+"width:".format(img_s4.shape(1))+'\n')

        for i in product(range(1000,940,-2), range(940,860,-4), range(860,700,-8),range(700,400,-10)):#range(700,400,-10):#(1000,940,-2),(940,860,-4),(860,700,-8),(700,400,-10)
            img_s = addsalt_pepper(img.transpose(2, 1, 0), i/1000)
            img_s = img_s.transpose(2, 1, 0)
            cv2.imwrite(pic_path+file_name+'addsalt_pepper-SNR={}'.format(i/1000)+'.jpg',img_s)
            name = pic_path+file_name+"addsalt_pepper-SNR={}".format(i/1000)
            file_path = name + '.txt'
            file = open(file_path,'w')
            score_saltpepper = saltPepper_Score(i)
            file.write("method:addsalt_pepper"+'\n'+"SNR={}".format(i/1000)+'\n'+"score:{}".format(score_saltpepper)+"height:".format(img_s.shape(0))+'\n'+"width:".format(img_s.shape(1))+'\n')

        for i in range(len(ksizeList)):
            img_s1 = GaussianBlur(img, ksizeList[i])
            cv2.imwrite(pic_path + file_name + 'GaussianBlur-ksize={}'.format(ksizeList[i]) + '.jpg', img_s1)
            name = pic_path + file_name + "GaussianBlur-ksize={}".format(ksizeList[i])
            file_path = name + '.txt'
            file = open(file_path, 'w')
            score_GaussianBlur = GaussianBlur_Score(i)
            file.write("method:GaussianBlur" + '\n' + "ksize={}".format(ksizeList[i]) + '\n' + "score:{}".format(
                score_GaussianBlur)+"height:".format(img_s1.shape(0))+'\n'+"width:".format(img_s1.shape(1))+'\n')

        for i in range(len(colorList)):
            for m in range(1, 7):
                for n in range(1, 7):
                    img_s2 = do_mosaic_rgb(img, m, n, colorList[i])
                    cv2.imwrite(
                        pic_path + file_name + 'mosaic_rgb={}-area={}'.format(colorList[i], m * n / 100) + '.jpg',
                        img_s2)
                    name = pic_path + file_name + "mosaic_rgb={}-area={}".format(colorList[i], m * n / 100)
                    file_path = name + '.txt'
                    file = open(file_path, 'w')
                    score_mosaic_rgb = mosaic_rgb_Score(m, n)
                    file.write("method:mosaic_rgb" + '\n' + "color={}".format(colorList[i]) + '\n' + "area={}".format(
                        m * n / 100) + '\n' + "score:{}".format(score_mosaic_rgb)+"height:".format(img_s2.shape(0))+'\n'+"width:".format(img_s2.shape(1))+'\n')

        for i in range(2, 51):  # 需要手动生成原图标签，分数为100
            score_motion_blur = round(100 - 2 * i, 2)
            for j in range(len(angleList)):
                img_s3 = motion_blur(img, degree=i, angle=angleList[j])
                cv2.imwrite(pic_path + file_name + 'motion_blur-degree={}-angle={}'.format(i, angleList[j]) + '.jpg',
                            img_s3)
                name = pic_path + file_name + "motion_blur-degree={}-angle={}".format(i, angleList[j])
                file_path = name + '.txt'
                file = open(file_path, 'w')
                file.write("method:motion_blur" + '\n' + "degree={}".format(i) + '\n' + "angle={}".format(
                    angleList[j]) + '\n' + "score:{}".format(score_motion_blur)+"height:".format(img_s3.shape(0))+'\n'+"width:".format(img_s3.shape(1))+'\n')

