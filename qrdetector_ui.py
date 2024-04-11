# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\original\coding\qr-detector\qrdetector.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(969, 838)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.browseButton1 = QtWidgets.QPushButton(self.centralwidget)
        self.browseButton1.setGeometry(QtCore.QRect(104, 10, 101, 25))
        self.browseButton1.setObjectName("browseButton1")
        self.browseButton3 = QtWidgets.QPushButton(self.centralwidget)
        self.browseButton3.setGeometry(QtCore.QRect(104, 90, 101, 25))
        self.browseButton3.setObjectName("browseButton3")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(20, 210, 301, 25))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.convertButton = QtWidgets.QPushButton(self.centralwidget)
        self.convertButton.setGeometry(QtCore.QRect(104, 160, 101, 25))
        self.convertButton.setObjectName("convertButton")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(335, 40, 621, 731))
        self.graphicsView.setObjectName("graphicsView")
        self.vendor_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.vendor_lineedit.setGeometry(QtCore.QRect(112, 290, 201, 25))
        self.vendor_lineedit.setObjectName("vendor_lineedit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(30, 290, 71, 25))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(28, 330, 71, 25))
        self.label_2.setObjectName("label_2")
        self.vatid_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.vatid_lineedit.setGeometry(QtCore.QRect(110, 330, 201, 25))
        self.vatid_lineedit.setObjectName("vatid_lineedit")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(28, 370, 71, 25))
        self.label_3.setObjectName("label_3")
        self.date_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.date_lineedit.setGeometry(QtCore.QRect(110, 370, 201, 25))
        self.date_lineedit.setObjectName("date_lineedit")
        self.total_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.total_lineedit.setGeometry(QtCore.QRect(112, 410, 201, 25))
        self.total_lineedit.setObjectName("total_lineedit")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 410, 71, 25))
        self.label_4.setObjectName("label_4")
        self.vatamount_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.vatamount_lineedit.setGeometry(QtCore.QRect(112, 450, 201, 25))
        self.vatamount_lineedit.setObjectName("vatamount_lineedit")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(30, 450, 71, 25))
        self.label_5.setObjectName("label_5")
        self.last = QtWidgets.QPushButton(self.centralwidget)
        self.last.setGeometry(QtCore.QRect(710, 10, 75, 25))
        self.last.setObjectName("last")
        self.next = QtWidgets.QPushButton(self.centralwidget)
        self.next.setGeometry(QtCore.QRect(630, 10, 75, 25))
        self.next.setObjectName("next")
        self.previous = QtWidgets.QPushButton(self.centralwidget)
        self.previous.setGeometry(QtCore.QRect(550, 10, 75, 25))
        self.previous.setObjectName("previous")
        self.first = QtWidgets.QPushButton(self.centralwidget)
        self.first.setGeometry(QtCore.QRect(470, 10, 75, 25))
        self.first.setObjectName("first")
        self.save = QtWidgets.QPushButton(self.centralwidget)
        self.save.setGeometry(QtCore.QRect(60, 500, 101, 25))
        self.save.setObjectName("save")
        self.folder_path_label = QtWidgets.QLabel(self.centralwidget)
        self.folder_path_label.setGeometry(QtCore.QRect(46, 50, 251, 20))
        self.folder_path_label.setText("")
        self.folder_path_label.setObjectName("folder_path_label")
        self.location_label = QtWidgets.QLabel(self.centralwidget)
        self.location_label.setGeometry(QtCore.QRect(50, 120, 251, 20))
        self.location_label.setText("")
        self.location_label.setObjectName("location_label")
        self.ai_button = QtWidgets.QPushButton(self.centralwidget)
        self.ai_button.setGeometry(QtCore.QRect(190, 500, 101, 25))
        self.ai_button.setObjectName("ai_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 969, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.browseButton1.setText(_translate("MainWindow", "choose folder"))
        self.browseButton3.setText(_translate("MainWindow", "save location"))
        self.convertButton.setText(_translate("MainWindow", "start"))
        self.label.setText(_translate("MainWindow", "اسم المورد"))
        self.label_2.setText(_translate("MainWindow", "الرقم الضريبي"))
        self.label_3.setText(_translate("MainWindow", "التاريخ"))
        self.label_4.setText(_translate("MainWindow", "مبلغ الفاتورة"))
        self.label_5.setText(_translate("MainWindow", "مبلغ الضريبة"))
        self.last.setText(_translate("MainWindow", ">>"))
        self.next.setText(_translate("MainWindow", ">"))
        self.previous.setText(_translate("MainWindow", "<"))
        self.first.setText(_translate("MainWindow", "<<"))
        self.save.setText(_translate("MainWindow", "save invoice"))
        self.ai_button.setText(_translate("MainWindow", "ai extract"))
