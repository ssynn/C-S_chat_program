import sys
import socket
import json
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout, QSplitter,
                        QToolButton, QLabel, QVBoxLayout, QTextBrowser, QTextEdit, QLineEdit)
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt, QSize


class ClientPage(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.selectList = QWidget()
        self.setSelectList()

        self.chatPage = QWidget()
        self.setChatPage()

        self.rightPage = QWidget()
        self.setRightPage()

        # 主体控件
        self.body = QSplitter()
        self.body.setContentsMargins(0, 0, 0, 0)
        self.body.addWidget(self.chatPage)

        self.bodyLayout = QHBoxLayout()
        self.bodyLayout.addWidget(self.selectList)
        self.bodyLayout.addWidget(self.body)
        self.bodyLayout.addWidget(self.rightPage)

        self.setLayout(self.bodyLayout)
        self.setWindowTitle('CS聊天程序')

        # self.setFixedSize(1280, 720)
        self.setContentsMargins(0, 0, 0, 0)
        self.show()
    
    def setSelectList(self):
        self.selectList.setFixedWidth(200)
    

    def setChatPage(self):
        # 消息框
        self.messageBox = QTextBrowser()

        # 输入框
        self.inputBox = QTextEdit()

        # 设置操作按钮
        self.submit = QToolButton()
        self.submit.setText('发送')
        self.submit.setFixedSize(80, 30)
        # self.submit.clicked.connect(self.confirmFunction)

        self.closePage = QToolButton()
        self.closePage.setText('关闭')
        self.closePage.setFixedSize(80, 30)
        # self.cancel.clicked.connect(self.close)

        self.buttons = QHBoxLayout()
        self.buttons.addStretch()
        self.buttons.addWidget(self.closePage)
        self.buttons.addWidget(self.submit)

        self.chatLayout = QVBoxLayout()
        self.chatLayout.addWidget(self.messageBox)
        self.chatLayout.addWidget(self.inputBox)
        self.chatLayout.addLayout(self.buttons)
        self.chatLayout.setContentsMargins(0,0,0,0)

        self.chatPage.setLayout(self.chatLayout)
        self.chatPage.setContentsMargins(0,0,0,0)

    def setRightPage(self):
        self.inputSocket = QLineEdit()
        self.connectButton = QToolButton()
        self.connectButton.setText('连接')
        self.connectButton.clicked.connect(self.newConnect)

        self.rightPageLayout = QVBoxLayout()
        self.rightPageLayout.addWidget(self.inputSocket)
        self.rightPageLayout.addWidget(self.connectButton)

        self.rightPage.setFixedWidth(200)
        self.rightPage.setLayout(self.rightPageLayout)
    
    def newConnect(self):
        '''
        创建新的聊天界面
        '''
        pass

    def onLine(self):
        '''
        连接服务器
        '''
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 建立连接:
        self.socket.connect(('127.0.0.1', 9999))
        # 接收欢迎消息:
        self.messageBox.append(self.socket.recv(1024).decode('utf-8'))

        while True:

            # 发送数据:
            msg = json.dumps(msg.split())
            self.socket.send(msg.encode())
            print(self.socket.recv(1024).decode('utf-8'))
        self.socket.send(b'exit')
        self.socket.close()
    
    def submitMsg(self):

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ClientPage()
    sys.exit(app.exec_())
