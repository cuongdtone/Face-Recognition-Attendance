import sys
import PyQt5
import cv2
import time
import os
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, \
    QWidget, QAction, QTabWidget, QVBoxLayout, QLabel, QStackedLayout, QLineEdit
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
from face_threading import face_thread
from utils import play_sound

width = 1280
height = 720

def set_color_for_object(obj, color=(0,0,0)):
    color = PyQt5.QtGui.QColor(color[0], color[1], color[2])
    alpha = 140
    values = "{r}, {g}, {b}, {a}".format(r=color.red(),
                                         g=color.green(),
                                         b=color.blue(),
                                         a=alpha
                                         )
    obj.setStyleSheet("QLabel { background-color: rgba(" + values + "); }")
def norm_size(w=0, h=0):
    return int(w*width), int(h*height)



class DetectThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self, id):
        super().__init__()
        self._run_flag = True
        self.id = id
    def run(self):
        # capture from web cam
        self.cap = cv2.VideoCapture(0)
        self.face_threading = face_thread(self.cap)
        final_frame_queue = self.face_threading.run()
        while self._run_flag:
            cv_img = final_frame_queue.get()
            self.change_pixmap_signal.emit(cv_img)
        self.cap.release()
        # shut down capture system
    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.cap.release()
        self.wait()

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Cuong Tran'
        self.left = 0
        self.top = 0
        self.width = width
        self.height = height
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tabs.resize(300, 200)

        self.tab1 = Camera()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        # Add tabs
        self.tabs.addTab(self.tab1, "Camera")
        self.tabs.addTab(self.tab2, "Them nhan vien")
        self.tabs.addTab(self.tab3, "Quan ly")

        # Create first tab


        #############################################
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def button_test(self):
        print('a')
    def button2_test(self):
        print('b')

        # Add tabs to widget


    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
class Camera(QWidget):
    def __init__(self):
        super(Camera, self).__init__()

        #Screen
        self.screen = QLabel(self)
        self.screen.setText("Screen")
        self.screen.setAlignment(Qt.AlignCenter)
        self.screen_width = 720
        self.screen_height = 480
        self.screen.setGeometry(100, 100, self.screen_width, self.screen_height)
        set_color_for_object(self.screen, (100, 100, 100))

        #Run Button
        self.run_button = QPushButton(self)
        self.run_button.setText("Run")
        self.run_button.move(430, 600)
        self.run_button.clicked.connect(self.run)

        #Stop Button
        self.stop_button = QPushButton(self)
        self.stop_button.setText("Stop")
        self.stop_button.move(530, 600)
        self.stop_button.clicked.connect(self.stop)

        self.show()
    def run(self):
        play_sound(8)
        self.thread = DetectThread(0)
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()
        self.run_button.setEnabled(False)
    def stop(self):
        self.thread.stop()
        self.run_button.setEnabled(True)

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.screen.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        #rgb_image = cv2.flip(rgb_image, flipCode=1)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.screen_width, self.screen_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
