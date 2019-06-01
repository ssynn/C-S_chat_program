import sys
from PyQt5.QtWidgets import QApplication
from src import main_widget as mw
from src import client_page as cp


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = cp.ClientPage({'ID':'1','PASSWORD':'1'},None, '127.0.0.1:9999')
    ex.show()
    sys.exit(app.exec_())
