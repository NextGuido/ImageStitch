import sys
from PyQt5.QtCore import QThread,pyqtBoundSignal
from PyQt5.QtWidgets import  *
from PyQt5.QtGui import  *
from PyQt5.QtCore import *
from myui import *
from myui2 import *
from login import *
from Stitcher import Stitcher
import cv2
import time
import glob
import os
import numpy as np
from manual import ManualForm
from myconfig import *

class Stitch(Stitcher):
    # 重写部分功能
    def __init__(self):
        super(Stitch).__init__()

    def resize(self, img, resize_x, resize_y):
        # 对图像进行缩放
        (h, w) = img.shape
        resizeH = int(h * resize_y)
        resizeW = int(w * resize_x)
        return cv2.resize(img, (resizeW, resizeH), interpolation=cv2.INTER_AREA)
    def flowStitch(self, fileList, caculateOffsetMethod):
        # 此部分重写没有改变原有的功能和结构，只在一些位置插入发射信号语句（emit），用来与界面通信
        self.printAndWrite("Stitching the directory which have " + str(fileList[0]))
        fileNum = len(fileList)
        offsetList = []
        describtion = ""
        # calculating the offset for small image
        startTime = time.time()
        status = True
        endfileIndex = 0
        thread.sig_s.emit()
        thread.sleep(1)
        for fileIndex in range(0, fileNum - 1):
            # newForm.setVal()
            thread.sig_s.emit()
            # print(fileIndex)
            self.msg = fileIndex
            self.printAndWrite("stitching " + str(fileList[fileIndex]) + " and " + str(fileList[fileIndex + 1]))

            # imageA = cv2.imread(fileList[fileIndex], 0)
            # imageB = cv2.imread(fileList[fileIndex + 1], 0)
            imageA = cv2.imdecode(np.fromfile(fileList[fileIndex],dtype=np.uint8),cv2.IMREAD_GRAYSCALE)
            imageB = cv2.imdecode(np.fromfile(fileList[fileIndex+1],dtype=np.uint8),cv2.IMREAD_GRAYSCALE)

            # if caculateOffsetMethod == self.calculateOffsetForPhaseCorrleate:
            #     (status, offset) = self.calculateOffsetForPhaseCorrleate(
            #         [fileList[fileIndex], fileList[fileIndex + 1]])
            # else:
            (status, offset) = caculateOffsetMethod([imageA, imageB])

            if status == False:
                describtion = "  " + str(fileList[fileIndex]) + " and " + str(
                    fileList[fileIndex + 1]) + " can not be stitched"
                break
            else:
                offsetList.append(offset)
                endfileIndex = fileIndex + 1
        endTime = time.time()

        self.printAndWrite("The time of registering is " + str(endTime - startTime) + "s")
        self.printAndWrite("  The offsetList is " + str(offsetList))

        # stitching and fusing
        self.printAndWrite("start stitching")
        startTime = time.time()
        dxSum = 0
        dySum = 0
        #stitchImage = cv2.imread(fileList[0], 0)
        stitchImage = cv2.imdecode(np.fromfile(fileList[0],dtype=np.uint8),cv2.IMREAD_GRAYSCALE)
        offsetListNum = len(offsetList)
        thread.sig_m.emit((str(fileList[0]), 0,0))
        for fileIndex in range(0, offsetListNum):
            str1="  stitching " + str(fileList[fileIndex + 1])
            # newForm.addLog(str1)
            thread.sig_l.emit(str1)
            self.printAndWrite("  stitching " + str(fileList[fileIndex + 1]))
            # imageB = cv2.imread(fileList[fileIndex + 1], 0)
            imageB =cv2.imdecode(np.fromfile(fileList[fileIndex + 1], dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
            dxSum = offsetList[fileIndex][0] + dxSum
            dySum = offsetList[fileIndex][1] + dySum
            offset = [dxSum, dySum]
            str2="  The offsetX is " + str(offsetList[fileIndex][0]) + " and the offsetY is " + str(
                offsetList[fileIndex][1])
            # newForm.addLog(str2)
            thread.sig_l.emit(str2)
            self.printAndWrite("  The offsetX is " + str(offsetList[fileIndex][0]) + " and the offsetY is " + str(
                offsetList[fileIndex][1]))
            str3="  The dxSum is " + str(dxSum) + " and the dySum is " + str(dySum)
            # newForm.addLog(str3)
            thread.sig_l.emit(str3)
            self.printAndWrite("  The dxSum is " + str(dxSum) + " and the dySum is " + str(dySum))
            (stitchImage, fuseRegion, roiImageRegionA, roiImageRegionB) = self.getStitchByOffset(
                [stitchImage, imageB], offset)
            thread.sig_m.emit((str(fileList[fileIndex + 1]),offsetList[fileIndex][1],offsetList[fileIndex][0]))
            if dxSum < 0:
                dxSum = 0
            if dySum < 0:
                dySum = 0

        endTime = time.time()

        self.printAndWrite("The time of fusing is " + str(endTime - startTime) + "s")

        if status == False:
            self.printAndWrite(describtion)
            str4 = "拼接出错！\n" + describtion

        else:
            str4="拼接成功！"
        thread.sig_r.emit(str4)
        return ((status, endfileIndex), stitchImage)

    def imageSetStitchWithMutiple(self, imgresize, imgresize_x, imgresize_y, projectAddress, outputAddress, fileName,
                       caculateOffsetMethod,startNum=1, fileExtension="jpg", outputfileExtension="jpg"):
        # 对图像拼接进行了较大改动，首先加入了图像缩放的变量和相应代码，然后修改部分代码使拼接功能由对多个文件夹
        # 进行拼接变为对单个目录下的图像进行拼接

        if imgresize:
            # 以下代码为将图像进行缩放并放入cache目录下，将cache作为输入进行拼接
            if not os.path.exists("./cache"):
                os.makedirs("./cache")
            for i in os.listdir("./cache"):
                path_file = os.path.join("./cache", i)
                os.remove(path_file)
            fileList = glob.glob(projectAddress + "\\" + "*." + fileExtension)
            fileNum = len(fileList)
            for j in range(0, fileNum):
                Name = fileList[j].split("\\")[-1]
                tmpfileExtension=Name.split('.')[-1]
                #img = cv2.imread(fileList[j], 0)
                img=cv2.imdecode(np.fromfile(fileList[j],dtype=np.uint8),cv2.IMREAD_GRAYSCALE)
                imgResized = self.resize(img, imgresize_x, imgresize_y)
                # cv2.imwrite("./cache/" + Name, imgResized)
                cv2.imencode("." + tmpfileExtension, imgResized)[1].tofile("./cache/" + Name)
            projectAddress = "./cache"
        fileAddress = projectAddress + "/"

        # + str(i) + "/"
        fileList = glob.glob(fileAddress + "*." + fileExtension)
        if not os.path.exists(outputAddress):
            os.makedirs(outputAddress)
        Stitcher.outputAddress = outputAddress
        result = self.flowStitchWithMutiple(fileList, caculateOffsetMethod)
        self.tempImageFeature.isBreak = True
        if len(result) == 1:
            # cv2.imwrite(outputAddress + "/" + fileName + "." + outputfileExtension, result[0])
            name=fileName + "."+outputfileExtension
            cv2.imencode("."+outputfileExtension, result[0])[1].tofile(outputAddress + "/" + name)
        else:
            for j in range(0, len(result)):
                # cv2.imwrite(
                #     (outputAddress + "/" + fileName + "_" + str(j + 1) + "." + outputfileExtension,
                #     result[j]))
                name=fileName + "_" + str(j + 1) + "." + outputfileExtension
                path=os.path.join(outputAddress,name)
                # #放在cache目录下
                # path = os.path.join('./cache', name)
                print(path)
                cv2.imencode('.'+outputfileExtension, result[j])[1].tofile(path)
            thread.sig_a.emit()

class stitcherThread(QThread):
    # 图像拼接线程
    projectAddress = "./images"
    outputAddress = "./result"
    fileNum = 0
    fileName = "result"
    method="calculateOffsetForFeatureSearch"
    imgresize = False
    imgresize_x = 1.00
    imgresize_y = 1.00
    fileExtension="jpg"
    outputfileExtension="jpg"
    sig_s=pyqtSignal()
    sig_l=pyqtSignal(str)
    sig_r=pyqtSignal(str)
    sig_e=pyqtSignal()
    #for manualAct
    sig_m=pyqtSignal(tuple)
    sig_a = pyqtSignal()
    def __init__(self):
        super(QThread,self).__init__()

    def setVal(self,msg):
        # 设定拼接参数并进行拼接
        self.imgresize = msg['imgresize']
        self.imgresize_x= msg['imgresize_x']
        self.imgresize_y = msg['imgresize_y']
        self.projectAddress = msg['projectAddress']
        self.outputAddress = msg['outputAddress']
        self.fileName = msg['fileName']
        self.method = msg['method']
        self.outputfileExtension = msg['outputfileExtension']
        self.fileExtension=msg['fileExtension']
        self.start()
    def run(self):
        # 开始拼接
        stitcher = Stitch()

        if self.method=="calculateOffsetForFeatureSearch":
            stitcher.imageSetStitchWithMutiple(self.imgresize, self.imgresize_x, self.imgresize_y,
                                    self.projectAddress, self.outputAddress, self.fileName,
                                    stitcher.calculateOffsetForFeatureSearch, startNum=1,
                                    fileExtension=self.fileExtension, outputfileExtension=self.outputfileExtension)
        elif self.method=="calculateOffsetForFeatureSearchIncre":
            stitcher.imageSetStitchWithMutiple(self.imgresize, self.imgresize_x, self.imgresize_y,
                                    self.projectAddress, self.outputAddress, self.fileName,
                                    stitcher.calculateOffsetForFeatureSearchIncre,startNum=1,
                                    fileExtension=self.fileExtension, outputfileExtension=self.outputfileExtension)
        self.sig_e.emit()

# class LoginWindow(QDialog,Ui_Login):
#     # 登录界面
#     superPassword = "afish1001"
#     def __init__(self,parent=None):
#         super(QDialog,self).__init__(parent)
#         self.setupUi(self)
#         reg = QRegExp("[a-zA-Z0-9_]+$")
#         pValidator = QRegExpValidator()
#         pValidator.setRegExp(reg)
#         self.lineEdit_password.setValidator(pValidator)
#         self.lineEdit_password.setEchoMode(QLineEdit.Password)
#         self.bt_yes.clicked.connect(self.login)
#         self.setWindowIcon(QIcon('./icon/icon.png'))
#     def login(self):
#         con=myconfig()
#         text=self.lineEdit_password.text()
#         if text == self.superPassword or con.matchPassword(text):
#             self.lineEdit_password.clear()
#             self.close()
#             form.show()
#         else:
#             self.lineEdit_password.clear()
#             warning = QMessageBox.warning(self, "错误！", "密码错误，请重新输入！")

class DialogWindow(QDialog,Ui_Dialog):
    # 拼接过程展示界面
    fileList=[]
    val=0
    def __init__(self,parent=None):
        super(QDialog,self).__init__(parent)
        self.setupUi(self)
        self.bt_backMainWindow.clicked.connect(self.back)
        self.bt_openResult.setEnabled(False)
        self.bt_backMainWindow.setEnabled(False)
        self.bt_manualAct.clicked.connect(self.startManualAct)
        self.bt_openResult.clicked.connect(form.printResult)
        self.setWindowIcon(QIcon('./icon/icon.png'))
        thread.sig_s.connect(self.setVal)
        thread.sig_l.connect(self.addLog)
        thread.sig_r.connect(self.setStitcherResult)
        thread.sig_e.connect(self.setEnd)
        thread.sig_m.connect(self.getManualFiles)
        thread.sig_a.connect(self.startManualAct)
    def getManualFiles(self,fileinfo):
        self.fileList.append(fileinfo)
    def startManualAct(self):
        if self.fileList:
            manualActForm.addImages(self.fileList)
            manualActForm.show()
    def back(self):
        # 将界面初始化并返回主界面
        self.list_stitcherlog.clear()
        self.list_result.clear()
        self.progressBar.setValue(0)
        self.fileList.clear()
        thread.quit()
        self.close()
        form.show()
    def setStart(self,fileNum):
        # 初始化
        # print(fileNum)
        self.bt_backMainWindow.setEnabled(False)
        self.bt_openResult.setEnabled(False)
        self.bt_manualAct.setEnabled(False)
        self.progressBar.setMaximum(fileNum)
        self.progressBar.setValue(0)
        self.val=0
        self.lb_stitchInf.setText("准备开始拼接！")
    def setVal(self):
        # 显示拼接进度和进度条
        self.val+=1
        self.progressBar.setValue(self.val)
        string = "正在拼接第" + str(self.val-1) + "张图片与第" + str(self.val) + "张图片"
        self.lb_stitchInf.setText(string)

    def setEnd(self):
        # 显示拼接完成
        self.lb_stitchInf.setText("拼接完成！")
        self.bt_openResult.setEnabled(True)
        self.bt_backMainWindow.setEnabled(True)
        self.bt_manualAct.setEnabled(True)
    def addLog(self,str):
        # 输出日志
        self.list_stitcherlog.addItem(str)
    def setStitcherResult(self,str):
        # 输出拼接结果
        self.list_result.addItem(str)

class MainWindow(QMainWindow,Ui_MainWindow ):
    projectAddress = "./images"
    outputAddress = "./result"
    method="calculateOffsetForFeatureSearch"
    fileNum = 0
    fileName="result"
    imgresize = False
    imgresize_x = 1.00
    imgresize_y = 1.00
    fileExtension = "jpg"
    outputfileExtension="jpg"
    superPassword="afish1001"
    manualForms=[]
    def __init__(self,parent=None ):
        super (MainWindow ,self ).__init__(parent )
        self .setupUi(self)
        # 设置界面控件参数，将控件和功能连接起来
        self.cbBox_mode.currentIndexChanged.connect(self.modeSet)
        self.bt_addMode.clicked.connect(self.addMode)
        self.checkBox_resize.stateChanged.connect(self.imgResize)
        self.dsBox_resize_x.valueChanged.connect(self.imgResize_x)
        self.dsBox_resize_y.valueChanged.connect(self.imgResize_y)
        self.cbBox_featureMethod.currentIndexChanged.connect(self.cbox_featureMethod)
        self.dsBox_searchRatio.valueChanged.connect(self.dbox_searchRatio)
        self.cbBox_offsetCaculate .currentIndexChanged.connect(self.cbox_offsetCaculate)
        self.dsBox_offsetEvaluate.valueChanged.connect(self.dbox_offsetEvaluate)
        self.cbBox_direction.currentIndexChanged.connect(self.cbox_direction)
        self.cbBox_method.currentIndexChanged.connect(self.cbox_method)
        self.cbBox_fusion.currentIndexChanged.connect(self.cbox_fusion)
        self.cbBox_extension.currentIndexChanged.connect(self.cbox_extension)
        self.bt_input.clicked.connect(self.input)
        self.bt_output.clicked.connect(self.output)
        self.lineEdit_fileName.setPlaceholderText("输入文件名，默认为：文件夹—pin")
        self.lineEdit_output.setPlaceholderText("默认为导入的上级目录！")
        reg=QRegExp("[a-zA-Z0-9_]+$")
        pValidator=QRegExpValidator()
        pValidator.setRegExp(reg)
        self.lineEdit_fileName.setValidator(pValidator)
        self.lineEdit_fileName.textChanged.connect(self.editFileName)
        self.bt_startStitch.clicked.connect(self.startStitch)

        self.bt_editMode .clicked.connect(self.editMode)

        self.bt_save.clicked.connect(self.saveMode)
        self.bt_del.clicked.connect(self.delMode)
        self.list_input.itemClicked.connect(self.inputPic)
        self.list_input.setAlternatingRowColors(True)
        self.lb_icon  .setPixmap(QPixmap ("./icon/icon.png").scaledToHeight(119))
        self.start()
        self.setWindowIcon(QIcon('./icon/icon.png'))

        # self.action_logout.triggered.connect(self.logout)
        # self.action_resetPassword.triggered.connect(self.resetPassword)
        # self.action_removePassword.triggered.connect(self.removePassword)
        self.action_manual.triggered.connect(self.manualAct)
        self.groupBox_setting.setEnabled(False)
        self.bt_editMode.setEnabled(False)

    def start(self):
        # 初始化界面
        self.bt_startStitch.setEnabled(False)
        self.cbBox_mode.clear()
        self.cbBox_mode.addItem("默认")
        if not os.path.exists("./config"):
            os.makedirs("./config")
        # if not os.path.exists("./user.ini"):
        #     f=open("./user.ini","w")
        #     f.close()
        for fn in os.listdir("./config/"):
            self.cbBox_mode.addItem(fn)

        self.modeSet()
    def manualAct(self):
        manualForm=ManualForm(self.projectAddress)
        self.manualForms.append(manualForm)
        # files=[]
        # for i in range(self.fileNum):
        #     files.append(os.path.join(self.projectAddress,self.list_input.item(i).text()))
        #     print(os.path.join(self.projectAddress,self.list_input.item(i).text()))
        # manualForm.addImages(files)
        manualForm.show()
    # def logout(self):
    #     # 退出登录
    #     self.close()
    #     loginForm.show()
    # def resetPassword(self):
    #     # 重置密码
    #     con = myconfig()
    #     qd = QInputDialog()
    #
    #     text, ok = qd.getText(self, "请输入密码", "请输入原密码：")
    #     if ok:
    #         if text == self.superPassword or con.matchPassword(text):
    #             text, ok = qd.getText(self, "请输入密码", "请输入新密码：")
    #             if ok:
    #                 con.setPassword(text)
    #         else:
    #             warning = QMessageBox.warning(self, "错误！", "密码错误，请重新输入！")
    #             self.resetPassword()
    # def removePassword(self):
    #     # 删除密码
    #     con = myconfig()
    #     qd = QInputDialog()
    #
    #     text, ok = qd.getText(self, "请输入密码", "请输入密码：")
    #     if ok:
    #         if text == self.superPassword or con.matchPassword(text):
    #             con.delPassword()
    #         else:
    #             warning = QMessageBox.warning(self, "错误！", "密码错误，请重新输入！")
    #             self.removePassword()
    def input(self):
        # 选择输入图像文件夹
        self.fileNum=0
        dlg= QFileDialog()
        dlg.setFileMode(QFileDialog.Directory )
        self.projectAddress = dlg.getExistingDirectory()
        self.list_input.clear()
        start=False
        # 将文件名显示在文件列表框里
        if os.path.exists(self.projectAddress):
            # self.outputAddress=os.path.abspath(os.path.dirname(self.projectAddress))
            self.outputAddress = os.path.abspath(self.projectAddress)
            self.lineEdit_output.setText(self.outputAddress)
            self.fileName=self.projectAddress.split("/")[-1]+"-pin"
            self.lineEdit_fileName.setText(self.fileName)
            for fn in os.listdir(self.projectAddress):
                if self.isImage(fn):
                    self.list_input .addItem(fn)
                    self.fileNum+=1
                    start=True
                    self.fileExtension=fn.split(".")[-1]
            self.bt_startStitch.setEnabled(start)
            # print(self.fileNum)
        else:
            self.lineEdit_output.clear()
            self.lineEdit_fileName.clear()
            self.bt_startStitch.setEnabled(False)
    def isImage(self,file):
        # 判定文件是否为图像
        image=["jpg","Jpg","jpeg","bmp","tif","tiff","png"]
        fileExtension=file.split(".")[-1]
        if fileExtension in image :
            return True
        else:
            return False
    def inputPic(self,item):
        # 点击列表中文件名打开图像功能
        n=self.list_input.currentRow()
        os.startfile(self.projectAddress+"/"+item.text())
    def output(self):
        # 设置图像输出位置
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.Directory)
        self.outputAddress = dlg.getExistingDirectory()
        self.lineEdit_output.setText(self.outputAddress)
    def cbox_extension(self):
        # 设置输出文件扩展名
        self.outputfileExtension=self.cbBox_extension.currentText()
    def editFileName(self):
        # 设置输出结果文件名
        self.fileName=self.lineEdit_fileName.text()
        if self.fileName=="":
            self.fileName="result"
    def startStitch(self):
        # 开始拼接
        newForm.setStart(self.fileNum)
        msg={}
        msg['imgresize']=self.imgresize
        msg['imgresize_x']=self.imgresize_x
        msg['imgresize_y'] = self.imgresize_y
        msg['projectAddress']=self.projectAddress
        msg['outputAddress'] =self.outputAddress
        msg['fileName'] =self.fileName
        msg['method'] =self.method
        msg['outputfileExtension'] =self.outputfileExtension
        msg['fileExtension']=self.fileExtension
        thread.setVal(msg)
        form.hide()
        newForm.show()
        newForm.exec_()
    def applySetting(self):
        # 参数设定
        self.cbox_featureMethod()
        self.dbox_searchRatio()
        self.cbox_offsetCaculate()
        self.dbox_offsetEvaluate()
        self.cbox_direction()
        self.cbox_method()
        self.cbox_fusion()
        self.imgResize()
        self.imgResize_x()
        self.imgResize_y()
    def modeSet(self):
        # 读取模式的配置文件并应用
        modeName=self.cbBox_mode.currentText()
        con=myconfig()
        mode={}
        if modeName=="默认":
            self.bt_editMode.setEnabled(False)
            mode= con.setDefault()
        else:
            self.bt_editMode.setEnabled(True)
            mode = con.read(modeName)
        self.checkBox_resize.setChecked(mode['imgresize']==str("True"))
        self.dsBox_resize_x.setValue(float(mode['imgresize_x']))
        self.dsBox_resize_y.setValue(float(mode['imgresize_y']))
        self.cbBox_featureMethod.setCurrentText(mode['featureMethod'])
        self.dsBox_searchRatio.setValue(float(mode['searchRatio']))
        self.cbBox_offsetCaculate.setCurrentText(mode['offsetEvaluate'])
        self.dsBox_offsetEvaluate.setValue(float(mode['offsetEvaluate']))
        self.cbBox_direction.setCurrentText(mode['direction'])
        self.cbBox_method.setCurrentText(mode['method'])
        self.cbBox_fusion.setCurrentText(mode['fusion'])
        self.applySetting()
    def addMode(self):
        # 添加新模式
        mode={}
        text,ok= QInputDialog.getText(self,'创建新的模式','请输入名称')
        if ok:
            self.cbBox_mode.addItem(text)
            mode['imgresize']=str(self.checkBox_resize.isChecked())
            mode['imgresize_x']=self.dsBox_resize_x.text()
            mode['imgresize_y']=self.dsBox_resize_y.text()
            mode['featureMethod']=self.cbBox_featureMethod.currentText()
            mode['searchRatio']=self.dsBox_searchRatio.text()
            mode['offsetCaculate']=self.cbBox_offsetCaculate.currentText()
            mode['offsetEvaluate']=self.dsBox_offsetEvaluate.text()
            mode['direction']=self.cbBox_direction.currentText()
            mode['method']=self.cbBox_method.currentText()
            mode['fusion']=self.cbBox_fusion.currentText()

            con=myconfig()
            con.create(text,mode)
            self.cbBox_mode.setCurrentText(text)
    def imgResize(self):
        # 设置图像是否缩放
        self.imgresize=self.checkBox_resize.isChecked()
    def imgResize_x(self):
        # X缩放比例
        self.imgresize_x=float(self.dsBox_resize_x.text())
    def imgResize_y(self):
        # Y缩放比例
        self.imgresize_y=float(self.dsBox_resize_y.text())
    def cbox_featureMethod(self):
        # 设置搜索算法
        Stitcher.featureMethod = self.cbBox_featureMethod .currentText()
    def dbox_searchRatio(self):
        # 设置搜索算法阈值
        Stitcher.searchRatio=float(self.dsBox_searchRatio.text())
    def cbox_offsetCaculate(self):
        off=self.cbBox_offsetCaculate.currentText()
        if off=="众数":
            Stitcher.offsetCaculate="mode"
        elif off=="RANSAC":
            Stitcher.offsetCaculate="ransac"
    def dbox_offsetEvaluate(self):
        Stitcher.offsetEvaluate=float(self.dsBox_offsetEvaluate.text())
    def cbox_direction(self):
        # 设定拼接方式
        direction = self.cbBox_direction .currentText()
        if direction  ==  '行拼接':
            self.lb_directionPic.setPixmap(QPixmap ("./icon/行拼接.png"))
            Stitcher.direction =4
            Stitcher.directIncre =1
        elif direction == '列拼接':
            self.lb_directionPic.setPixmap(QPixmap("./icon/列拼接.png"))
            Stitcher.direction = 1
            Stitcher.directIncre = -1
        elif direction == '左向拼接':
            self.lb_directionPic.setPixmap(QPixmap("./icon/左向拼接.png"))
            Stitcher.direction = 4
            Stitcher.directIncre = 0
        elif direction == '右向拼接':
            self.lb_directionPic.setPixmap(QPixmap("./icon/右向拼接.png"))
            Stitcher.direction = 2
            Stitcher.directIncre = 0
        elif direction == '朝上拼接':
            self.lb_directionPic.setPixmap(QPixmap("./icon/朝上拼接.png"))
            Stitcher.direction = 3
            Stitcher.directIncre = 0
        elif direction == '朝下拼接':
            self.lb_directionPic.setPixmap(QPixmap("./icon/朝下拼接.png"))
            Stitcher.direction = 1
            Stitcher.directIncre = 0
    def cbox_method(self):
        method = self.cbBox_method.currentText()
        if method=="全局":
            self.method="calculateOffsetForFeatureSearch"
        elif method=="增量":
            self.method="calculateOffsetForFeatureSearchIncre"
    def cbox_fusion(self):
        text=self.cbBox_fusion.currentText()
        if text=="无融合":
            Stitcher.fuseMethod = "notFuse"
        elif text=="均值融合":
            Stitcher.fuseMethod = "average"
        elif text == "最大值融合":
            Stitcher.fuseMethod = "maximum"
        elif text == "最小值融合":
            Stitcher.fuseMethod = "minimum"
        elif text == "渐入渐出融合":
            Stitcher.fuseMethod = "fadeInAndFadeOut"
        elif text == "三角函数融合":
            Stitcher.fuseMethod = "trigonometric"
        elif text == "带权拉普拉斯金字塔融合":
            Stitcher.fuseMethod = "multiBandBlending"
        elif text == "最佳缝合线":
            Stitcher.fuseMethod = "optimalSeamLine"

    def editMode(self):
        # 编辑参数
        self.groupBox_setting.setEnabled(True)
        self.cbBox_mode.setEnabled(False)
        self.bt_editMode.setEnabled(False)
        self.bt_addMode.setEnabled(False)

    def saveMode(self):
        # 保存参数
        self.groupBox_setting .setEnabled(False)
        self.cbBox_mode.setEnabled(True)
        self.bt_editMode.setEnabled(True)
        self.bt_addMode.setEnabled(True)
        text=self.cbBox_mode .currentText()
        mode={}
        mode['imgresize'] = str(self.checkBox_resize.isChecked())
        mode['imgresize_x'] = self.dsBox_resize_x.text()
        mode['imgresize_y'] = self.dsBox_resize_y.text()
        mode['featureMethod'] = self.cbBox_featureMethod.currentText()
        mode['searchRatio'] = self.dsBox_searchRatio.text()
        mode['offsetCaculate'] = self.cbBox_offsetCaculate.currentText()
        mode['offsetEvaluate'] = self.dsBox_offsetEvaluate.text()
        mode['direction'] = self.cbBox_direction.currentText()
        mode['method'] = self.cbBox_method.currentText()
        mode['fusion']=self.cbBox_fusion.currentText()
        con = myconfig()
        con.reset(text,mode)

    def  delMode(self):
        # 删除当前模式
        self.cbBox_mode.currentIndexChanged.disconnect(self.modeSet)
        self.groupBox_setting.setEnabled(False)
        text = self.cbBox_mode.currentText()
        con=myconfig()
        self.cbBox_mode.setCurrentText("默认")
        con.delFile(text)
        self.cbBox_mode.currentIndexChanged.connect(self.modeSet)
        self.modeSet()
        self.cbBox_mode.setEnabled(True)
        self.bt_editMode.setEnabled(True)
        self.bt_addMode.setEnabled(True)


    def printResult(self):
        # 拼接完成后打开拼接结果

        if os.path.exists(self.outputAddress):
            os.startfile(self.outputAddress)
        else:
            warning = QMessageBox.warning(self, "错误！", "打开失败！")

if __name__ == "__main__":
    app=QApplication (sys.argv )
    app.setWindowIcon(QIcon('./icon/icon.png'))
    thread = stitcherThread()
    form = MainWindow()
    # loginForm=LoginWindow()
    # loginForm.show()
    form.show()
    newForm = DialogWindow()
    manualActForm=ManualForm()
    sys.exit(app.exec_())

