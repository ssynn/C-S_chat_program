import sys
from PyQt5.QtWidgets import (QApplication, QVBoxLayout, QLabel, QLineEdit, QToolButton, QGroupBox)


class Signup(QGroupBox):
    def __init__(self):
        super().__init__()

        self.title = QLabel()
        self.title.setText('注册用户')

        self.subTitle = QLabel()
        self.subTitle.setText('创建一个新的账户')

        account = QLabel()
        account.setText('账号')

        password = QLabel()
        password.setText('密码')

        repPassword = QLabel()
        repPassword.setText('重复密码')

        # 账号输入框
        self.accountInput = QLineEdit()
        self.accountInput.setFixedSize(400, 40)
        self.accountInput.setText('请输入账号')
        self.accountInput.initText = '请输入账号'
        self.accountInput.setTextMargins(5, 5, 5, 5)
        self.accountInput.mousePressEvent = lambda x: self.inputClick(self.accountInput)

        # 密码
        self.passwordInput = QLineEdit()
        self.passwordInput.setFixedSize(400, 40)
        self.passwordInput.setText('请输入密码')
        self.passwordInput.initText = '请输入密码'
        self.passwordInput.setTextMargins(5, 5, 5, 5)
        self.passwordInput.mousePressEvent = lambda x: self.inputClick(self.passwordInput)

        # 重复密码
        self.repPasswordInput = QLineEdit()
        self.repPasswordInput.setFixedSize(400, 40)
        self.repPasswordInput.setText('请重复输入密码')
        self.repPasswordInput.initText = '请重复输入密码'
        self.repPasswordInput.setTextMargins(5, 5, 5, 5)
        self.repPasswordInput.mousePressEvent = lambda x: self.inputClick(self.repPasswordInput)

        # 提交
        self.submit = QToolButton()
        self.submit.setText('提交')
        self.submit.setFixedSize(400, 40)

        # 返回登录
        self.back = QToolButton()
        self.back.setText('返回登录')
        self.back.setFixedSize(400, 40)

        self.bodyLayout = QVBoxLayout()
        self.bodyLayout.addWidget(self.title)
        self.bodyLayout.addWidget(self.subTitle)
        self.bodyLayout.addWidget(self.accountInput)
        self.bodyLayout.addWidget(self.passwordInput)
        self.bodyLayout.addWidget(self.repPasswordInput)
        self.bodyLayout.addWidget(self.submit)
        self.bodyLayout.addWidget(self.back)

        self.setLayout(self.bodyLayout)
        self.initUI()

    def inputClick(self, e):
        for i in range(2, 5):
            item = self.bodyLayout.itemAt(i).widget()
            if item.text() == '':
                item.setText(item.initText)
                if item is self.passwordInput or item is self.repPasswordInput:
                    item.setEchoMode(QLineEdit.Normal)

        if e.text() == e.initText:
            e.setText('')
        if e is self.passwordInput or e is self.repPasswordInput:
            e.setEchoMode(QLineEdit.Password)

    def initUI(self):
        self.setFixedSize(422, 350)
        self.setWindowTitle('注册')
        self.setMyStyle()

    def getInfo(self):
        return {
            'ID':self.accountInput.text(),
            'PASSWORD':self.passwordInput.text()
        }

    def setMyStyle(self):
        self.setStyleSheet('''
        QWidget{
            background-color: white;
        }
        QLineEdit{
            border:0px;
            border-bottom: 1px solid rgba(229, 229, 229, 1);
            color: grey;
        }
        QToolButton{
            border:0;
            background-color:rgba(50, 198, 212, 1);
            color: white;
            font-size: 20px;
            font-family: 微软雅黑;
        }
        QGroupBox{
            border: 1px solid rgba(229, 229, 229, 1);
            border-radius: 5px;
        }
        ''')
        self.title.setStyleSheet('''
        *{
            color: rgba(113, 118, 121, 1);
            font-size: 30px;
            font-family: 微软雅黑;
        }
        ''')
        self.subTitle.setStyleSheet('''
        *{
            color: rgba(184, 184, 184, 1);
        }
        ''')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Signup()
    ex.show()
    sys.exit(app.exec_())
