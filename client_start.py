import sys
from PyQt5.QtWidgets import QApplication
from src import main_widget as mw

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = mw.MainWindow()
    ex.show()
    sys.exit(app.exec_())
