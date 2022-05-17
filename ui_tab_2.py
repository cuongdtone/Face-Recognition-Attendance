# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_tab.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Tab_2(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1366, 780)
        self.gridLayoutWidget = QtWidgets.QWidget(Form)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(100, 150, 281, 141))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setStyleSheet("color: rgb(255, 255, 255);\n"
                                    "font: 75 15pt \"Ubuntu Condensed\";\n"
                                    "border-style:inset;")
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setStyleSheet("color: rgb(255, 255, 255);\n"
                                    "font: 75 15pt \"Ubuntu Condensed\";\n"
                                    "border-style:inset;")
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);\n"
                                    "font: 75 15pt \"Ubuntu Condensed\";\n"
                                    "border-style:inset;")
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.office = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.office.setStyleSheet("border-color: rgb(255, 255, 255);\n"
                                    "background-color: rgb(136, 138, 133);\n"
                                    "border-width : 1.5px;\n"
                                    "border-style:inset;\n"
                                    "border-radius: 8px;\n"
                                    "padding: 0 5px;")
        self.office.setObjectName("office")
        self.gridLayout.addWidget(self.office, 2, 1, 1, 1)
        self.position = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.position.setStyleSheet("border-color: rgb(255, 255, 255);\n"
                                    "background-color: rgb(136, 138, 133);\n"
                                    "border-width : 1.5px;\n"
                                    "border-style:inset;\n"
                                    "border-radius: 8px;\n"
                                    "padding: 0 5px;")
        self.position.setObjectName("position")
        self.gridLayout.addWidget(self.position, 1, 1, 1, 1)
        self.name = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.name.setStyleSheet("border-color: rgb(255, 255, 255);\n"
                                "background-color: rgb(136, 138, 133);\n"
                                "border-width : 1.5px;\n"
                                "border-style:inset;\n"
                                "border-radius: 8px;\n"
                                "padding: 0 5px;")
        self.name.setText("")
        self.name.setObjectName("name")
        self.gridLayout.addWidget(self.name, 0, 1, 1, 1)
        self.screen = QtWidgets.QLabel(Form)
        self.screen.setGeometry(QtCore.QRect(490, 120, 720, 480))
        self.screen.setStyleSheet("background-color: rgb(136, 138, 133);\n"
                                    "border-color: rgb(255 ,255,255);\n"
                                    "font: 75 15pt \"Ubuntu Condensed\";\n"
                                    "border-width : 1.5px;\n"
                                    "border-style:inset;\n"
                                    "border-radius: 8px;\n"
                                    "padding: 0 5px;\n"
                                    "color: rgb(255, 255, 255);")
        self.screen.setAlignment(QtCore.Qt.AlignCenter)
        self.screen.setObjectName("screen")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(810, 70, 91, 41))
        self.label_5.setStyleSheet("font: 75 15pt \"Ubuntu Condensed\";\n"
                                    "color: rgb(255, 255, 255);")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(10, 10, 1366, 768))
        self.label_6.setStyleSheet("background-color: rgb(46, 52, 54)")
        self.label_6.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_6.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")
        self.create_person = QtWidgets.QPushButton(Form)
        self.create_person.setGeometry(QtCore.QRect(180, 460, 111, 91))
        self.create_person.setStyleSheet("QPushButton{\n"
                                        "border-color: rgb(255 ,255,255);\n"
                                        "font: 75 15pt \"Ubuntu Condensed\";\n"
                                        "background-color: rgb(136, 138, 133);\n"
                                        "border-width : 1.5px;\n"
                                        "border-style:inset;\n"
                                        "border-radius: 8px;\n"
                                        "padding: 0 5px;\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "}")
        self.create_person.setObjectName("create_person")
        self.cap_button = QtWidgets.QPushButton(Form)
        self.cap_button.setGeometry(QtCore.QRect(180, 340, 111, 91))
        self.cap_button.setStyleSheet("QPushButton{\n"
                                        "border-color: rgb(255 ,255,255);\n"
                                        "font: 75 15pt \"Ubuntu Condensed\";\n"
                                        "background-color: rgb(136, 138, 133);\n"
                                        "border-width : 1.5px;\n"
                                        "border-style:inset;\n"
                                        "border-radius: 8px;\n"
                                        "padding: 0 5px;\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "}")
        self.cap_button.setObjectName("cap_button")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(70, 110, 341, 191))
        self.label_7.setStyleSheet("border-color: rgb(255, 255, 255);\n"
                                    "border-width : 1.5px;\n"
                                    "border-style:inset;\n"
                                    "border-radius: 8px;\n"
                                    "font: 75 15pt \"Ubuntu Condensed\";\n"
                                    "padding: 0 5px;\n"
                                    "color: rgb(255, 255, 255);")
        self.label_7.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_7.setObjectName("label_7")
        self.label_6.raise_()
        self.gridLayoutWidget.raise_()
        self.screen.raise_()
        self.label_5.raise_()
        self.create_person.raise_()
        self.cap_button.raise_()
        self.label_7.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_3.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:18pt; font-weight:400;\">Positon</span></p></body></html>"))
        self.label_4.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:18pt; font-weight:400;\">Office</span></p></body></html>"))
        self.label_2.setText(_translate("Form", "<html><head/><body><p><span style=\" font-size:18pt; font-weight:400;\">Name</span></p></body></html>"))
        self.screen.setText(_translate("Form", "Screen"))
        self.label_5.setText(_translate("Form", "<html><head/><body><p>CAMERA</p><p><br/></p></body></html>"))
        # self.create_person.setText(_translate("Form", "Completed"))
        # self.cap_button.setText(_translate("Form", "Take a photo"))
        self.label_7.setText(_translate("Form", "NEW EMPLOYEE"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Tab_2()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
