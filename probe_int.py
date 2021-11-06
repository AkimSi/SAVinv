from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
import sys


class Apl():
    def __init__(self):

        self.Form, self.Window = uic.loadUiType("inter.ui")
        self.app = QApplication([])
        self.window = self.Window()
        self.form = self.Form()
        self.form.setupUi(self.window)
        self.window.show()


        def click(self):
            print("TYPE!!!")

        self.form.pushButton.clicked.connect(click)

def main():
    go = Apl()
    sys.exit(go.app.exec())



if __name__ == '__main__':
    main()
