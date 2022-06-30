import cv2
import os

video_path = r'C:/Users/BJM/Videos/videos1080P/'
videos = os.listdir(video_path)
for video_name in videos:
    file_name = video_name.split('.')[0]
    folder_name = video_path + file_name
    os.makedirs(folder_name,exist_ok=True)
    vc = cv2.VideoCapture(video_path+video_name) #读入视频文件
    c=1 
     
    timeF = 15 #视频帧计数间隔频率 
     
    while (True):  #循环读取视频帧 
        pic_path = folder_name+'/'
        rval, frame = vc.read() 
        if rval:

            if(c % timeF == 0): #每隔timeF帧进行存储操作 
                print("开始截取视频第：" + str(c) + " 帧")
                cv2.imwrite(pic_path + file_name + str(c) + '.jpg',frame) #存储为图像 
            c = c + 1 
            cv2.waitKey(1)
        else:
            print("所有帧已经保存完成")
            break 
    vc.release()
    print('save_success')




