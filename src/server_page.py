import sys
import socket
import json
import threading
import time
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout, QSplitter, QTableWidget,
                             QToolButton, QLabel, QAbstractItemView, QHeaderView, QTableWidgetItem, QVBoxLayout, QTextBrowser, QTextEdit, QLineEdit, QMessageBox)
from PyQt5.QtGui import QIcon, QColor, QFont
from PyQt5.QtCore import Qt, QSize, QTimer


class ServerPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.body = QHBoxLayout()

        # 设置缓冲池界面
        self.setTable()

        # 设置在线用户界面
        self.setOnlineUsers()

        # 设置离线用户界面
        self.setOfflineUsers()

        self.body.addWidget(self.messageBuffer)
        self.body.addWidget(self.onlineUser)
        self.body.addWidget(self.offlineUser)
        self.body.setContentsMargins(0, 0, 0, 0)

        self.setLayout(self.body)

    def setTable(self):
        self.messageBuffer = QTableWidget(1, 3)
        self.messageBuffer.verticalHeader().setVisible(False)
        self.messageBuffer.horizontalHeader().setVisible(False)
        self.messageBuffer.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.messageBuffer.setFocusPolicy(Qt.NoFocus)
        self.messageBuffer.setColumnWidth(0, 130)
        self.messageBuffer.setColumnWidth(1, 130)
        self.messageBuffer.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)

        self.messageBuffer.setItem(0, 0, QTableWidgetItem('FROM'))
        self.messageBuffer.setItem(0, 1, QTableWidgetItem('TO'))
        self.messageBuffer.setItem(0, 2, QTableWidgetItem('MESSAGE'))

        for i in range(3):
            self.messageBuffer.item(0, i).setTextAlignment(Qt.AlignCenter)
            self.messageBuffer.item(0, i).setFont(QFont('微软雅黑', 15))

        # self.messageBuffer.insertRow(1)
        # a = QTableWidgetItem('127.0.0.1:9999')
        # b = QTableWidgetItem('127.0.0.1:9999')
        # c = QTableWidgetItem('22121321321321')
        # self.messageBuffer.setItem(1, 0, a)
        # self.messageBuffer.setItem(1, 1, b)
        # self.messageBuffer.setItem(1, 2, c)

    def setOnlineUsers(self):
        self.onlineUser = QTableWidget(1, 1)
        self.onlineUser.horizontalHeader().setVisible(False)
        self.onlineUser.verticalHeader().setVisible(False)
        self.onlineUser.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.onlineUser.setFocusPolicy(Qt.NoFocus)
        self.onlineUser.setColumnWidth(0, 150)
        self.onlineUser.setFixedWidth(150)
        self.onlineUser.verticalScrollBar().setStyleSheet('''
            QScrollBar{background:transparent; width: 10px;}
            QScrollBar::handle{background:lightgray; border:2px solid transparent; border-radius:5px;}
            QScrollBar::handle:hover{background:gray;}
            QScrollBar::sub-line{background:transparent;}
            QScrollBar::add-line{background:transparent;}
        ''')

        self.onlineUser.setItem(0, 0, QTableWidgetItem('离线'))
        self.onlineUser.item(0, 0).setTextAlignment(Qt.AlignCenter)
        self.onlineUser.item(0, 0).setFont(QFont('微软雅黑', 15))

        # self.onlineUser.insertRow(1)
        # tt = QTableWidgetItem('127.0.0.1:9999')
        # self.onlineUser.setItem(1, 0, tt)

    def setOfflineUsers(self):
        self.offlineUser = QTableWidget(1, 1)
        self.offlineUser.horizontalHeader().setVisible(False)
        self.offlineUser.verticalHeader().setVisible(False)
        self.offlineUser.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.offlineUser.setFocusPolicy(Qt.NoFocus)
        self.offlineUser.setColumnWidth(0, 150)
        self.offlineUser.setFixedWidth(155)
        self.offlineUser.verticalScrollBar().setStyleSheet('''
            QScrollBar{background:transparent; width: 10px;}
            QScrollBar::handle{background:lightgray; border:2px solid transparent; border-radius:5px;}
            QScrollBar::handle:hover{background:gray;}
            QScrollBar::sub-line{background:transparent;}
            QScrollBar::add-line{background:transparent;}
        ''')

        self.offlineUser.setItem(0, 0, QTableWidgetItem('在线'))
        self.offlineUser.item(0, 0).setTextAlignment(Qt.AlignCenter)
        self.offlineUser.item(0, 0).setFont(QFont('微软雅黑', 15))

        # self.offlineUser.insertRow(1)
        # tt = QTableWidgetItem('127.0.0.1:9999')
        # self.offlineUser.setItem(1, 0, tt)
    
    def refresh(self):
        '''
        每秒获取一次服务器的状态，把信息跟新到服务器
        '''
        pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ServerPage()
    ex.show()
    sys.exit(app.exec_())
