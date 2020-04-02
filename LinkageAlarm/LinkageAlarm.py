#!/usr/bin/python3
# coding=utf-8

import sys
import numpy as np
import cv2
import os
import time
from PIL import Image

from email.header import Header
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
import smtplib

faceCascadeFile = '/usr/local/lib/python3.7/site-packages/cv2/data/haarcascade_frontalface_default.xml'
ymlfile = 'face.yml'
faceminbox = 100

smtpserver = 'smtp.139.com'
password = '2387802_wz'

def FormatAddr(s):
    name, addr = parseaddr(s)
    print(name, addr)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def SendEmail(PicName):
    from_addr = '13637289392@139.com'
    to_addr = '570318039@qq.com'
    cc_addr = '1132427047@qq.com'
    recv_addr = [to_addr]
    #recv_addr = [to_addr] + [cc_addr]

    message = MIMEMultipart('related')
    message['From'] = FormatAddr("家庭监控报警器 <13637289392@139.com>")
    message['To'] = FormatAddr("男主 <570318039@qq.com>")
    #message['Cc'] = FormatAddr("女主 <1132427047@qq.com>")
    subject = '家庭监控报警'
    message['Subject'] = Header(subject, 'utf-8')

    msgAlternative = MIMEMultipart('alternative')
    message.attach(msgAlternative)
 
    mail_msg = """
    <p>发生报警</p>
    <p><img src="cid:image1"></p>
    """
    msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))

    fp = open(PicName, 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    msgImage.add_header('Content-ID', '<image1>')
    message.attach(msgImage)

    server = smtplib.SMTP(smtpserver, 25)
    #server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, recv_addr, message.as_string())

def FaceDetect(FaceCascade, Img):
    #转换成灰度图像
    gray = cv2.cvtColor(Img, cv2.COLOR_BGR2GRAY)
                
    #人脸检测
    faces = FaceCascade.detectMultiScale(
            gray,     
            scaleFactor = 1.2,
            minNeighbors = 5,     
            minSize = (faceminbox, faceminbox)
    )
    
    if len(faces) <= 0:
        #if os.path.exists(ymlfile) == True:
            #os.remove(ymlfile);
        return -1
    
    i = 0
    ids = []
    faceSamples = []
    addyml = False
    fileexist = False

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    if os.path.exists(ymlfile) == True:
        fileexist = True

    #画矩形
    for (x, y, w, h) in faces:
        #print("x: %d, y: %d, w: %d, h: %d" % (x, y, w, h))
        cv2.rectangle(Img, (x, y), (x+w, y+h), (0, 0, 255), 2)
        
        add = True
        if fileexist == True:
            recognizer.read(ymlfile)
            idnum, confidence = recognizer.predict(gray[y: y + h, x: x + w])
            if confidence < 100:
                add = False
            else:
                print("confidence: %d" % round(100 - confidence))
        
        if add == True:
            print("add new feat")
            imgnumpy = np.array(gray, 'uint8')
            faceSamples.append(gray[y: y + h, x: x + w])
            ids.append(i)
            
            i += 1
            addyml = True

    if addyml == True:
        recognizer.train(faceSamples, np.array(ids))
        recognizer.write(ymlfile)
    
        snaptime = time.strftime("%04Y%02m%02d_%02H%02M%02S", time.localtime(time.time()))
        picname = '%s.jpg' % snaptime
        cv2.imwrite(picname, Img)

        #SendEmail(picname)

def SelectMode(Mode, File):
    #人脸识别分类器
    faceCascade = cv2.CascadeClassifier(faceCascadeFile)

    #启用前删掉之前的人脸特征文件
    if os.path.exists(ymlfile) == True:
        os.remove(ymlfile);

    #周期检测
    count = 1

    if Mode == 0:
        img = cv2.imread(File, 1)
        FaceDetect(faceCascade, img)
    elif Mode == 1:
        cap = cv2.VideoCapture(File)  
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        while (1):
            success, frame = cap.read()
            if not success:
                break

            if count >= fps:
                count = 1
                FaceDetect(faceCascade, frame)
            else:
                count += 1
 
            cv2.waitKey(25) #延迟
        cap.release()
    else:
        cap = cv2.VideoCapture(0)
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        while cap.isOpened():
            ok, img = cap.read()
            if not ok:            
                break

            if count >= fps:
                count = 1
                FaceDetect(faceCascade, img)
            else:
                count += 1

        print("Read frame from cap fail!")
        cap.release()

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1].find('.jpg') != -1:
            SelectMode(0, sys.argv[1])
        elif sys.argv[1].find('.mp4') != -1:
            SelectMode(1, sys.argv[1])
        else:
            print("参数异常，请输入图片")
            sys.exit()
    else:
        SelectMode(2, "")
