import sys
import socket
import json
import threading
import time
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout, QSplitter,
                             QToolButton, QLabel, QVBoxLayout, QTextBrowser, QTextEdit, QLineEdit, QMessageBox)
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import Qt, QSize

# FIXME
'''
_chat_page 使用userID作为key
与用户通讯不再使用socket
source和target不再填写socket
'''

# TODO
'''
好友列表
申请好友
toolbutton显示用户名
接受好友请求
删除好友
'''

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
    接收信息并发送至对应的聊天窗口
    '''
    while True:
        try:
            msgs = master.socket.recv(2048).decode('utf-8')
            msgs = json.loads(msgs)
            target_page = None
            for page in master._chat_pages:
                if msgs[0]['source'] == page:
                    target_page = master._chat_pages[page][1]
                    break
            if target_page is None:
                continue
            master._chat_pages[page][0].setStyleSheet('''
                QToolButton{
                    border-left:9px solid yellow;
                }
            ''')
            for msg in msgs:
                target_page.messageBox.append(
                    msg['time']+' ' + msg['source']+': '+msg['text'])
        except Exception as e:
            print('Connection closed!')
            print(e)
            # 清空socket变量
            master.socket = None
            # 显示未连接到服务器
            master.isConnected.setText('未连接至服务器')
            master.isConnected.setStyleSheet('''
            QLabel{
                font-size:25px;
                font-family:微软雅黑;
                color:#D32F2F;
            }
        ''')
            break


class ClientPage(QWidget):

    def __init__(self, userID: str, sock, serverSocket):
        '''
        继承从main_widget建立的tcp连接，获取用户名，服务器套接字
        '''
        super().__init__()
        self.userID = userID
        self.socket = sock
        self.serverSocket = serverSocket
        self._chat_pages = dict()
        self.chatPageNow = None
        self.initUI()
        self.setMyStyleSheet()
        self.onLine()

    def closeEvent(self, a0):
        self.offLine()

    def initUI(self):
        self.selectList = QWidget()
        self.setSelectList()

        self.chatPage = QWidget()
        self.setChatPage()

        self.rightPage = QWidget()
        self.setRightPage()

        self.bodyLayout = QHBoxLayout()
        self.bodyLayout.addWidget(self.selectList)
        self.bodyLayout.addWidget(self.chatPage)
        self.bodyLayout.addWidget(self.rightPage)

        self.setLayout(self.bodyLayout)
        self.setWindowTitle('欢迎使用CS聊天程序：'+self.userID)

        self.setFixedSize(980, 720)
        # self.setMinimumSize(, 500)
        self.setContentsMargins(0, 0, 0, 0)
        # self.show()

    def setSelectList(self):
        self.selectListLayout = QVBoxLayout()
        self.selectListLayout.addStretch(100)
        self.selectList.setLayout(self.selectListLayout)
        self.selectList.setFixedWidth(200)
        self.selectListLayout.setContentsMargins(0, 0, 0, 0)

    def setChatPage(self):
        self.chatPage.setMinimumWidth(300)

    def createChatPageContents(self):
        # 消息框
        messageBox = QTextBrowser()
        messageBox.setFixedHeight(400)

        # 输入框
        inputBox = QTextEdit()

        # 设置操作按钮
        submit = QToolButton()
        submit.setText('发送')
        submit.setFixedSize(80, 30)
        submit.clicked.connect(self.submitMsg)
        submit.setStyleSheet('''
            QToolButton{
                color: #448AFF;
                border: 1px solid #448AFF;
                border-radius: 5px;
            }
            QToolButton:hover{
                background: #448AFF;
                color: white;
            }
        ''')

        closePage = QToolButton()
        closePage.setText('关闭')
        closePage.setFixedSize(80, 30)
        closePage.setStyleSheet('''
            QToolButton{
                color: #D32F2F;
                border: 1px solid #D32F2F;
                margin-right: 5px;
                border-radius: 5px;
            }
            QToolButton:hover{
                background: #D32F2F;
                color: white;
            }
        ''')

        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(closePage)
        buttons.addWidget(submit)

        chatPageLayout = QVBoxLayout()
        chatPageLayout.addWidget(messageBox)
        chatPageLayout.addWidget(inputBox)
        chatPageLayout.addLayout(buttons)
        chatPageLayout.setContentsMargins(0, 0, 0, 0)

        chatPage = QWidget()
        chatPage.messageBox = messageBox
        chatPage.inputBox = inputBox
        chatPage.closePage = closePage
        chatPage.submit = submit
        chatPage.setLayout(chatPageLayout)
        chatPage.setFixedSize(500, 650)
        chatPage.setContentsMargins(0, 0, 0, 0)

        return chatPage

    def closePageFunction(self, sock):
        chatButton, chatPage = self._chat_pages[sock]
        self.selectListLayout.removeWidget(chatButton)
        chatButton.deleteLater()
        chatPage.deleteLater()
        self._chat_pages.pop(sock)

    def setRightPage(self):
        # 输入套接字
        self.inputSocket = QLineEdit()
        self.inputSocket.setText('输入套接字')
        self.inputSocket.setFixedSize(180, 40)

        # 创建一个新的聊天页面
        self.connectButton = QToolButton()
        self.connectButton.setText('建立聊天')
        self.connectButton.clicked.connect(self.newConnect)
        self.connectButton.setFixedSize(180, 50)

        # 显示连接服务器状态
        self.isConnected = QLabel()
        self.isConnected.setFixedSize(180, 40)
        self.isConnected.setText('未连接服务器')

        # 连接服务器
        self.connectServer = QToolButton()
        self.connectServer.setFixedSize(180, 50)
        self.connectServer.setText('连接服务器')
        self.connectServer.clicked.connect(self.onLine)

        self.rightPageLayout = QVBoxLayout()
        self.rightPageLayout.addWidget(self.inputSocket)
        self.rightPageLayout.addWidget(self.connectButton)
        self.rightPageLayout.addSpacing(50)
        self.rightPageLayout.addWidget(self.isConnected)
        self.rightPageLayout.addWidget(self.connectServer)
        self.rightPageLayout.addStretch(10)

        self.rightPage.setFixedWidth(200)
        self.rightPage.setLayout(self.rightPageLayout)

    def newConnect(self):
        '''
        创建新的聊天界面
        '''

        if self.inputSocket.text() in self._chat_pages:
            self.refresh(self.inputSocket.text())
            return

        # 创建选择按钮
        newChatButton = QToolButton()
        newChatButton.setText(self.inputSocket.text())
        newChatButton.setFixedSize(200, 50)
        newChatButton.clicked.connect(
            lambda: self.refresh(newChatButton.text()))

        # 创建聊天页面
        newchatPage = self.createChatPageContents()
        newchatPage.setParent(self.chatPage)
        newchatPage.socketName = self.inputSocket.text()

        # 把建立的聊天页面加入列表
        self._chat_pages[self.inputSocket.text()] = (
            newChatButton, newchatPage)
        newchatPage.closePage.clicked.connect(
            lambda: self.closePageFunction(newchatPage.socketName))

        # 创建选择按钮
        self.selectListLayout.insertWidget(0, newChatButton)

        self.refresh(self.inputSocket.text())

    def refresh(self, socketName):
        '''
        展示当前选择的页面
        '''
        # print(socketName)
        for sock in self._chat_pages:
            self._chat_pages[sock][1].setVisible(False)
            self._chat_pages[sock][0].setStyleSheet('''
            *{
                background: white;
                border-left:9px solid rgba(230, 230, 230);
            }
            QToolButton:hover{
                background-color: rgba(230, 230, 230, 0.3);
            }
            ''')
        for sock in self._chat_pages:
            if sock == socketName:
                self.chatPageNow = self._chat_pages[sock][1]
                self._chat_pages[sock][1].setVisible(True)
                self._chat_pages[sock][0].setStyleSheet('''
                QToolButton{
                    background-color: rgba(230, 230, 230, 0.7);
                    border-left:9px solid green;
                }
                ''')

                break

    def onLine(self):
        '''
        连接服务器
        '''
        try:
            if self.socket is None:
                # 建立新的连接:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect(('127.0.0.1', 9999))

            # 专门一个线程用于接受消息
            self.receiver = threading.Thread(target=recvMsg, args=(self,))
            self.receiver.start()

            # 设置页面信息
            self.isConnected.setText('已连接至服务器')
            self.isConnected.setStyleSheet('''
            QLabel{
                font-size:25px;
                font-family:微软雅黑;
                color:#689F38;
            }
        ''')
        except Exception as e:
            print('连接出现错误')
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
            'source': "%s:%d" % self.socket.getsockname(),
            'target': self.chatPageNow.socketName,
            'text': self.chatPageNow.inputBox.toPlainText(),
            'time': str(time.strftime('%Y-%m-%d %H:%M:%S')),
            'operation': 'msg'
        }
        try:
            self.socket.send(json.dumps(msg).encode())
            self.chatPageNow.messageBox.append(
                str(time.strftime('%Y-%m-%d %H:%M:%S'))+' 本机: ' + msg['text'])
            self.chatPageNow.inputBox.clear()
        except Exception as e:
            self.chatPageNow.messageBox.append(
                str(time.strftime('%Y-%m-%d %H:%M:%S'))+' 发送失败')
            print(e)

    # 错误提示框
    def errorBox(self, mes: str):
        msgBox = QMessageBox(
            QMessageBox.Warning,
            "警告!",
            mes,
            QMessageBox.NoButton,
            self
        )
        msgBox.addButton("确认", QMessageBox.AcceptRole)
        msgBox.exec_()

    def setMyStyleSheet(self):
        self.setStyleSheet('''
        QWidget{
            background-color:white;
        }
        ''')
        self.selectList.setStyleSheet('''
            QWidget{
            border: 0px;
            border-right: 1px solid rgba(227, 227, 227, 1);
            }
            QToolButton{
                color: rgba(51, 90, 129, 1);
                font-family: 微软雅黑;
                font-size: 25px;
                border-right: 1px solid rgba(227, 227, 227, 1);
            }
            QToolButton:hover{
                background-color: rgba(230, 230, 230, 0.3);
            }
            '''
                                      )
        self.connectButton.setStyleSheet('''
            QToolButton{
                border-radius:10px;
                border:1px solid #4CAF50;
                background-color:white;
                color:#4CAF50;
                font-size:20px;
                font-family:微软雅黑;
            }
            QToolButton:hover{
                background-color:#4CAF50;
                color:white;
            }
        ''')
        self.isConnected.setStyleSheet('''
            QLabel{
                font-size:25px;
                font-family:微软雅黑;
                color:#D32F2F;
            }
        ''')
        self.connectServer.setStyleSheet('''
            QToolButton{
                border-radius:10px;
                border:1px solid #0288D1;
                background-color:white;
                color:#0288D1;
                font-size:20px;
                font-family:微软雅黑;
            }
            QToolButton:hover{
                background-color:#0288D1;
                color:white;
            }
        ''')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ClientPage()
    sys.exit(app.exec_())
