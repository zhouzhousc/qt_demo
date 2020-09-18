#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author: Carl time:2020/5/15


import sys
import json
import threading
from serial import Serial
import serial.tools.list_ports
import time
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, \
    QGridLayout, QListWidget, QInputDialog, QLineEdit, QMessageBox, QDialog
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QDateTime


class BackendThread(QThread):
    # 通过类成员对象定义信号
    update_date = pyqtSignal(str)

    # 处理业务逻辑
    def run(self):
        while True:
            data = QDateTime.currentDateTime()
            currTime = data.toString("yyyy-MM-dd hh:mm:ss")
            self.update_date.emit(str(currTime))
            time.sleep(1)


class GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.stop_flag = ""
        self.iniUI()

    def iniUI(self):
        self.setWindowTitle("炒鸡小工具")
        self.resize(600, 400)
        self.add_menu_and_statu()
        self.grid_layout()
        # self.listWidget()
        self.qthread(self.timedis)

    def qthread(self, handle):
        # 创建线程
        self.backend = BackendThread()
        # 连接信号
        self.backend.update_date.connect(handle)
        # 开始线程
        self.backend.start()

    # 添加菜单栏和状态栏
    def add_menu_and_statu(self):
        self.statusBar().showMessage("版本V0.0")
        # 创建一个菜单栏
        menu = self.menuBar()
        # 创建两个菜单
        file_menu = menu.addMenu("文件")
        file_menu.addSeparator()
        edit_menu = menu.addMenu('修改')
        edit_menu.addSeparator()

        # 创建一个行为
        new_action = QAction('新的文件', self)
        # 更新状态栏文本
        new_action.setStatusTip('打开新的文件')
        # 添加一个行为到菜单
        file_menu.addAction(new_action)

        # 创建退出行为
        exit_action = QAction('退出', self)
        # 退出操作
        exit_action.setStatusTip("点击退出应用程序")
        # 点击关闭程序
        exit_action.triggered.connect(self.close)
        # 设置退出快捷键
        exit_action.setShortcut('Ctrl+Q')
        # 添加退出行为到菜单上
        file_menu.addAction(exit_action)

    # 网格布局
    def grid_layout(self):
        # 两个标签
        label_1 = QLabel('mpu数据串口采集')
        label_2 = QLabel('当前时间显示')
        self.label3 = QLabel(self)
        self.label3.setFixedWidth(113)
        self.label_4 = QLabel('采集数据耗时')
        self.label5 = QLabel(self)

        # 两个按钮
        button_1 = QPushButton('开始采集')
        button_2 = QPushButton('停止采集')
        button_3 = QPushButton('文件数据分析')
        button_4 = QPushButton('选定COM')
        button_1.clicked.connect(self.getText)
        button_2.clicked.connect(self.getInteger)
        button_3.clicked.connect(self.getDouble)
        button_4.clicked.connect(self.getChoice)

        # 创建一个网格布局对象
        grid_layout = QGridLayout()

        # 在网格中添加窗口部件
        grid_layout.addWidget(label_1, 0, 0)  # 放置在0行0列
        grid_layout.addWidget(button_1, 0, 3)  # 0行1列
        grid_layout.addWidget(label_2, 1, 0)  # 1行0列
        grid_layout.addWidget(button_2, 0, 4)  # 1行1列
        grid_layout.addWidget(button_3, 3, 0, 1, 1)
        grid_layout.addWidget(button_4, 0, 1)
        grid_layout.addWidget(self.label3, 1, 1)
        grid_layout.addWidget(self.label_4, 2, 0)
        grid_layout.addWidget(self.label5, 2, 1)

        # 对齐方式
        grid_layout.setAlignment(Qt.AlignTop)
        # grid_layout.setAlignment(label_1, Qt.AlignRight)

        # 创建一个窗口对象
        layout_widget = QWidget()
        # 设置窗口的布局层
        layout_widget.setLayout(grid_layout)

        self.setCentralWidget(layout_widget)

    def listWidget(self):
        self.listView = QListWidget(self)  # 实例化QListWidget
        self.listView.setGeometry(20, 120, 200, 100)  # 设置QListWidget在窗口中的位置与大小
        self.listView.addItem('点击关闭！！')  # 往QListWidget添加内容
        self.listView.addItem('点击也是关闭！！')  # 往QListWidget添加内容
        self.listView.itemClicked.connect(self.close)  # 给 QListWidget 每个项目设置点击事件

    def getText(self):
        self.text, okPressed = QInputDialog.getText(self, '保存文件', '请输入文件名', QLineEdit.Normal, "move.txt")

        if okPressed and self.text != '':
            print(self.text)
            self.thread_ser_data()

    def getIfom(self):
        reply = QMessageBox.information(self, '失败', '没有可用串口', QMessageBox.Retry | QMessageBox.Cancel)
        if reply == QMessageBox.Retry:
            self.getText()

    def getInteger(self):
        self.t2 = time.time()
        self.label5.setText(str(round(self.t2 - self.t1, 2)) + "s")
        self.stop_flag = "break_flag"
        print("停止采集")

    def getDouble(self):
        # d, okPressed = QInputDialog.getDouble(self, "浮点数", "选择浮点数:", 10.05, 0, 100, 3)
        # if okPressed:
        #     print(d)
        pass

    def getChoice(self):
        # Get item/choice
        items = []
        plist = list(serial.tools.list_ports.comports())
        for i in range(len(plist)):
            items.append(list(plist[i])[0])
        self.item, okPressed = QInputDialog.getItem(self, "选择com口", "COM：", items, 0, False)

        if okPressed and self.item:
            print(self.item)

    def thread_ser_data(self):
        t = threading.Thread(target=self.ser_data, name='ser_data')
        t.start()

    def ser_data(self):
        self.t1 = time.time()
        self.count = 0
        self.stop_flag = "ok"

        ser = Serial(port=self.item, baudrate=115200)
        with open(self.text, 'w', encoding='utf-8', newline='') as f:  # 追加是a+
            f.write("ax,ay,az,gx,gy,gz,mx, my,mz,Yaw,Pitch,Roll,rate,count\n")

            while self.count < 2001:
                if self.stop_flag == "break_flag":
                    break

                else:
                    try:
                        data = str(ser.readline(), encoding="utf-8")
                        print(data)
                        f.write(data)
                        self.count += 1

                    except Exception as e:
                        print(e)
                        time.sleep(1)
        # while self.count < 50000001:
        #     if self.stop_flag == "break_flag":
        #         break
        #     else:
        #
        #         self.count += 1
        #         print(self.count)
        ser.close()
        print("finished")

    def timedis(self, data):
        self.label3.setText(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())
