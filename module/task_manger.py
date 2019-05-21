import sys
from PyQt5.QtWidgets import (QApplication, QWidget,
                             QHBoxLayout, QSplitter, QToolButton, QLabel, QVBoxLayout, QGroupBox)
from PyQt5.QtGui import QIcon, QPainter, QColor
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QTimer


class TaskManger(QWidget):

    after_close_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.focus = 0
        self.initUI()

    def initUI(self):
        # self.setWindowIcon(QIcon('icon/task.png'))
        self.content = QWidget()

        self.cpuWidget = QWidget()
        self.cpuWidget.setParent(self.content)
        self.cpuWidget.setVisible(True)

        self.diskPage = QWidget()
        self.diskPage.setParent(self.content)
        self.diskPage.setVisible(False)

        self.body = QSplitter()
        self.body.setFixedHeight(710)
        self.body.setContentsMargins(0, 0, 0, 0)

        self.setLeftMunu()
        self.body.addWidget(self.content)

        self.setContent()

        self.bodyLayout = QHBoxLayout()
        self.bodyLayout.addWidget(self.body)

        self.setLayout(self.bodyLayout)
        self.setWindowTitle('资源管理器')

        self.setFixedSize(1280, 720)
        self.setContentsMargins(0, 0, 0, 0)
        self.setMyStyle()
        self.show()

    # 左侧菜单栏
    def setLeftMunu(self):
        # CPU
        self.CPU = QToolButton()
        self.CPU.setText('CPU')
        self.CPU.setFixedSize(160, 50)
        self.CPU.setIcon(QIcon('icon/cpu.png'))
        self.CPU.setIconSize(QSize(40, 40))
        self.CPU.clicked.connect(
            lambda: self.switch(0, self.CPU))
        self.CPU.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        # 磁盘
        self.disk = QToolButton()
        self.disk.setText('磁盘')
        self.disk.setFixedSize(160, 50)
        self.disk.setIcon(QIcon('icon/disk.png'))
        self.disk.setIconSize(QSize(40, 40))
        self.disk.clicked.connect(lambda: self.switch(1, self.disk))
        self.disk.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)

        self.btnList = [
            self.CPU,
            self.disk
        ]

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.CPU)
        self.layout.addWidget(self.disk)
        self.layout.addStretch()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.menu = QGroupBox()
        self.menu.setFixedSize(160, 650)
        self.menu.setLayout(self.layout)
        self.menu.setContentsMargins(0, 0, 0, 0)
        self.body.addWidget(self.menu)

    # 切换视图事件
    def switch(self, index, btn):
        self.focus = index
        self.setClickedStyle(btn)
        self.setContent()

    # 关闭事件
    def closeEvent(self, e):
        self.after_close_signal.emit()

    # 设置右侧信息页
    def setContent(self):
        if self.focus == 0:
            self.diskPage.setVisible(False)
            self.cpuWidget.setVisible(True)
        elif self.focus == 1:
            self.cpuWidget.setVisible(False)
            self.diskPage.setVisible(True)

    def setMyStyle(self):
        self.setStyleSheet('''
        QWidget{
            background-color: white;
        }
        ''')
        self.menu.setStyleSheet('''
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
        ''')

    def setClickedStyle(self, btn):
        for i in self.btnList:
            i.setStyleSheet('''
            *{
                background: white;
            }
            QToolButton:hover{
                background-color: rgba(230, 230, 230, 0.3);
            }
            ''')

        btn.setStyleSheet('''
        QToolButton{
            background-color: rgba(230, 230, 230, 0.7);
        }
        ''')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TaskManger()
    # ex.show()
    sys.exit(app.exec_())
