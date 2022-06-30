import os
import xml.dom.minidom
import xml.etree.ElementTree
import xml.etree.ElementTree as ET
from PIL import Image
from PIL import ImageEnhance
import cv2
import glob
import numpy as np
'''
######################

#更改XML的filename

######################

path = 'C:/Users/BJM/Desktop/2_1'  # xml文件存放路径
sv_path = 'C:/Users/BJM/Desktop/2_2'  # 修改后的xml文件存放路径
files = os.listdir(path)

for xmlFile in files:
    dom = xml.dom.minidom.parse(os.path.join(path, xmlFile))  # 打开xml文件，送到dom解析
    root = dom.documentElement  # 得到文档元素对象
    names = root.getElementsByTagName('filename')
    a, b = os.path.splitext(xmlFile)  # 分离出文件名a
    for n in names:
        n.firstChild.data = a + '.jpg'
    with open(os.path.join(sv_path, xmlFile), 'w') as fh:
        dom.writexml(fh)
'''
#######################

#修改XML里的节点内容

#######################

''' 
xmldir = 'C:\\Users\\ylc\\Desktop\\heibaidian\\xml-3\\'
xmldir1 = 'C:\\Users\\ylc\\Desktop\\heibaidian\\xml-1\\'
for xmlfile in os.listdir(xmldir):
    xmlname = os.path.splitext(xmlfile)[0]
 
    #read the xml file
    dom = xml.dom.minidom.parse(os.path.join(xmldir,xmlfile))
    root = dom.documentElement
 
    #obtain the filename label pair and give it a new value
    #root.getElementsByTagName('filename')[0].firstChild.data = xmlname + '.jpg'
    #root.getElementsByTagName('path')[0].firstChild.data = '/home/dulingwen/Music/jpg/' + xmlname + '.jpg'
    #root.getElementsByTagName('width')[0].firstChild.data = '800'
    #root.getElementsByTagName('height')[0].firstChild.data = '800'
    root.getElementsByTagName('depth')[0].firstChild.data = '1'
    xml_specific = xmldir1 + xmlfile
    with open(xml_specific,'w') as fh:
        dom.writexml(fh)
'''

######################

#更改文件名

######################
'''
class BatchRename():
    # 批量重命名文件夹中的图片文件
    
 
    def __init__(self):
        self.path = 'C:\\Users\\BJM\\Desktop\\1'  # 表示需要命名处理的文件夹
        self.new_path = 'C:\\Users\\BJM\\Desktop\\1_1'     # 表示图片处理后保存的文件夹，
 
    def rename(self):
        filelist = os.listdir(self.path)  # 获取文件路径
        total_num = len(filelist)  # 获取文件长度（个数）
        i = 000  # 表示文件的命名是从1开始的
        for item in filelist:
            if item.endswith('.jpg'):  # 初始的图片的格式为jpg格式的（或者源文件是png格式及其他格式，后面的转换格式就可以调整为自己需要的格式即可）
                src = os.path.join(os.path.abspath(self.path), item)
                dst = os.path.join(os.path.abspath(self.new_path), 'ng' + str(i) + '.jpg')  # 处理后的格式也为jpg格式的，当然这里可以改成png格式
               # dst = os.path.join(os.path.abspath(self.new_path),
                                    #format(str(i), '0>2s') +'_add' '.jpg')  # 这种情况下的命名格式为000.jpg形式，可以自主定义想要的格式
                try:
                    os.rename(src, dst)
                    print('converting %s to %s ...' % (src, dst))
                    i = i + 1
                except:
                    continue
        print('total %d to rename & converted %d jpgs' % (total_num, i))


if __name__ == '__main__':
    demo = BatchRename()
    demo.rename()
'''
'''
 ####################

#修改图片尺寸大小

#####################

#obtain the filename
path_ori = '/home/dulingwen/Music/jpg/'
filename = os.listdir(path_ori)
 
#resize the image
for fn in filename:
    img = cv2.imread(path_ori+fn)
    dim = (800,800)
    img_res = cv2.resize(img,dim,interpolation=cv2.INTER_AREA)
    cv2.imwrite(path_ori+fn,img_res)
'''
'''
#####################
修改xml里标签名称
通过解析xml文件，批量修改xml文件里的标签名称，比如把标签suit改成suits
#####################
'''

path = r'D:\\data\\cloth&helmet\\dataset\\paperdata_suits&person\\Annotations'    #存储标签的路径，修改为自己的Annotations标签路径
for xml_file in glob.glob(path + '/*.xml'):
    ####### 返回解析树
	tree = ET.parse(xml_file)
	##########获取根节点
	root = tree.getroot()
	#######对所有目标进行解析
	for member in root.findall('object'):
		objectname = member.find('name').text
		if objectname == 'phone':      #原来的标签名字
			print(xml_file)
# 			member.find('name').text = str('suits')    #替换的标签名字
# 			tree.write(xml_file)

"""
===================
根据图片信息改变xml内容
===================
"""
# 源文件夹
# sourceDir = "D:\\data\\cloth&helmet\\dataset\\paperdata_suits&person\\images\\"
# path=r'C:\\Users\\BJM\\Desktop\\auto_label\\addsuits'
# # 结果保存文件夹
# # targetDir = "D:\data\cloth&helmet\dataset\suits&person"
#
#
# for xml_file in glob.glob(path + '/*.xml'):
# 	file = os.path.splitext(xml_file)[0]
# 	xml_name = os.path.join(path, file + '.xml')
# 	# xml_name="{}.xml".format(file)
# 	###### 返回解析树
# 	tree = ET.parse(xml_name)
# 	##########获取根节点
# 	root = tree.getroot()
# 	img_name = os.path.join(path, file + '.jpg')
# 	img = cv2.imread(img_name)
# 	for obj in root.iter('size'):
# 		if obj.find('width').text == '0':
# 			obj.find('width').text = str(img.shape[1])
# 		if obj.find('height').text == '0':
# 			obj.find('height').text = str(img.shape[0])
# 			# print('正在进行resize:' + xml_name)
#
# 		tree.write(xml_name)


