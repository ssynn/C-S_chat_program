import sys
import time
import json
import socket
from PyQt5.QtWidgets import (QApplication, QWidget, QMessageBox)
from src import login
from src import signup
from src import database
from src import public_function as pf
from src import client_page as cp


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setLogin()
        self.body = None
        self.setGeometry(200, 200, 980, 720)
        self.setFixedSize(1000, 750)
        self.setMyStyle()

    # 创建登录菜单
    def setLogin(self):
        self.login = login.Login()
        self.login.setParent(self)
        self.login.move(240, 120)
        self.login.loginButton.clicked.connect(self.loginFunction)
        self.login.signup.clicked.connect(self.signupViewFunction)

    # 创建注册菜单
    def setSignup(self):
        self.signup = signup.Signup()
        self.signup.setParent(self)
        self.signup.setVisible(True)
        self.signup.move(275, 110)
        self.signup.back.clicked.connect(self.backToLogin)
        self.signup.submit.clicked.connect(self.signupFunction)

    # 登录按钮按下
    def loginFunction(self):
        _mes = self.login.getInfo()
        self.userInfo = {'ID':_mes['ID'], 'PASSWORD':_mes['PASSWORD']}
        self.socket = _mes['SOCKET']
        _mes['PASSWORD'] = pf.encrypt(_mes['PASSWORD'])
        self.isLogin = self.loginToServer(_mes)
        if self.isLogin:
            self.setWindowTitle('欢迎使用CS聊天程序：'+self.userInfo['ID'])
            self.login.setVisible(False)
            self.display()
            print('登录成功！')
        else:
            print('登录失败!')

    # 与服务器建立连接，验证用户的身份
    def loginToServer(self, info: dict):
        # 检查套接字是否输入正确
        if not pf.checkSocket(info['SOCKET']):
            self.errorBox('套接字错误')
            return False
        address = info['SOCKET'].split(':')

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # 建立连接:
            self.sock.connect((address[0], int(address[1])))

            msg = {
                'operation': 'login',
                'ID': info['ID'],
                'PASSWORD': info['PASSWORD']
            }

            self.sock.send(json.dumps(msg).encode())

            ans = self.sock.recv(1024).decode('utf-8')
            ans = json.loads(ans)

            if ans['answer'] == 'success':
                return True
            else:
                # 验证失败则与服务器断开连接
                self.sock.send(b'exit')
                self.sock.close()
                self.errorBox('用户名或密码错误')
                return False

        except Exception as e:
            self.errorBox('无法连接到服务器！')
            print(e)
            return False

    # 显示注册界面
    def signupViewFunction(self):
        self.login.setVisible(False)
        self.setSignup()

    # 注册按钮按下
    def signupFunction(self):
        '''
        获取注册信息后交由signinToServer（）与服务器通讯进行服务器注册
        '''
        if self.signup.passwordInput.text() != self.signup.repPasswordInput.text():
            print('密码不一致')
            return

        info = self.signup.getInfo()
        info['SOCKET'] = self.login.getInfo()['SOCKET']

        ans = self.signinToServer(info)

        if ans:
            self.errorBox('注册成功，请登录！')
            print('成功')
        else:
            print('注册失败')
    
    # 把注册信息发送给服务器进行注册
    def signinToServer(self, info: dict):
        # 检查套接字是否输入正确
        if not pf.checkSocket(info['SOCKET']):
            self.errorBox('套接字错误')
            return False
        address = info['SOCKET'].split(':')

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # 建立连接:
            sock.connect((address[0], int(address[1])))

            msg = {
                'time': str(time.strftime('%Y-%m-%d %H:%M:%S')),
                'operation': 'signup',
                'ID': info['ID'],
                'PASSWORD': info['PASSWORD']
            }

            sock.send(json.dumps(msg).encode())

            ans = sock.recv(1024).decode('utf-8')
            ans = json.loads(ans)

            # 验证完与服务器断开连接
            sock.send(b'exit')
            sock.close()

            if ans['answer'] == 'success':
                return True
            else:
                self.errorBox(ans['reason'])
                return False
        except Exception as e:
            self.errorBox('服务器错误！')
            print(e)
            return False

    def backToLogin(self):
        self.signup.setVisible(False)
        self.login.setVisible(True)

    def logout(self):
        self.body.close()
        self.login.setVisible(True)

    def display(self):
        # 显示登录界面
        self.body = cp.ClientPage(self.userInfo, self.sock, self.socket)
        self.body.setParent(self)
        self.body.setVisible(True)

    # 错误提示框
    def errorBox(self, mes: str):
        msgBox = QMessageBox(
            QMessageBox.Warning,
            "提示!",
            mes,
            QMessageBox.NoButton,
            self
        )
        msgBox.addButton("确认", QMessageBox.AcceptRole)
        msgBox.exec_()

    def closeEvent(self, a0):
        if self.body:
            self.body.offLine()

    def setMyStyle(self):
        self.setStyleSheet('''
        QWidget{
            background-color: white;
        }
        ''')

