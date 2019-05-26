import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QLineEdit, QToolButton, QPushButton)
from PyQt5.QtCore import Qt


class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.bodyLayout = QGridLayout()

        # 欢迎登陆图书馆系统标题
        self.titleText = QLabel(self)
        self.titleText.setText('欢迎使用CS聊天系统')
        self.titleText.setAlignment(Qt.AlignCenter)
        self.titleText.setFixedSize(480, 60)

        # 账号标题
        account = QLabel()
        account.setText('账号')

        # 密码标题
        password = QLabel()
        password.setText('密码')

        # 服务器标题
        server = QLabel()
        server.setText('服务器地址')

        # 学号输入框
        self.accountInput = QLineEdit()
        self.accountInput.setFixedSize(400, 50)
        self.accountInput.setText('学号')
        self.accountInput.setTextMargins(5, 5, 5, 5)
        self.accountInput.mousePressEvent = lambda x: self.inputClick(self.accountInput)
        # self.accountInput.setClearButtonEnabled(True)

        # 密码输入框
        self.passwordInput = QLineEdit()
        self.passwordInput.setFixedSize(400, 50)
        self.passwordInput.setText('******')
        self.passwordInput.setTextMargins(5, 5, 5, 5)
        self.passwordInput.mousePressEvent = lambda x: self.inputClick(self.passwordInput)
        self.passwordInput.setEchoMode(QLineEdit.Password)
        # self.passwordInput.setClearButtonEnabled(True)

        # 服务器地址输入
        self.serverAddress = QLineEdit()
        self.serverAddress.setFixedSize(400, 50)
        self.serverAddress.setTextMargins(5,5,5,5)
        self.serverAddress.setText('127.0.0.1:9999')
        # self.serverAddress.mousePressEvent = lambda x: self.inputClick(self.serverAddress)

        # 注册按钮
        self.signup = QPushButton()
        self.signup.setText('注册')
        self.signup.setFixedSize(40, 20)

        # 登录按钮
        self.loginButton = QToolButton()
        self.loginButton.setText('登  录')
        self.loginButton.setFixedSize(100, 60)

        # 把上面定义的元素加入大框
        self.inputBoxLayout = QVBoxLayout()
        self.inputBoxLayout.addWidget(account)
        self.inputBoxLayout.addWidget(self.accountInput)
        self.inputBoxLayout.addWidget(password)
        self.inputBoxLayout.addWidget(self.passwordInput)
        self.inputBoxLayout.addWidget(server)
        self.inputBoxLayout.addWidget(self.serverAddress)
        self.inputBoxLayout.addWidget(self.signup)
        self.inputBoxLayout.addWidget(self.loginButton)

        # 下面一个大框
        self.inputBox = QWidget()
        self.inputBox.setObjectName('inputBox')
        self.inputBox.setContentsMargins(30, 30, 30, 30)
        self.inputBox.setFixedSize(480, 400)
        self.inputBox.setLayout(self.inputBoxLayout)

        # 把大标题和下面输入框加入self
        self.bodyLayout.addWidget(self.titleText, 0, 0)
        self.bodyLayout.addWidget(self.inputBox, 1, 0)
        self.setLayout(self.bodyLayout)
        self.setFixedSize(500, 500)
        self.setMyStyle()

    def inputClick(self, e):
        if e.text() == '学号' or e.text() == '******':
            e.setText('')

    def getInfo(self):
        return {
            'ID': self.accountInput.text(),
            'PASSWORD': self.passwordInput.text(),
            'SOCKET': self.serverAddress.text()
        }

    def setMyStyle(self):
        self.setStyleSheet('''
            QWidget{
                background-color:white;
            }
        ''')
        self.titleText.setStyleSheet('''
            *{
                color: rgba(63, 101, 114);
                width: 200px;
                background-color: rgba(203, 231, 245, 1);
                border: 1px solid rgba(220, 243, 249, 1);
                border-radius: 10px;
            }
        ''')
        self.inputBox.setStyleSheet('''
        QWidget#inputBox{
            border-radius: 5px;
            border: 1px solid rgba(229, 229, 229, 1);
        }
        QLineEdit{
            color: grey;
            border-radius: 5px;
            border: 1px solid rgba(229, 229, 229, 1);
        }
        QToolButton{
            border-radius: 10px;
            background-color:rgba(52, 118, 176, 1);
            color: white;
            font-size: 25px;
            font-family: 微软雅黑;
        }
        QPushButton{
            color:blue;
            font-weight:300;
            border:0;
            background-color:white;
        }
        ''')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Login()
    ex.show()
    sys.exit(app.exec_())
