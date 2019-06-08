import sys
import socket
import json
import threading
import time
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout, QSplitter,
                             QTableWidget, QTableWidgetItem, QAbstractItemView,
                             QToolButton, QLabel, QVBoxLayout, QTextBrowser,
                             QTextEdit, QLineEdit, QMessageBox, QHeaderView,
                             QInputDialog, QMenu, QAction)
from PyQt5.QtGui import QIcon, QColor, QFont, QCursor
from PyQt5.QtCore import Qt, QSize, QThread, pyqtSignal
from src import public_function as pf

# FIXME
'''

'''

# TODO
'''
打开未读消息的窗口
接受好友请求
删除好友
'''


class ClientPage(QWidget):
    def __init__(self, userInfo: dict, sock, serverSocket):
        '''
        继承从main_widget建立的tcp连接
        传入用户ID，TCP连接，服务器套接字
        '''
        super().__init__()
        self.userID = userInfo['ID']
        self.userInfo = userInfo
        self.socket = sock
        self.serverSocket = serverSocket
        self._chat_pages = dict()
        self.chatPageNow = None
        self._unread_buffer = []
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

    def closePageFunction(self, userID):
        chatButton, chatPage = self._chat_pages[userID]
        self.selectListLayout.removeWidget(chatButton)
        chatButton.deleteLater()
        chatPage.deleteLater()
        self._chat_pages.pop(userID)

    def setRightPage(self):
        '''
        设置右边的元素
        '''

        self.friendsList = QTableWidget(1, 1)
        self.friendsList.horizontalHeader().setVisible(False)
        self.friendsList.verticalHeader().setVisible(False)
        self.friendsList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.friendsList.setFocusPolicy(Qt.NoFocus)
        # self.friendsList.setColumnWidth(0, 150)
        self.friendsList.setShowGrid(False)
        self.friendsList.setFixedWidth(180)
        self.friendsList.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.friendsList.verticalScrollBar().setStyleSheet('''
            QScrollBar{background:transparent; width: 10px;}
            QScrollBar::handle{background:lightgray; border:2px solid transparent; border-radius:5px;}
            QScrollBar::handle:hover{background:gray;}
            QScrollBar::sub-line{background:transparent;}
            QScrollBar::add-line{background:transparent;}
        ''')

        self.friendHead = QToolButton()
        self.friendHead.setText('好友列表')
        self.friendHead.setFixedSize(180, 50)
        self.friendHead.clicked.connect(self.getFrineds)

        self.friendsList.setCellWidget(0, 0, self.friendHead)
        self.friendsList.setRowHeight(0, 50)

        self.rightPageLayout = QVBoxLayout()
        self.rightPageLayout.addWidget(self.friendsList)
        self.setMenuBar()

        self.rightPage.setFixedWidth(200)
        self.rightPage.setLayout(self.rightPageLayout)

    def setMenuBar(self):
        self.friend = QToolButton()
        self.friend.setIcon(QIcon('icon/newFriend.png'))
        self.friend.setFixedSize(40, 40)
        self.friend.setIconSize(QSize(40, 40))
        self.friend.clicked.connect(self.makeFriends)

        self.newMessage = QToolButton()
        self.newMessage.setIcon(QIcon('icon/msg.png'))
        self.newMessage.setFixedSize(45, 40)
        self.newMessage.setIconSize(QSize(40, 40))
        self.newMessage.clicked.connect(self.openUnreadMessage)

        self.isConnected = QToolButton()
        self.isConnected.setFixedSize(70, 40)
        self.isConnected.clicked.connect(self.onLine)

        self.menuBarLayout = QHBoxLayout()
        self.menuBarLayout.addWidget(self.friend)
        self.menuBarLayout.addWidget(self.newMessage)
        self.menuBarLayout.addWidget(self.isConnected)
        self.menuBarLayout.setContentsMargins(0, 0, 0, 0)

        self.menuBar = QWidget()
        self.menuBar.setLayout(self.menuBarLayout)
        self.menuBar.setFixedHeight(40)
        self.menuBar.setContentsMargins(0, 0, 0, 0)

        self.rightPageLayout.addWidget(self.menuBar)

    def makeFriends(self):
        '''
        添加好友方法
        单方面添加好友
        '''
        text, ok = QInputDialog.getText(self, '添加好友:', '输入好友ID')
        if ok and len(text) != 0:
            msg = {
                'operation': 'makeFriends',
                'ID': text
            }
            self.socket.send(json.dumps(msg).encode())

    def newPage(self, userID, needRefresh=True):
        '''
        双击好友的图标, 传入用户ID
        创建新的聊天界面
        '''
        if userID in self._chat_pages:
            self.refresh(userID)
            return

        # 创建选择按钮 应该显示用户ID
        newChatButton = QToolButton()
        newChatButton.setText(userID)
        newChatButton.setFixedSize(200, 50)
        newChatButton.clicked.connect(
            lambda: self.refresh(newChatButton.text()))

        # 创建聊天页面 记录用户ID
        newchatPage = self.createChatPageContents()
        newchatPage.setParent(self.chatPage)
        newchatPage.userID = userID

        # 把建立的聊天页面加入列表 key值为用户ID, value为（选择按钮，聊天界面）
        self._chat_pages[userID] = (
            newChatButton, newchatPage)
        newchatPage.closePage.clicked.connect(
            lambda: self.closePageFunction(userID))

        # 创建选择按钮
        self.selectListLayout.insertWidget(0, newChatButton)

        if needRefresh or self.chatPageNow is None:
            self.refresh(userID)
        else:
            pass

    def refresh(self, userID):
        '''
        隐藏其他聊天页面
        显示当前选择的页面
        '''

        for UID in self._chat_pages:
            self._chat_pages[UID][1].setVisible(False)
            self._chat_pages[UID][0].setStyleSheet('''
            *{
                background: white;
                border-left:9px solid rgba(230, 230, 230);
            }
            QToolButton:hover{
                background-color: rgba(230, 230, 230, 0.3);
            }
            ''')

        for UID in self._chat_pages:
            if UID == userID:
                self.chatPageNow = self._chat_pages[UID][1]
                self._chat_pages[UID][1].setVisible(True)
                self._chat_pages[UID][0].setStyleSheet('''
                QToolButton{
                    background-color: rgba(230, 230, 230, 0.7);
                    border-left:9px solid green;
                }
                ''')

                break

    def getFrineds(self):
        if self.socket:
            self.socket.send(json.dumps({'operation': 'getFriends'}).encode())

    def onLine(self):
        '''
        连接服务器
        '''
        try:
            # 如果连接已经断开,则与服务器新建立一个TCP连接
            if self.socket is None:
                # 建立新的连接:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect(pf.split_socket(self.serverSocket))
                msg = {
                    'time': str(time.strftime('%Y-%m-%d %H:%M:%S')),
                    'operation': 'login',
                    'ID': self.userInfo['ID'],
                    'PASSWORD': self.userInfo['PASSWORD']
                }
                self.socket.send(json.dumps(msg).encode())
                data = self.socket.recv(2048).decode('utf-8')

            # 获取好友列表
            self.socket.send(json.dumps({'operation': 'getFriends'}).encode())

            # 专门一个线程用于接受消息
            self.receiver = RecvMsg(self)
            self.receiver.refreshFriends.connect(self.makeFriendList)
            self.receiver.messages.connect(self.errorBox)
            self.receiver.unreadMessages.connect(
                lambda m: self.unreadMessages(m))
            self.receiver.start()

            # 设置在线显示
            self.setOnlineStyle()

        except Exception as e:
            print('连接出现错误')
            print(e)
            self.socket = None
            self.setOfflineStyle()

    def unreadMessages(self, msgs: list):
        '''
        收到了没有建立聊天窗口的消息，由这个方法处理
        '''
        self.newMessage.setStyleSheet('''
            background-color:#FFEB3B;
        ''')
        self._unread_buffer += msgs

    def openUnreadMessage(self, msgs: list):
        '''
        打开对应未读消息的窗口
        对于每一条消息 
        if 没有打开对应的窗口：
            新建窗口
        添加消息
        '''
        self.newMessage.setStyleSheet('''
            background-color:white;
        ''')
        for item in self._unread_buffer:
            if item['source'] not in self._chat_pages:
                self.newPage(item['source'], False)

            # 先找到对应的聊天页面
            target_page = None
            if item['source'] in self._chat_pages:
                target_page = self._chat_pages[item['source']][1]

            # 如果对应的聊天页面没有开启则进入缓冲列表
            if target_page is None:
                self.unreadMessages.emit(item['message'])

            # 收到消息的页面会有黄色提示
            self._chat_pages[item['source']][0].setStyleSheet('''
                QToolButton{
                    border-left:9px solid yellow;
                }
                QToolButton:hover{
                    background-color: rgba(230, 230, 230, 0.3);
                }
            ''')
            target_page.messageBox.append(
                item['time']+' ' + item['source']+': '+item['text'])

    def makeFriendList(self, friends: list, isOnline: list):
        '''
        把好友信息显示到用户界面上
        '''
        print(friends, isOnline)
        while self.friendsList.rowCount() != 1:
            self.friendsList.removeRow(1)
        for i in range(len(friends)):
            if isOnline[i] == 0:
                self.friendsList.insertRow(1)
                self.friendsList.setRowHeight(1, 50)
                self.friendsList.setCellWidget(
                    1, 0, self.makeFriendButton(friends[i], 0))

        for i in range(len(friends)):
            if isOnline[i] == 1:
                self.friendsList.insertRow(1)
                self.friendsList.setRowHeight(1, 50)
                self.friendsList.setCellWidget(
                    1, 0, self.makeFriendButton(friends[i], 1))

    def makeFriendButton(self, userID: str, isOnline: int):
        return FriendButton(self, userID, isOnline)

    def deleteFriend(self, userID: str):
        msg = {
            'operation': 'deleteFriend',
            'friend':userID
        }
        self.socket.send(json.dumps(msg).encode())
        print(f'delete: {userID}')
        self.getFrineds()

    def offLine(self):
        try:
            self.socket.send(b'exit')
            self.socket.close()
            self.socket = None
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
            'source': self.userID,
            'target': self.chatPageNow.userID,
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

    def setOfflineStyle(self):
        self.isConnected.setText('离线')
        self.isConnected.setStyleSheet('''
            QToolButton{
                font-size:25px;
                font-family:微软雅黑;
                color:#FF5252;
            }
            QToolButton:hover{
                background-color:#FF5252;
                color:white;
            }
        ''')

    def setOnlineStyle(self):
        self.isConnected.setText('在线')
        self.isConnected.setStyleSheet('''
            QToolButton{
                font-size:25px;
                font-family:微软雅黑;
                color:#00796B;
            }
            QToolButton:hover{
                background-color:#00796B;
                color:white;
            }
        ''')

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
        self.rightPage.setStyleSheet('''
            QTableWidget{
                border:0px;
                
            }
            QWidget{
                border:0px;
                border-left:1px solid #BDBDBD;
            }
        ''')
        self.menuBar.setStyleSheet('''
            QToolButton{
                border:0px;
            }
            QToolButton:hover{
                background-color: rgba(230, 230, 230, 1);
            }
            QWidget{
                border:0px;
            }
        ''')
        self.friendsList.setStyleSheet('''
            QTableWidget{
                border:0px;
            }
            QToolButton{
                border:0px;
                font-family: 微软雅黑;
                font-size: 20px;
            }
            QToolButton:hover{
                background-color: rgba(230, 230, 230, 0.3);
                
            }
        ''')
        self.friendHead.setStyleSheet('''
        QToolButton{
            border:0px;
            font-family: 微软雅黑;
            font-size: 20px;
        }
        ''')

        # self.connectServer.setStyleSheet('''
        #     QToolButton{
        #         border-radius:10px;
        #         border:1px solid #0288D1;
        #         background-color:white;
        #         color:#0288D1;
        #         font-size:20px;
        #         font-family:微软雅黑;
        #     }
        #     QToolButton:hover{
        #         background-color:#0288D1;
        #         color:white;
        #     }
        # ''')

    def setGetMessageStyleSheet(self, userID):
        if self.chatPageNow.userID != userID:
            self._chat_pages[userID][0].setStyleSheet('''
                QToolButton{
                    border-left:9px solid yellow;
                }
            ''')


class RecvMsg(QThread):
    refreshFriends = pyqtSignal(list, list)
    messages = pyqtSignal(str)
    unreadMessages = pyqtSignal(list)

    def __init__(self, master: ClientPage):
        super().__init__()
        self.master = master

    def run(self):
        '''
        返回的消息格式为
        {
            'operation':'msg',
            'message':list
        }
        message: [
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
        msgs = None
        while True:
            try:
                msgs = self.master.socket.recv(2048).decode('utf-8')
                msgs = json.loads(msgs)

                # 接收消息
                if msgs['operation'] == 'msg':
                    # 先找到对应的聊天页面
                    target_page = None
                    if msgs['source'] in self.master._chat_pages:
                        target_page = self.master._chat_pages[msgs['source']][1]

                    # 如果对应的聊天页面没有开启则进入缓冲列表
                    if target_page is None:
                        self.unreadMessages.emit(msgs['message'])
                        continue

                    # 收到消息的页面会有黄色提示
                    self.master.setGetMessageStyleSheet(msgs['source'])

                    # 把消息填入消息框
                    for msg in msgs['message']:
                        target_page.messageBox.append(
                            msg['time']+' ' + msg['source']+': '+msg['text'])

                # 接收服务器结果
                if msgs['operation'] == 'ans':
                    pass

                # 刷新好友列表
                if msgs['operation'] == 'getFriends':
                    self.refreshFriends.emit(msgs['friends'], msgs['state'])

                # 添加好友的结果
                if msgs['operation'] == 'makeFriends':
                    if msgs['answer'] == 'success':
                        self.master.socket.send(json.dumps(
                            {'operation': 'getFriends'}).encode())
                        self.messages.emit('添加成功')
                    else:
                        self.messages.emit(msgs['reason'])

                # 服务器通知客户端刷新好友列表
                if msgs['operation'] == 'refresh':
                    self.master.socket.send(json.dumps(
                        {'operation': 'getFriends'}).encode())

            except Exception as e:
                print('Connection closed!')
                print(msgs)
                print(e)
                # 清空socket变量
                self.master.socket = None
                # 显示未连接到服务器
                self.master.setOfflineStyle()
                break


class FriendButton(QToolButton):
    def __init__(self, master: ClientPage, userID: str, isOnline: int):
        super().__init__()
        self.master = master
        self.userID = userID
        self.setIcon(QIcon('icon/friend.png'))
        self.setText('%010s %s' % (userID, '在线' if isOnline else '离线'))
        self.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.setIconSize(QSize(40, 40))
        self.setFixedSize(180, 50)
        # 根据是否上线设置按钮边框
        if isOnline == 1:
            self.setStyleSheet('''
                QToolButton{
                    border-left:9px solid #03A9F4;
                }
            ''')
        else:
            self.setStyleSheet('''
                QToolButton{
                    border-left:9px solid rgba(230, 230, 230);
                }
            ''')

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.master.newPage(self.userID)
        else:
            self.context()

    def context(self):
        item = QAction('删除好友', self)
        item.triggered.connect(lambda:self.master.deleteFriend(self.userID))

        menu = QMenu()
        menu.addAction(item)
        menu.exec_(QCursor.pos())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = ClientPage()
    sys.exit(app.exec_())
