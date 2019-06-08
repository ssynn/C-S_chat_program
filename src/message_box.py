import sys
import socket
import json
import threading
import time
from PyQt5.QtWidgets import (QApplication, QWidget, QHBoxLayout, QHeaderView,
                             QTableWidget, QAbstractItemView,
                             QLabel)
from PyQt5.QtGui import QFont, QCursor, QFontMetrics
from PyQt5.QtCore import Qt,  QRect


class MessageBox(QTableWidget):
    def __init__(self):
        super().__init__(0, 1)
        self.setFixedSize(500, 400)
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setFocusPolicy(Qt.NoFocus)
        self.setShowGrid(False)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.verticalScrollBar().setStyleSheet('''
            QScrollBar{background:transparent; width: 10px;}
            QScrollBar::handle{background:lightgray; border:2px solid transparent; border-radius:5px;}
            QScrollBar::handle:hover{background:gray;}
            QScrollBar::sub-line{background:transparent;}
            QScrollBar::add-line{background:transparent;}
        ''')

        # self.append(
        #     '哇哇哇哇哇哇哇哇\n哇哇哇哇哇\nn哇\n哇哇哇哇\n哇哇哇哇\n\阿斯顿哇哇哇哇哇哇\n哇哇哇哇哇哇哇哇哇哇哇哇哇', 0)
        # self.append('2888 88888 8888\n8\n8sadasdadasd\n8888 ', 1)
        # self.append('2888 88888 8888\n8\n8sadasdadasd\n8888 ', 1)
        # self.append('2888 88888 8888\n8\n8sadasdadasd\n8888 ', 1)
        # self.append('2888 88888 8888\n8\n8sadasdadasd\n8888 ', 1)
        # self.append('2888 88888 8888\n8\n8sadasdadasd\n8888 ', 1)
        # self.append('2888 88888 8888\n8\n8sadasdadasd\n8888 ', 1)

    def append(self, msg: str, source: int):
        '''
        source：0 对方，1 自己
        '''
        bubble = self.createBubble(msg, source)
        self.insertRow(self.rowCount())
        self.setRowHeight(self.rowCount()-1, bubble.height())
        self.setCellWidget(self.rowCount()-1, 0, bubble)
        self.verticalScrollBar().setValue(self.rowCount())
        self.setMyStyle()

    def createBubble(self, msg: str, source: int):
        '''
        对文字按行分割
        对每一行文字如果宽度大于450则对行分割
        统计行最宽值
        累加行高
        '''
        font = QFont()
        font.setFamily('微软雅黑')
        font.setPixelSize(20)
        fm = QFontMetrics(font)

        lines = msg.splitlines()
        text = []
        height = 0
        width = 0

        while len(lines) != 0:
            # print(len(lines), lines)
            length = 15
            line = lines[0]
            while length <= len(line) and fm.boundingRect(line[:length]).width() < 420:
                length += 1
            text.append(line[:length])
            width = max(width, fm.boundingRect(text[-1]).width())
            height += fm.boundingRect(text[-1]).height()
            height += 11
            lines[0] = line[length:]
            if len(lines[0]) == 0:
                lines = lines[1:]

        # print(text)

        width = fm.boundingRect(text[0]).width()

        bubble = QLabel()
        bubble.setFont(font)

        bubble.setText('\n'.join(text))
        bubble.adjustSize()
        bubble.setWordWrap(True)
        bubble.setScaledContents(True)

        bubble.setFixedHeight(height+30)
        bubble.setFixedWidth(width+30)

        layout = QHBoxLayout()
        layout.addWidget(bubble)

        if source == 1:
            bubble.setContentsMargins(10, 10, 10, 10)
            layout.setAlignment(Qt.AlignRight)
            bubble.setStyleSheet('''
                background-color:rgb(149,236,105);
                 border:0px;
                border-radius:10px;
                color:white;
            ''')
        else:
            bubble.setContentsMargins(10, 10, 10, 10)
            layout.setAlignment(Qt.AlignLeft)
            bubble.setStyleSheet('''
                background-color:rgba(65,204,237);
                 border:0px;
                border-radius:10px;
                color:white;
            ''')
        w = QWidget()
        w.setFixedSize(500, bubble.height()+10)
        w.setLayout(layout)

        return w

    # def test(self, msg: str, source: int):
    #     height = 0
    #     width = 0
    #     height = 56
    #     checkLengthOver = 0
    #     chineseExistFlag = 0
    #     textSlice = msg.split("\n")
    #     sendTextList = list()

    #     for s in textSlice:
    #         tmpText = ""
    #         tmpNum = 0
    #         tmpWidth = 0
    #         tmpNumList = list()
    #         tmpNumList.append(0)
    #         status = 0
    #         if not s:
    #             height += 16
    #         for i in s:
    #             if ord(i) in range(257):
    #                 tmpWidth += 600 / 73
    #                 tmpNum += 1
    #                 if not status:
    #                     status = 1
    #                     height += 16
    #             else:
    #                 tmpWidth += 600 / 44
    #                 tmpNum += 1
    #                 if not status:
    #                     status = 1
    #                     height += 16.3
    #                 chineseExistFlag = 1

    #             if tmpWidth > 600 - 600 / 44:
    #                 tmpNumList.append(tmpNum)
    #                 checkLengthOver = 1
    #                 tmpWidth = 0
    #                 if chineseExistFlag:
    #                     chineseExistFlag = 0
    #                     height += 16.3
    #                 else:
    #                     height += 16

    #             if tmpWidth > width:
    #                 width = tmpWidth
    #             if checkLengthOver == 1:
    #                 width = 600

    #         for j in range(len(tmpNumList)-1):
    #             tmpText = tmpText + s[tmpNumList[j]:tmpNumList[j+1]] + "\n"
    #             tmpText = tmpText + s[tmpNumList[-1]:]
    #             sendTextList.append(tmpText)
    #             sendText = "\n".join(sendTextList)

    #             if width == 0:
    #                 width = 70
    #             else:
    #                 width += 80

    #             itemHeight = height + 100

    #             bubble.setMinimumSize(QtCore.QSize(width, height))
    #             bubble.setMaximumSize(QtCore.QSize(width, height))
    #             bubble.setWordWrap(True)
    #             bubble.setText(sendText)
    #             bubble.adjustSize()
    #             bubble.setScaledContents(True)

    def setMyStyle(self):
        self.setStyleSheet('''
            QLabel:{
                border:0px;
                border-radius:10px;
                color:white;
                font-family: 微软雅黑;
                font-size: 20px;
            }
        ''')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MessageBox()
    ex.show()
    sys.exit(app.exec_())
