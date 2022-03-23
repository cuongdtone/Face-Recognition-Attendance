# importing the required libraries
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # set the title
        self.setWindowTitle("Geometry")

        # setting  the geometry of window
        # setGeometry(left, top, width, height)
        self.setGeometry(100, 60, 1000, 800)

        # creating a label widget
        self.widget = QLabel('Hello', self)
        self.widget.setGeometry(100,100,100,100)

        # show all the widgets
        self.show()


# create pyqt5 app
App = QApplication(sys.argv)

# create the instance of our Window
window = Window()
# start the app
sys.exit(App.exec())