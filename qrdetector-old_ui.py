# Form implementation generated from reading ui file 'd:\original\coding\invoices-reader\qrdetector-old.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(969, 838)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.progressBar = QtWidgets.QProgressBar(parent=self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(20, 310, 301, 25))
        self.progressBar.setLayoutDirection(QtCore.Qt.LayoutDirection.RightToLeft)
        self.progressBar.setAutoFillBackground(True)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.layoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(18, 390, 291, 191))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.vatamount_lineedit = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.vatamount_lineedit.setObjectName("vatamount_lineedit")
        self.gridLayout.addWidget(self.vatamount_lineedit, 4, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 1, 1, 1)
        self.total_lineedit = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.total_lineedit.setObjectName("total_lineedit")
        self.gridLayout.addWidget(self.total_lineedit, 3, 0, 1, 1)
        self.invoicenumber_lineedit = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.invoicenumber_lineedit.setObjectName("invoicenumber_lineedit")
        self.gridLayout.addWidget(self.invoicenumber_lineedit, 6, 0, 1, 1)
        self.vendor_lineedit = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.vendor_lineedit.setObjectName("vendor_lineedit")
        self.gridLayout.addWidget(self.vendor_lineedit, 0, 0, 1, 1)
        self.date_lineedit = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.date_lineedit.setObjectName("date_lineedit")
        self.gridLayout.addWidget(self.date_lineedit, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 1, 1, 1)
        self.vatid_lineedit = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.vatid_lineedit.setObjectName("vatid_lineedit")
        self.gridLayout.addWidget(self.vatid_lineedit, 1, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_6.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 6, 1, 1, 1)
        self.layoutWidget1 = QtWidgets.QWidget(parent=self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(335, 10, 621, 791))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.first = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.first.setObjectName("first")
        self.gridLayout_2.addWidget(self.first, 0, 0, 1, 1)
        self.previous = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.previous.setObjectName("previous")
        self.gridLayout_2.addWidget(self.previous, 0, 1, 1, 1)
        self.next = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.next.setObjectName("next")
        self.gridLayout_2.addWidget(self.next, 0, 2, 1, 1)
        self.last = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.last.setObjectName("last")
        self.gridLayout_2.addWidget(self.last, 0, 3, 1, 1)
        self.graphicsView = QtWidgets.QGraphicsView(parent=self.layoutWidget1)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout_2.addWidget(self.graphicsView, 1, 0, 1, 4)
        self.layoutWidget2 = QtWidgets.QWidget(parent=self.centralwidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(26, 110, 281, 181))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.browseButton1 = QtWidgets.QPushButton(parent=self.layoutWidget2)
        self.browseButton1.setObjectName("browseButton1")
        self.gridLayout_3.addWidget(self.browseButton1, 0, 0, 1, 1)
        self.folder_path_label = QtWidgets.QLabel(parent=self.layoutWidget2)
        self.folder_path_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.folder_path_label.setObjectName("folder_path_label")
        self.gridLayout_3.addWidget(self.folder_path_label, 1, 0, 1, 1)
        self.browseButton3 = QtWidgets.QPushButton(parent=self.layoutWidget2)
        self.browseButton3.setObjectName("browseButton3")
        self.gridLayout_3.addWidget(self.browseButton3, 2, 0, 1, 1)
        self.location_label = QtWidgets.QLabel(parent=self.layoutWidget2)
        self.location_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.location_label.setObjectName("location_label")
        self.gridLayout_3.addWidget(self.location_label, 3, 0, 1, 1)
        self.convertButton = QtWidgets.QPushButton(parent=self.layoutWidget2)
        self.convertButton.setObjectName("convertButton")
        self.gridLayout_3.addWidget(self.convertButton, 4, 0, 1, 1)
        self.layoutWidget3 = QtWidgets.QWidget(parent=self.centralwidget)
        self.layoutWidget3.setGeometry(QtCore.QRect(20, 600, 291, 25))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.layoutWidget3)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.ai_button = QtWidgets.QPushButton(parent=self.layoutWidget3)
        self.ai_button.setObjectName("ai_button")
        self.gridLayout_4.addWidget(self.ai_button, 0, 1, 1, 1)
        self.save = QtWidgets.QPushButton(parent=self.layoutWidget3)
        self.save.setObjectName("save")
        self.gridLayout_4.addWidget(self.save, 0, 0, 1, 1)
        self.layoutWidget4 = QtWidgets.QWidget(parent=self.centralwidget)
        self.layoutWidget4.setGeometry(QtCore.QRect(80, 50, 158, 25))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.layoutWidget4)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.previous_extractions = QtWidgets.QPushButton(parent=self.layoutWidget4)
        self.previous_extractions.setObjectName("previous_extractions")
        self.gridLayout_5.addWidget(self.previous_extractions, 0, 0, 1, 1)
        self.new_batch = QtWidgets.QPushButton(parent=self.layoutWidget4)
        self.new_batch.setObjectName("new_batch")
        self.gridLayout_5.addWidget(self.new_batch, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 969, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_5.setText(_translate("MainWindow", "مبلغ الضريبة"))
        self.label_4.setText(_translate("MainWindow", "مبلغ الفاتورة"))
        self.label_3.setText(_translate("MainWindow", "التاريخ"))
        self.label.setText(_translate("MainWindow", "اسم المورد"))
        self.label_2.setText(_translate("MainWindow", "الرقم الضريبي"))
        self.label_6.setText(_translate("MainWindow", "رقم الفاتورة"))
        self.first.setText(_translate("MainWindow", "<<"))
        self.previous.setText(_translate("MainWindow", "<"))
        self.next.setText(_translate("MainWindow", ">"))
        self.last.setText(_translate("MainWindow", ">>"))
        self.browseButton1.setText(_translate("MainWindow", "Choose Folder"))
        self.folder_path_label.setText(_translate("MainWindow", "................."))
        self.browseButton3.setText(_translate("MainWindow", "Save Location"))
        self.location_label.setText(_translate("MainWindow", "................."))
        self.convertButton.setText(_translate("MainWindow", "Start Qr Reading"))
        self.ai_button.setText(_translate("MainWindow", "Extract Invoice With AI"))
        self.save.setText(_translate("MainWindow", "Save Edits"))
        self.previous_extractions.setText(_translate("MainWindow", "History"))
        self.new_batch.setText(_translate("MainWindow", "New Batch"))
