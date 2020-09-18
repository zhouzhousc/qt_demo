#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author: Carl time:2020/5/12


from PyQt5 import QtWidgets


class MyLineEdit(QtWidgets.QLineEdit):
    def __init__(self, id, parent=None):
        QtWidgets.QLineEdit.__init__(self, parent)
        self.id = id

    def focusInEvent(self, e):
        print("输入焦点在", self.id)
        QtWidgets.QLineEdit.focusInEvent(self, e)

    def focusOutEvent(self, e):
        print(self.id, "失去输入焦点")
        QtWidgets.QLineEdit.focusOutEvent(self, e)


class MyWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.resize(300, 100)
        self.button = QtWidgets.QPushButton("设置输入焦点在编辑框 2")
        self.line1 = MyLineEdit(1)
        self.line2 = MyLineEdit(2)
        self.vbox = QtWidgets.QVBoxLayout()

        self.vbox.addWidget(self.line1)
        self.vbox.addWidget(self.line2)
        self.vbox.addWidget(self.button)
        self.setLayout(self.vbox)
        self.button.clicked.connect(self.on_clicked)
        # 指定顺序
        QtWidgets.QWidget.setTabOrder(self.line1, self.line2)
        QtWidgets.QWidget.setTabOrder(self.line2, self.button)

    def on_clicked(self):
        self.line2.setFocus()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
