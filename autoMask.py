import cv2
import os
from os import getcwd
from xml.etree import ElementTree as ET

#此处设置相关的文件路径，我使用的时人脸检测的模型，所示是face.weights
weightsPath = "./face/face.weights"
configPath = "./face/face.cfg"
labelsPath = "./face/face.names"

#读取names文件中的类别名
LABELS = open(labelsPath).read().strip().split("\n")

#使用opencv加载Darknet模型
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)

#下面是通过检测获取坐标的函数
def coordinate_get(img):
    coordinates_list=[] # 创建坐标列表
    boxes = []
    confidences = []
    classIDs = []
    (H, W) = img.shape[:2]
    # 得到 YOLO需要的输出层
    ln = net.getLayerNames()
    ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    # 从输入图像构造一个blob，然后通过加载的模型，给我们提供边界框和相关概率
    blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layerOutputs = net.forward(ln)

    # 在每层输出上循环
    for output in layerOutputs:
        # 对每个检测进行循环
        for detection in output:
            scores = detection[5:]
            classID = np.argmax(scores)
            confidence = scores[classID]
            # 过滤掉那些置信度较小的检测结果
            if confidence > 0.01:
                # 框后接框的宽度和高度
                box = detection[0:4]  * np.array([W, H, W, H])
                (centerX, centerY, width, height) = box.astype("int")
                # 边框的左上角
                x = int(centerX - (width / 2))
                y = int(centerY - (height / 2))
                # 更新检测出来的框
                boxes.append([x, y, int(width), int(height)])
                confidences.append(float(confidence))
                classIDs.append(classID) 

    idxs = cv2.dnn.NMSBoxes(boxes, confidences, 0.2, 0.3)
    if len(idxs) > 0:
        for i in idxs.flatten():
            (x, y) = (boxes[i][0], boxes[i][1])
            (w, h) = (boxes[i][2], boxes[i][3])

            xmin = int(x)
            ymin = int(y)
            xmax = int(x + w)
            ymax = int(y + h)
            coordinates_list.append([xmin,ymin,xmax,ymax,classIDs[i]])

    return coordinates_list

# 定义一个创建一级分支object的函数
def create_object(root,xi,yi,xa,ya,obj_name):   # 参数依次，树根，xmin，ymin，xmax，ymax
    #创建一级分支object
    _object=ET.SubElement(root,'object')
    #创建二级分支
    name=ET.SubElement(_object,'name')
    print(obj_name)
    name.text= str(obj_name)
    pose=ET.SubElement(_object,'pose')
    pose.text='Unspecified'
    truncated=ET.SubElement(_object,'truncated')
    truncated.text='0'
    difficult=ET.SubElement(_object,'difficult')
    difficult.text='0'
    #创建bndbox
    bndbox=ET.SubElement(_object,'bndbox')
    xmin=ET.SubElement(bndbox,'xmin')
    xmin.text='%s'%xi
    ymin = ET.SubElement(bndbox, 'ymin')
    ymin.text = '%s'%yi
    xmax = ET.SubElement(bndbox, 'xmax')
    xmax.text = '%s'%xa
    ymax = ET.SubElement(bndbox, 'ymax')
    ymax.text = '%s'%ya

# 创建xml文件的函数
def create_tree(image_name, h, w):
    global annotation
    # 创建树根annotation
    annotation = ET.Element('annotation')
    #创建一级分支folder
    folder = ET.SubElement(annotation,'folder')
    #添加folder标签内容
    folder.text=(imgdir)

    #创建一级分支filename
    filename=ET.SubElement(annotation,'filename')
    filename.text=image_name

    #创建一级分支path
    path=ET.SubElement(annotation,'path')

    path.text= getcwd() + '\{}\{}'.format(imgdir,image_name)  # 用于返回当前工作目录
    
    #创建一级分支source
    source=ET.SubElement(annotation,'source')
    #创建source下的二级分支database
    database=ET.SubElement(source,'database')
    database.text='Unknown'

    #创建一级分支size
    size=ET.SubElement(annotation,'size')
    #创建size下的二级分支图像的宽、高及depth
    width=ET.SubElement(size,'width')
    width.text= str(w)
    height=ET.SubElement(size,'height')
    height.text= str(h)
    depth = ET.SubElement(size,'depth')
    depth.text = '3'

    #创建一级分支segmented
    segmented = ET.SubElement(annotation,'segmented')
    segmented.text = '0'


if __name__ == "__main__":
    for image_name in IMAGES_LIST:
        #判断后缀只处理jpg文件
        if image_name.endswith('jpg'):
            image = cv2.imread(os.path.join(imgdir, image_name))
            coordinates_list = coordinate_get(image)
            (h, w) = image.shape[:2]
            create_tree(image_name, h, w)

            for coordinate in coordinates_list:
                label_id = coordinate[4]
                create_object(annotation, coordinate[0], coordinate[1], coordinate[2], coordinate[3], LABELS[label_id])
                # if coordinates_list==[]:
                #     break

            # 将树模型写入xml文件
            tree = ET.ElementTree(annotation)       
            tree.write('.\{}\{}.xml'.format(imgdir, image_name.strip('.jpg')))
