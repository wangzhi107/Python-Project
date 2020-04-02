#!/usr/bin/python3
# coding==utf-8

import sys
import numpy as np
import cv2
import os
from PIL import Image, ImageDraw, ImageFont

faceCascadeFile = '/usr/local/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_default.xml'
eyeCascadeFile = '/usr/local/lib/python3.7/site-packages/cv2/data/haarcascade_eye.xml'

dataPath = "./Facedata"
trainerPath = "./Facetrainer"
trainerFile = "./Facetrainer/trainer.yml"
nameFile = "./Facetrainer/trainer_name.txt"

def faceDataCollect(picPath):
    face_detector = cv2.CascadeClassifier(faceCascadeFile)
    if os.path.exists(dataPath) == False:
        os.mkdir(dataPath)

    imagePath = [os.path.join(picPath, f) for f in os.listdir(picPath)]
    for imageFile in imagePath:
        img = cv2.imread(imageFile)
        
        #转为灰度图片
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #检测人脸
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + w), (255, 0, 0))
            #保存图像
            fileName = imageFile.split("/")[-1]
            cv2.imwrite("./Facedata/" + fileName, gray[y: y + h, x: x + w])
 
    cv2.destroyAllWindows()

def faceTraining():
    if os.path.isdir(dataPath) == False:
        return -1;
    
    if os.path.exists(trainerPath) == False:
        os.mkdir(trainerPath)
    if os.path.exists(trainerFile) == False:
        os.mknod(trainerFile)

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(faceCascadeFile)

    faceSamples = []
    ids = []
    f = open(nameFile, 'w+', encoding = 'utf-8')

    count = 0
    imagePaths = [os.path.join(dataPath, f) for f in os.listdir(dataPath)]
    for imagePath in imagePaths:
        jpgFile = imagePath.split("/")[-1]
        fileName = jpgFile.split(".")[0]
        idNum = int(fileName.split("_")[-1])
        
        if count == 0:
            count = 1
        else:
            f.write('_')
        f.write(fileName.split("_")[0])
        
        PIL_img = Image.open(imagePath).convert('L')   # convert it to grayscale
        img_numpy = np.array(PIL_img, 'uint8')
        faces = detector.detectMultiScale(img_numpy)
        for (x, y, w, h) in faces:
            faceSamples.append(img_numpy[y:y + h, x: x + w])
            ids.append(idNum)                                                                
    
    f.close()
    recognizer.train(faceSamples, np.array(ids))
    recognizer.write(trainerFile)

def faceRecognition(recogePic):
    if (os.path.isfile(trainerFile) == False) or (os.path.isfile(nameFile) == False):
        return -1;

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(trainerFile)
    faceCascade = cv2.CascadeClassifier(faceCascadeFile)
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    idnum = 0
    f = open(nameFile, 'r+', encoding = 'utf-8')
    nameData = f.read()
    names = nameData.split("_")
    print(names)

    while True:
        img = cv2.imread(recogePic)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor = 1.2,
                minNeighbors = 5,
                minSize = (32, 32)
        )
                                                    
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            idnum, confidence = recognizer.predict(gray[y: y + h, x: x + w])
                                
            if confidence < 100:
                idnum = names[idnum]
                confidence = "{0}%".format(round(100 - confidence))
            else:
                idnum = "unknown"
                confidence = "{0}%".format(round(100 - confidence))
    
        cv2img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pilimg = Image.fromarray(cv2img)
        draw = ImageDraw.Draw(pilimg)
        font = ImageFont.truetype("simsun.ttf", 20, encoding="utf-8")  # 参数1：字体文件路径，参数2：字体大小
        draw.text((x + 5, y - 5), str(idnum), (255, 0, 0), font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体 
        draw.text((x + 5, y + h - 5), str(confidence), (0, 0, 0), font=font)  # 参数1：打印坐标，参数2：文本，参数3：字体颜色，参数4：字体 
        cv2charimg = cv2.cvtColor(np.array(pilimg), cv2.COLOR_RGB2BGR)
                                                                                                                
        cv2.namedWindow('camera')
        cv2.imshow('camera', cv2charimg)
        k = cv2.waitKey(10)
        if k == 27:
            break
    
    f.close()
    cv2.destroyAllWindows()

def faceDetect(picFile):
    #人脸识别分类器
    faceCascade = cv2.CascadeClassifier(faceCascadeFile)
    #识别眼睛的分类器
    eyeCascade = cv2.CascadeClassifier(eyeCascadeFile)

    img = cv2.imread(picFile, 1)
    #转换成灰度图像
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                
    #人脸检测
    faces = faceCascade.detectMultiScale(
            gray,     
            scaleFactor = 1.2,
            minNeighbors = 5,     
            minSize = (32, 32)
    )
                        
    #在检测人脸的基础上检测眼睛
    for (x, y, w, h) in faces:
        fac_gray = gray[y: (y+h), x: (x+w)]
        result = []
        eyes = eyeCascade.detectMultiScale(fac_gray, 1.3, 2)
        
        #眼睛坐标的换算，将相对位置换成绝对位置
        for (ex, ey, ew, eh) in eyes:
            result.append((x+ex, y+ey, ew, eh))
                                                                                   
    #画矩形
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    for (ex, ey, ew, eh) in result:
        cv2.rectangle(img, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

    cv2.namedWindow('image')
    key = 0
    while key != 27: 
        cv2.imshow('image', img)
        key = cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("参数个数出错!")
        sys.exit()
    else:
        mode = int(sys.argv[1])
        if mode == 1:
            #检测展示模式
            if len(sys.argv) != 3:
                print("参数个数出错!")
                sys.exit()
            if sys.argv[2].find('.jpg') != -1:
                faceDetect(sys.argv[2])
        elif mode == 2:
            #检测提取模式
            if len(sys.argv) != 3:
                print("参数个数出错!")
                sys.exit()
            faceDataCollect(sys.argv[2])
        elif mode == 3:
            #数据训练模式
            faceTraining()
        else:
            #人脸比对模式
            if len(sys.argv) != 3:
                print("参数个数出错!")
                sys.exit()
            if sys.argv[2].find('.jpg') != -1:
                faceRecognition(sys.argv[2])
