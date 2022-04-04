import sys
import PyQt5
import cv2
import time
import os
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, \
    QWidget, QAction, QTabWidget, QVBoxLayout, QLabel, QStackedLayout, QLineEdit
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
from face_threading import face_thread
from utils import play_sound
from log import Log
import yaml

with open('config.yaml', 'r') as f:
    param = yaml.load(f, yaml.FullLoader)

camera_id = param['camera']

width = param['width']
height = param['height']

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
    change_infor_signal = pyqtSignal(dict)

    def __init__(self, id, log):
        super().__init__()
        self._run_flag = True
        self.id = id
        self.log = log
    def run(self):
        # capture from web cam
        self.cap = cv2.VideoCapture(camera_id)
        self.face_threading = face_thread(self.cap)
        final_frame_queue, frame_ori_queue = self.face_threading.run()
        #print(final_data_queue)
        while self._run_flag:
            data = final_frame_queue.get()
            frame_ori = frame_ori_queue.get()

            cv_img = data['frame'] # drawed frame
            self.change_pixmap_signal.emit(cv_img)

            data['frame'] = frame_ori
            info = self.log.timekeep(data)
            if info is not None:
                self.change_infor_signal.emit(info)

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
        self.setWindowIcon(QIcon('icon/logo.png'))
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
        #self.tabs.resize(300, 200)

        self.tab1 = Camera()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        # Add tabs
        self.tabs.addTab(self.tab1, "Camera")
        self.tabs.addTab(self.tab2, "Them nhan vien")
        self.tabs.addTab(self.tab3, "Quan ly")

        #############################################
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    @pyqtSlot()
    def on_click(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
class Camera(QWidget):
    def __init__(self):
        super(Camera, self).__init__()
        uic.loadUi('gui.ui', self)

        #Screen
        self.screen = self.findChild(QLabel, 'screen')
        self.screen.setText("Screen")
        self.screen.setAlignment(Qt.AlignCenter)

        x_screen, y_screen = norm_size(0.1, 0.1)
        self.screen_width, self.screen_height = norm_size(0.5, 0.7)


        #Sub Screen
        self.sub_screen = QLabel(self)
        self.sub_screen.setText('Sub Screen')
        self.sub_screen.setAlignment(Qt.AlignCenter)

        x_sub_screen, y_sub_screen  = x_screen + self.screen_width + 150, y_screen
        self.width_sub_screen, self.height_sub_sceen = 200, 200
        self.sub_screen.setGeometry(x_sub_screen, y_sub_screen, self.width_sub_screen, self.height_sub_sceen)
        set_color_for_object(self.sub_screen, (100, 100, 100))

        # info
        self.name_screen = QLabel(self)
        self.name_screen.setText("Name: ")
        x_name, y_name = x_sub_screen, y_sub_screen + self.height_sub_sceen + 50
        self.name_screen.setGeometry(x_name, y_name, 300, 100)

        #Run Button
        self.run_button = QPushButton(self)
        self.run_button.setText("Run")
        x = int((x_screen + self.screen_width)/2.3)
        y = y_screen + self.screen_height + 30
        self.run_button.move(x, y)
        self.run_button.clicked.connect(self.run)

        #Stop Button
        self.stop_button = QPushButton(self)
        self.stop_button.setText("Stop")
        x = int((x_screen + self.screen_width)/1.6)
        y = y_screen + self.screen_height + 30
        self.stop_button.move(x, y)
        self.stop_button.clicked.connect(self.stop)

        self.show()
    def run(self):
        play_sound(8)
        self.log = Log()
        self.thread = DetectThread(0, self.log)
        self.thread.change_pixmap_signal.connect(self.update_image_main_screen)
        self.thread.change_infor_signal.connect(self.update_timekeep)
        self.thread.start()
        self.run_button.setEnabled(False)
    def stop(self):
        self.thread.stop()
        self.run_button.setEnabled(True)
        try:
            self.log.flag = False
        except:
            pass


    @pyqtSlot(np.ndarray)
    def update_timekeep(self, data):
        try:
            face = data['face']
            qt_img = self.convert_cv_qt(face, self.width_sub_screen, self.height_sub_sceen)
            self.sub_screen.setPixmap(qt_img)
            self.name_screen.setText('Name: ' + data['Name'] +
                                     '\nPosition: ' + data['Position'] +
                                     '\nOffice: ' + data['Office']  + '\nTime: ' + data['Time'])
        except:
            pass

    def update_image_main_screen(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img, self.screen_width, self.screen_height)
        self.screen.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img, w_screen, h_screen):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)

        #rgb_image = cv2.flip(rgb_image, flipCode=1)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(w_screen-10, h_screen-10, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

class AddEmployee(QWidget):
    def __init__(self):
        super(AddEmployee, self).__init__()
        # Load new info
        self.load_button

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
