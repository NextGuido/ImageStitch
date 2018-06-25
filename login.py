# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(288, 165)
        self.label = QtWidgets.QLabel(Login)
        self.label.setGeometry(QtCore.QRect(40, 30, 91, 16))
        self.label.setObjectName("label")
        self.lineEdit_password = QtWidgets.QLineEdit(Login)
        self.lineEdit_password.setGeometry(QtCore.QRect(40, 60, 211, 21))
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.bt_yes = QtWidgets.QPushButton(Login)
        self.bt_yes.setGeometry(QtCore.QRect(40, 100, 93, 28))
        self.bt_yes.setObjectName("bt_yes")
        self.bt_no = QtWidgets.QPushButton(Login)
        self.bt_no.setGeometry(QtCore.QRect(160, 100, 93, 28))
        self.bt_no.setObjectName("bt_no")

        self.retranslateUi(Login)
        self.bt_no.clicked['bool'].connect(Login.close)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "请登录"))
        self.label.setText(_translate("Login", "请输入密码："))
        self.bt_yes.setText(_translate("Login", "确定"))
        self.bt_no.setText(_translate("Login", "取消"))

