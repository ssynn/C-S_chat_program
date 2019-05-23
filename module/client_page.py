import sys
import socket
import json
import threading
import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout, QSplitter,
                        QToolButton, QLabel, QVBoxLayout, QTextBrowser, QTextEdit, QLineEdit)
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt, QSize


def recvMsg(master):
    '''
    返回的消息格式为[
        {
            source:str,
            target:str,
            text:str,
            time:str,
            operation:str
        },
        ...
    ]
    '''
    while True:
        try:
            msgs = master.socket.recv(2048).decode('utf-8')
            msgs = json.loads(msgs)
            for msg in msgs:
                master.messageBox.append(msg['time']+' ' + msg['source']+': '+msg['text'])
        except Exception as e:
            print('Connection closed!')
            break


class ClientPage(QWidget):

    def __init__(self):
        super().__init__()
        self._select_buttons = []
        self._chat_pages = []
        self.initUI()
        self.onLine()
    
    def __del__(self):
        self.offLine()
    
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

        self.setFixedSize(1280, 720)
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
        self.submit.clicked.connect(self.submitMsg)

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
        # 输入套接字
        self.inputSocket = QLineEdit()

        # 创建一个新的聊天页面
        self.connectButton = QToolButton()
        self.connectButton.setText('建立聊天')
        self.connectButton.clicked.connect(self.newConnect)

        # 显示连接服务器状态
        self.isConnected = QLabel()
        self.isConnected.setText('未连接')

        # 连接服务器
        self.connectServer = QToolButton()
        self.connectServer.setText('连接服务器')
        self.connectServer.clicked.connect(self.onLine)

        self.rightPageLayout = QVBoxLayout()
        self.rightPageLayout.addWidget(self.inputSocket)
        self.rightPageLayout.addWidget(self.connectButton)
        self.rightPageLayout.addWidget(self.isConnected)
        self.rightPageLayout.addWidget(self.connectServer)

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
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # 建立连接:
            self.socket.connect(('127.0.0.1', 9999))
            # 接收欢迎消息:
            self.messageBox.append(self.socket.recv(1024).decode('utf-8'))
            
            # 专门一个线程用于接受消息
            self.receiver = threading.Thread(target=recvMsg, args=(self,))
            self.receiver.start()

            # 设置页面信息
            self.setWindowTitle(f'欢迎登录: {self.socket.getsockname[0]}:{self.socket.getsockname[1]}')
            self.isConnected.setText('已连接')
        except Exception as e:
            print(e)
    
    def offLine(self):
        try:
            self.socket.send(b'exit')
            self.socket.close()
        except Exception as e:
            print(e)
    
    def submitMsg(self):
        '''
        客户端发送给服务端的数据格式
        {
            source:str,
            target:str,
            text:str,
            time:str,
            operation:str
        }
        operation:msg(发送信息)
        '''
        # 发送数据:
        msg = {
            'source':"%s:%d" % self.socket.getsockname(),
            'target':self.inputSocket.text(),
            'text':self.inputBox.toPlainText(),
            'time':str(datetime.datetime.now()),
            'operation':'msg'
        }
        try:
            self.socket.send(json.dumps(msg).encode())
            self.messageBox.append(str(datetime.datetime.now())+' 本机: '+ msg['text'])
            self.inputBox.clear()
        except Exception as e:
            self.messageBox.append(str(datetime.datetime.now())+' 发送失败')
            print(e)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ClientPage()
    sys.exit(app.exec_())
