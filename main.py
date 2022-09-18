from find import *
import sys
import os 
import tkinter as tk
from tkinter import filedialog

def getFileList(dir,Filelist, ext=None):
    """
    获取文件夹及其子文件夹中文件列表
    输入 dir：文件夹根目录
    输入 ext: 扩展名
    返回： 文件路径列表
    """
    newDir = dir
    if os.path.isfile(dir):
        if ext is None:
            Filelist.append(dir)
        else:
            if ext in dir[-3:]:
                Filelist.append(dir)
    
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir=os.path.join(dir,s)
            getFileList(newDir, Filelist, ext)
 
    return Filelist


'''打开选择文件夹对话框'''
root = tk.Tk()
root.withdraw()

Folderpath = filedialog.askdirectory() #获得选择好的文件夹
#Filepath = filedialog.askopenfilename() #获得选择好的文件
filelist=[]
getFileList(Folderpath,filelist, ext=None)
#print(filelist)
os.mkdir(os.path.dirname(Folderpath)+"\\processed")
new_dir=os.path.dirname(Folderpath)+"/processed"
# print(os.path.dirname(Folderpath))
# print(new_dir)
for i in filelist:
    try:
        img = cv2.imread(i)
        if img is None:
            sys.exit("Could not read the image.")
            
        img2=findone(img)
        _,imgname=os.path.split(i)
    
        s=os.path.join(new_dir,imgname)
        # print(s)
        cv2.imwrite(s,img2)
    except :
        pass
    