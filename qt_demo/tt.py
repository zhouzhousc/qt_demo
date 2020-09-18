#!/usr/bin/python
# -*- coding: UTF-8 -*-
# author: Carl time:2020/5/12


import pandas as pd
import numpy as np
import os, json, time
import matplotlib.pyplot as plt
from scipy import signal
import serial

plt.figure()
plt.title("accelerated speed ax,ay,az")
for i, f in enumerate(os.listdir(r'F:/mpu9250r/')[3:9]):
    plt.subplot(4, 3, i + 1)
    print((i, f))
    # data1= pd.read_csv(f, index_col=False)["Yaw"]
    # data2= pd.read_csv(f, index_col=False)["Pitch"]
    # data3= pd.read_csv(f, index_col=False)["Roll"]

    data1 = pd.read_csv('F:/mpu9250r/move1.txt', index_col=False)["az"] / 100
    # data2 = pd.read_csv(f, index_col=False)["ay"] / 100
    # data3 = pd.read_csv(f, index_col=False)["ax"] / 100
    # g = abs(np.sqrt(np.square(data1) + np.square(data2) + np.square(data3)))
    # print(g)
    # gravity, alpha = 9.81, 0.8
    # gravity = alpha * gravity + (1 - alpha) * data1  # 清除重力加速度影響
    # data_decomp = data1 - gravity
    peakind = signal.find_peaks(data1, height=11.0, width=1.5)
    plt.scatter(peakind[0], data1[peakind[0]], c="r", marker="d", label="Cycle:" + str(peakind[0].shape[0]))
    #     plt.plot(data1, label="Yaw")
    #     plt.plot(data2, label="Pitch")
    #     plt.plot(data3, label="Roll")
    plt.plot(data1, label="az")

    #     plt.ylabel(f)
    plt.legend()
