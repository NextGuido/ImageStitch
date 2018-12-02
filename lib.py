import cv2
import os
import shutil
import numpy as np
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import globalvar as gl
def newIcon(icon):
    return QIcon('./icon/' + icon+'.png')
def newAction(parent,text,slot=None,shortcut=None,icon=None,
              tip=None,statustip=None,checkable=False,enabled=True):
    a = QAction(text, parent)
    if icon is not None:
        a.setIcon(newIcon(icon))
    if shortcut is not None:
        if isinstance(shortcut, (list, tuple)):
            a.setShortcuts(shortcut)
        else:
            a.setShortcut(shortcut)
    if tip is not None:
        a.setToolTip(tip)
        a.setStatusTip(tip)
    if statustip is not None:
        a.setStatusTip(statustip)
    if slot is not None:
        a.triggered.connect(slot)
    if checkable:
        a.setCheckable(True)
    a.setEnabled(enabled)
    return a
def addActions(widget, actions):
    for action in actions:
        if action is None:
            widget.addSeparator()
        elif isinstance(action, QMenu):
            widget.addMenu(action)
        else:
            widget.addAction(action)
def newWidgetAction(parent,widget):
    action=QWidgetAction(parent)
    action.setDefaultWidget(widget)
    return action
def read(filename,default=None):
    try:
        with open(filename,'rb')as f:
            return f.read()
    except:
        return default
class saveThread(QThread):
    def __init__(self,scene,filename):
        super(saveThread, self).__init__()
        self.scene = scene
        self.filename=filename
        self.ext=os.path.basename(self.filename).split('.')[-1]
        tmpDataPath=gl.get_value('temp')
        self.tmp_dir = tmpDataPath+'/imageStitchtmp'
        print(self.tmp_dir)
        self.tmp_img_base =os.path.join(self.tmp_dir, os.path.basename(self.filename).split('.')[0])
        # x=self.scene.sceneRect().x()
        # y=self.scene.sceneRect().y()
        w = int(scene.itemsBoundingRect().width()-1)#减去1px的边界宽度
        h = int(self.scene.itemsBoundingRect().height() - 1)
        self.image =np.zeros((h,w), dtype=np.uint8)
    def run(self):
        rect=self.scene.sceneRect()
        x = rect.x()+0.5
        y = rect.y()+0.5
        w = rect.width() - 1
        h = rect.height() - 1
        p=QPainter()
        images=[]
        tmp_w=20000
        sum=int(w/tmp_w)
        i=0
        while i<sum:
            image=QImage(tmp_w,h,QImage.Format_RGB32)
            p.begin(image)
            self.scene.render(p,target=QRectF(0,0,tmp_w,h),source=QRectF(x+i*tmp_w,y,tmp_w,h))
            p.end()
            print(x+i*tmp_w)
            images.append(image)
            i+=1
        print(w,h,w-sum*tmp_w)
        image=QImage(w-sum*tmp_w,h,QImage.Format_RGB32)
        p.begin(image)
        self.scene.render(p,target=QRectF(0,0,w-sum*tmp_w,h),source=QRectF(x+sum*tmp_w,y,w-sum*tmp_w,h))
        p.end()
        images.append(image)
        if not os.path.exists(self.tmp_dir):
            os.mkdir(self.tmp_dir)
        for i,img in enumerate(images):
            img.save(self.tmp_img_base+str(i)+'.jpg')
        for i in range(len(images)):
            print(self.tmp_img_base + str(i) + '.jpg')
            name=self.tmp_img_base+str(i)+'.jpg'
            image=cv2.imdecode(np.fromfile(name, dtype=np.uint8), 0)
            print(i*tmp_w+image.shape[1])
            self.image[0:image.shape[0],i*tmp_w:i*tmp_w+image.shape[1]]=image
        shutil.rmtree(self.tmp_dir)
        cv2.imencode('.png',self.image)[1].tofile(self.filename)
        print(self.filename+' saved')