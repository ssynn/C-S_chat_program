import sys
import src.main_widget as mw
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = mw.MainWindow()
    ex.show()
    sys.exit(app.exec_())