#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author: Carl time:2020/5/11
import sys

from demo1 import Ui_MainWindow
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
from serial import Serial
import serial.tools.list_ports

import threading
import time


class QueryWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # 给button 的 点击动作绑定一个事件处理函数
        self.ui.pushButton.clicked.connect(self.query_formula)
        self.ui.pushButton_2.clicked.connect(self.query_formula2)

    def query_formula(self):
        # 此处编写具体的业务逻辑
        plist = list(serial.tools.list_ports.comports())
        if len(plist) <= 0:
            print("The Serial port can't find!")

        else:
            plist_lastname = list(plist[-1])[0]
            print(plist_lastname)

        with open('num.txt', 'w', encoding='utf-8', newline='') as f:
            count = 0
            j = 0

            while count < 500001:
                f.write(str(count) + "\n")
                for i in range(1, 10000):
                    j += 1
                count = count + 1

        self.ui.pushButton.setStyleSheet("color: red")
        print("finished")

        # ser = Serial(port=plist_lastname, baudrate=115200)
        # count = 0
        #
        # with open('move6.txt', 'w', encoding='utf-8', newline='') as f:  # 追加是a+
        #     f.write("ax,ay,az,gx,gy,gz,mx, my,mz,Yaw,Pitch,Roll,rate\n")
        #
        #     while count < 501:
        #         try:
        #             data = str(ser.readline(), encoding="utf-8")
        #             print(data)
        #             f.write(data)
        #             count += 1
        #
        #         except Exception as e:
        #             print(e)
        #             time.sleep(1)
        #
        # ser.close()
        # print("finished")

    def query_formula2(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = QueryWindow()
    w.show()
    sys.exit(app.exec_())

    # t1 = threading.Thread(target=query_formula)
    # t2 = threading.Thread(target=QueryWindow.query_formula2)
    #
    # t2.start()
    # t1.start()
    # t2.join()
    # t1.join()
