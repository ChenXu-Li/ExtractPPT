import cv2
import numpy as np 
import sys
import os
def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )
def is_rectangle(cnt):#改变了cnt格式!
    cnt_len = cv2.arcLength(cnt, True) #计算轮廓周长
    cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True) #多边形逼近
    # 条件判断逼近边的数量是否为4，轮廓面积是否大于1000，检测轮廓是否为凸的
    if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
        a = cnt.reshape(-1, 2)
        max_cos = np.max([angle_cos( a[i], a[(i+1) % 4], a[(i+2) % 4] ) for i in range(4)])
        # 只检测矩形（cos90° = 0）
        #if max_cos < 0.1:
        # 检测四边形（不限定角度范围）
        if True:
            return True
        else:
            return False
def findone(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#化为灰度
    gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5)))
    ret,thresh_img =cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)#大津算法
    #二值化 有两个返回值 第一个是阈值 第二个是二值化后的图像

    contours, _ = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    maxarea=0
    for cnt in contours:
        
        if cv2.contourArea(cnt) > maxarea and is_rectangle(cnt):#当前最大轮廓面积
            maxarea = cv2.contourArea(cnt) 
            ppt_contour=cnt

    cnt_len = cv2.arcLength(ppt_contour, True) #计算轮廓周长
    ppt_contour = cv2.approxPolyDP(ppt_contour, 0.02*cnt_len, True) #多边形逼近
    
    cv2.drawContours(img, [ppt_contour], -1, (0,0,255), 5)#画轮廓

    i=0
    for p in ppt_contour:    
        ppoint=(p[0][0],p[0][1])
        if i==0:
            cv2.circle(img,ppoint,4,(0,0,0),8)   
        if i==1:
            cv2.circle(img,ppoint,4,(0,255,0),8)  
        if i==2:
            cv2.circle(img,ppoint,4,(255,0,0),8)
        if i==3:
            cv2.circle(img,ppoint,4,(255,255,255),8) 
        i+=1 

    
    
    pts1=np.float32(ppt_contour)
    pts2=np.float32([[0,0],[0,300],[480,300],[480,0]])
    M=cv2.getPerspectiveTransform(pts1,pts2)
    processed = cv2.warpPerspective(img,M,(480, 300))
    cv2.imshow("img", img)
    cv2.imshow("object", processed)
    cv2.waitKey(100)
    return processed

