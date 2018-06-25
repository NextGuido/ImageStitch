# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myui2.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(807, 560)
        Dialog.setMinimumSize(QtCore.QSize(807, 560))
        Dialog.setMaximumSize(QtCore.QSize(807, 560))
        self.bt_backMainWindow = QtWidgets.QPushButton(Dialog)
        self.bt_backMainWindow.setGeometry(QtCore.QRect(622, 70, 81, 28))
        self.bt_backMainWindow.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bt_backMainWindow.setObjectName("bt_backMainWindow")
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(80, 70, 451, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.list_stitcherlog = QtWidgets.QListWidget(Dialog)
        self.list_stitcherlog.setGeometry(QtCore.QRect(80, 240, 621, 281))
        self.list_stitcherlog.setObjectName("list_stitcherlog")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(80, 40, 72, 15))
        self.label.setObjectName("label")
        self.lb_stitchInf = QtWidgets.QLabel(Dialog)
        self.lb_stitchInf.setGeometry(QtCore.QRect(170, 40, 321, 20))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.lb_stitchInf.setFont(font)
        self.lb_stitchInf.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.lb_stitchInf.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lb_stitchInf.setObjectName("lb_stitchInf")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(80, 110, 72, 15))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(80, 220, 72, 15))
        self.label_3.setObjectName("label_3")
        self.list_result = QtWidgets.QListWidget(Dialog)
        self.list_result.setGeometry(QtCore.QRect(80, 130, 621, 71))
        self.list_result.setObjectName("list_result")
        self.bt_openResult = QtWidgets.QPushButton(Dialog)
        self.bt_openResult.setGeometry(QtCore.QRect(540, 70, 71, 28))
        self.bt_openResult.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.bt_openResult.setObjectName("bt_openResult")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "北科大材料显微图像拼接软件"))
        self.bt_backMainWindow.setText(_translate("Dialog", "返回"))
        self.label.setText(_translate("Dialog", "拼接进度："))
        self.lb_stitchInf.setText(_translate("Dialog", "拼接进度"))
        self.label_2.setText(_translate("Dialog", "拼接结论："))
        self.label_3.setText(_translate("Dialog", "日志："))
        self.bt_openResult.setText(_translate("Dialog", "打开结果"))

