# Form implementation generated from reading ui file 'd:\original\coding\invoices-reader\progress_dialog.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_ProgressDialog(object):
    def setupUi(self, ProgressDialog):
        ProgressDialog.setObjectName("ProgressDialog")
        ProgressDialog.resize(448, 286)
        self.verticalLayout = QtWidgets.QVBoxLayout(ProgressDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.progressLabel = QtWidgets.QLabel(parent=ProgressDialog)
        self.progressLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.progressLabel.setObjectName("progressLabel")
        self.verticalLayout.addWidget(self.progressLabel)
        self.progressBar = QtWidgets.QProgressBar(parent=ProgressDialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)

        self.retranslateUi(ProgressDialog)
        QtCore.QMetaObject.connectSlotsByName(ProgressDialog)

    def retranslateUi(self, ProgressDialog):
        _translate = QtCore.QCoreApplication.translate
        ProgressDialog.setWindowTitle(_translate("ProgressDialog", "ProgressDialog"))
        self.progressLabel.setText(_translate("ProgressDialog", "please wait...."))
