import cv2 as cv
import os
 
print('----------------------------------------------------')
print('程序的功能为：将该目录下的文件夹内的png格式的图片转为jpg')
print('转化为的结果: 在用户输入的文件夹名_1')
print('----------------------------------------------------')
print('')
 
son = input('请输入该目录下文件夹名：')
daddir= 'D:\\data\\cloth&helmet\\'
print(daddir)
path = daddir + son+'\\'
 
newpath = son+'_1'
if not os.path.exists(newpath):
    os.mkdir(newpath)
print(newpath)
 
path_list=os.listdir(path)
path_list.sort()
for filename in path_list:
    portion = os.path.splitext(filename)
    print('convert  ' + filename +'  to '+portion[0]+'.jpg')
    src = cv.imread(path+filename)
    cv.imwrite(newpath+'\\'+portion[0]+'.jpg',src)
 
print('转换完毕，文件存入 '+newpath+' 中')
cv.waitKey(0)
cv.destroyAllWindows()
