import base64
import copy
import os
import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QAbstractItemView

from GetTimestamp import get_TimeStamp
from Grabdata import grab_info
from LuckBox import Ui_Form
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap
from PyQt5 import QtCore, QtGui
from one_jpg import img as one
from two_jpg import img as two

import globalvar as gl

temp_dict_mtl = {}
temp_dict_mdx = {}
temp_info = '礼物信息'
msg_num = 0




class Mywindow(QtWidgets.QMainWindow, Ui_Form):
    def __init__(self):
        super(Mywindow, self).__init__()
        self.setupUi(self)

        # 设置表格
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['昵称', '数量'])
        self.pushButton.clicked.connect(self.connect)
        self.pushButton_2.clicked.connect(self.Timer_emit_begin)
        self.pushButton_2.clicked.connect(self.Timer_emit_mtl)
        self.pushButton_2.clicked.connect(self.Timer_emit_lcd)
        tmp = open('second.jpg', 'wb')  # 创建临时的文件
        tmp.write(base64.b64decode(two))  # 把这个one图片解码出来，写入文件中去。
        tmp.close()
        pix = QPixmap('second.jpg')
        self.label_9.setPixmap(pix)
        os.remove('second.jpg')
        tmp = open('first.jpg', 'wb')  # 创建临时的文件
        tmp.write(base64.b64decode(one))  # 把这个one图片解码出来，写入文件中去。
        tmp.close()
        pix_1 = QPixmap('first.jpg')
        self.label_10.setPixmap(pix_1)
        self.label_10.setScaledContents(True)
        os.remove('first.jpg')

        # 设置表格
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['时间', '昵称', '礼物', '个数', '砖石'])
        self.tableView.setModel(self.model)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView.setColumnWidth(0, 80)
        self.tableView.setColumnWidth(1, 150)
        self.tableView.setColumnWidth(2, 120)
        self.tableView.setColumnWidth(3, 65)
        # 滚动条自动到底
        self.model.rowsInserted.connect(self.autoScroll)

    def autoScroll(self):
        QtCore.QTimer.singleShot(0, self.tableView.scrollToBottom)

    def connect(self):
        # 获取房间号并存入全局变量
        room_id = self.lineEdit.text()
        gl.set_value('roomId', room_id)
        # 根据房间号拿到时间戳并存入全局变量
        time_stamp = get_TimeStamp(room_id)
        gl.set_value('time_stamp', time_stamp)
        # 获取礼物价钱并存入全局变量
        price_mdx = self.lineEdit_2.text()
        price_mtl = self.lineEdit_3.text()
        gl.set_value('price_mdx', price_mdx)
        gl.set_value('price_mtl', price_mtl)
        self.pushButton.setDisabled(True)

    def Timer_emit_begin(self):
        timer = QTimer(self)
        timer.timeout.connect(self.update_begin)
        timer.start(100)

    def update_begin(self):
        # 开始抓取信息
        grab_info(self)
        self.pushButton_2.setDisabled(True)

        # 讲符合条件的信息显示在GUI上的textEdit上
        global msg_num
        global temp_info
        gift_info = gl.get_value(msg_num)
        if gift_info != temp_info and gift_info is not None:
            try:
                msg = gift_info.split(",")
            except Exception as e:
                print(e)
            # print(msg)
            # print('========================================================')
            for i in range(0, len(msg) - 1):
                item = QStandardItem(msg[i])
                try:
                    self.model.setItem(msg_num, i, item)
                    if "梦幻花环" in msg[2]:
                        self.model.item(msg_num, i).setBackground(QtGui.QBrush(QtGui.QColor("mistyrose")))
                    if "梦幻情书" in msg[2]:
                        self.model.item(msg_num, i).setBackground(QtGui.QBrush(QtGui.QColor("cyan")))
                    if "梦幻迷迭香" in msg[2]:
                        self.model.item(msg_num, i).setBackground(QtGui.QBrush(QtGui.QColor("lightpink")))
                    if "梦幻摩天轮" in msg[2]:
                        self.model.item(msg_num, i).setBackground(QtGui.QBrush(QtGui.QColor("gold")))
                    self.model.item(msg_num, i).setTextAlignment(Qt.AlignCenter)
                except Exception as e:
                    print(e)
            temp_info = gift_info
            msg_num += 1
            app.processEvents()

    def Timer_emit_mtl(self):
        timer = QTimer(self)
        timer.timeout.connect(self.update_mtl)
        timer.start(500)

    def update_mtl(self):
        global temp_dict_mdx, temp_dict_mtl
        try:
            dict_Mtl = gl.get_value('dict_Mtl')
            if temp_dict_mdx == dict_Mtl:
                i = 1
            else:
                self.textEdit_2.clear()
                for key in dict_Mtl.keys():
                    str_info = key + ' , ' + str(dict_Mtl[key]) + '个'
                    self.textEdit_2.append(str_info)
                temp_dict_mtl = copy.copy(dict_Mtl)
            # print(dict_Mtl)

        except Exception as e:
            print(e)
            app.processEvents()

        try:
            dict_Mdx = gl.get_value('dict_Mdx')
            if temp_dict_mdx == dict_Mdx:
                i = 1
            else:
                self.textEdit_3.clear()
                for key in dict_Mdx.keys():
                    str_info = key + ' , ' + str(dict_Mdx[key]) + '个'
                    self.textEdit_3.append(str_info)
                temp_dict_mdx = copy.copy(dict_Mdx)

        except Exception as e:
            print(e)
            app.processEvents()

    def Timer_emit_lcd(self):
        timer = QTimer(self)
        timer.timeout.connect(self.update_lcd)
        timer.start(100)

    def update_lcd(self):
        # 获取摩天轮和迷迭香的数量
        num_mdx = gl.get_value('num_mdx')
        num_mtl = gl.get_value('num_mtl')
        # 获取砖石价值和RMB价值
        Total_Diamond = gl.get_value('Total_Diamond')
        RMB_value = gl.get_value('RMB_value')
        # 获取返给玩家的钱
        try:
            price_mdx = gl.get_value('price_mdx')
            price_mtl = gl.get_value('price_mtl')
        except Exception as e:
            print(e)
        balance = RMB_value - num_mtl * int(price_mtl) - num_mdx * int(price_mdx)

        self.lcdNumber.display(Total_Diamond)
        self.lcdNumber_2.display(RMB_value)
        self.lcdNumber_3.display(balance)
        app.processEvents()


app = QtWidgets.QApplication(sys.argv)
window = Mywindow()
window.show()
sys.exit(app.exec_())
