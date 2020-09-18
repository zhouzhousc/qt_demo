#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author: Carl time:2020/5/12


import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QColorDialog
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor


class ColorDialog(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self)

        color = QColor(255, 255, 255)  # 设置初始颜色
        self.setGeometry(300, 300, 350, 350)
        self.setWindowTitle('ColorDialog')  # 设置主窗口标题
        self.button = QPushButton('Dialog', self)  # 设置按键文字
        self.button.setFocusPolicy(Qt.NoFocus)  # 设置button焦点
        self.button.move(20, 20)
        self.button.clicked.connect(self.showDialog)  # 信号->事件->槽函数
        self.setFocus()  # 设置主窗口焦点

        self.widget = QtWidgets.QWidget(self)
        self.widget.setStyleSheet('QWidget{background-color:%s}' % color.name())
        self.widget.setGeometry(130, 22, 100, 100)

    def showDialog(self):
        col = QColorDialog.getColor()
        if col.isValid():
            # color.name() 获取到颜色面板选择颜色的值
            self.widget.setStyleSheet('QWidget {background-color:%s}' % col.name())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    qb = ColorDialog()  # 实例化颜色面板
    qb.show()  # 显示
    sys.exit(app.exec_())
