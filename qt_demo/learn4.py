#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author: Carl time:2020/5/12


# calc.py

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QWidget

from ui_calc import Ui_Calc


# 方式一
class MyCalc(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Calc()
        self.resize(250, 150)
        self.ui.setupUi(self)

    @pyqtSlot(int)
    def on_inputSpinBox1_valueChanged(self, value):
        self.ui.outputWidget.setText(str(value + self.ui.inputSpinBox2.value()))

    @pyqtSlot(int)
    def on_inputSpinBox2_valueChanged(self, value):
        self.ui.outputWidget.setText(str(value + self.ui.inputSpinBox1.value()))


# 方式二
class MyCalc2(QWidget, Ui_Calc):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

    @pyqtSlot(int)
    def on_inputSpinBox1_valueChanged(self, value):
        self.outputWidget.setText(str(value + self.inputSpinBox2.value()))

    @pyqtSlot(int)
    def on_inputSpinBox2_valueChanged(self, value):
        self.outputWidget.setText(str(value + self.inputSpinBox1.value()))


# @PyQt5.QtCore.pyqtSlot(参数)
# def on_发送者对象名称_发射信号名称(self, 参数):
#     pass

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    win = MyCalc()
    # win = MyCalc2()
    win.show()
    sys.exit(app.exec_())
