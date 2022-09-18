# 提取ppt

有时，我们会用手机拍摄课堂上的PPT，但是由于角度，光照等，照片质量不佳，后期回看时很费眼睛。

因此我决定使用opencv对相册中的图片进行批量操作，实现这样的效果：

![image-20220918204046819](http://cdn.lcx-blog.top/img/image-20220918204046819.png)



## 实现逻辑

### 1.阈值化

ppt相对背景来说更加明亮，因此可以通过大津算法提取出来

```python
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)#化为灰度
gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5)))
ret,thresh_img =cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)#大津算法
#二值化 有两个返回值 第一个是阈值 第二个是二值化后的图像
```

![image-20220918201613128](http://cdn.lcx-blog.top/img/image-20220918201613128.png)

### 2.拟合四边形轮廓

寻找多边形轮廓并保存，遍历所有轮廓，如果轮廓为四边形，并且面积大道一定程度即可判断为ppt部分

```python
contours, _ = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for cnt in contours:
    if cv2.contourArea(cnt) < 30000:#轮廓面积
        continue
    peri = cv2.arcLength(cnt, True)#轮廓长度（true:闭合的）
    epsilon = 0.02*peri
    approx = cv2.approxPolyDP(cnt, epsilon, True)#拟合多边形 eplision越小拟合精度越高 返回值为顶点坐标
    cv2.drawContours(img, [approx], -1, (0,0,255), 5)#画轮廓
    #pointlist=approx[0]  
    i=0
    for p in approx:  
        i+=1   
        ppoint=(p[0][0],p[0][1])
        cv2.circle(img,ppoint,4,(0,0,0),8)   
        if i==1:
            cv2.circle(img,ppoint,4,(0,255,0),8)  
        if i==2:
            cv2.circle(img,ppoint,4,(255,0,0),8)
        if i==3:
            cv2.circle(img,ppoint,4,(255,255,255),8) 
```

![image-20220918201841923](http://cdn.lcx-blog.top/img/image-20220918201841923.png)

### 3.仿射变换

已知了四边形的四个角点，就可以将其变为矩形了

![image-20220918202129090](http://cdn.lcx-blog.top/img/image-20220918202129090.png)

对单张图片的处理就完成了，大致逻辑如下：

![image-20220918201407667](http://cdn.lcx-blog.top/img/image-20220918201407667.png)

### 4.批量操作

之后便可以对文件夹中的所有图片依次进行上述操作并保存了，会在相同目录下生成processed文件夹并保存

![image-20220918202627362](http://cdn.lcx-blog.top/img/image-20220918202627362.png)

