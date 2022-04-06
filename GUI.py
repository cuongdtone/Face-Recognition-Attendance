import sys
import traceback

import PyQt5
import cv2
import time
import os
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt, QThread
import numpy as np
from Face_Recognition.face_threading import face_thread
from Face_Recognition.face import Face_Model
from utils import play_sound, save_new_image
from log import Log
import yaml
from glob import glob
from ui_tab_1 import Tab_1
from ui_tab_2 import Tab_2

with open('config.yaml', 'r') as f:
    param = yaml.load(f, yaml.FullLoader)

camera_id = param['camera']

width = param['width']
height = param['height']

use_camera = 1 #tab 1 is allow using camera
thread_1_running = False

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

    def __init__(self, log):
        super().__init__()
        self._run_flag = True
        self.log = log
    def run(self):
        # capture from web cam
        global use_camera
        self.cap = cv2.VideoCapture(camera_id)
        self.face_threading = face_thread(self.cap)
        final_frame_queue, frame_ori_queue = self.face_threading.run()
        #print(final_data_queue)
        while self._run_flag and use_camera == 1:
            #print('task 1')
            data = final_frame_queue.get()
            frame_ori = frame_ori_queue.get()

            cv_img = data['frame'] # drawed frame
            self.change_pixmap_signal.emit(cv_img)

            data['frame'] = frame_ori
            info = self.log.timekeep(data)
            if info is not None:
                self.change_infor_signal.emit(info)
        print('end task 1')
        self.cap.release()
        self.stop()
        # shut down capture system
    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.cap.release()
        self.wait()

class CapThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def run(self):
        # capture from web cam
        print('Cap runing')
        global use_camera
        cap = cv2.VideoCapture(camera_id)
        while use_camera == 2:
            #print('Task 2')
            ret, cv_img = cap.read()
            if ret:
                self.change_pixmap_signal.emit(cv_img)
        cap.release()

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
        self.tab2 = AddEmployee()
        self.tab3 = QWidget()
        # Add tabs
        self.tabs.addTab(self.tab1, "Camera")
        self.tabs.addTab(self.tab2, "Them nhan vien")

        #############################################
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    @pyqtSlot()
    def on_click(self):
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
class Camera(QWidget, Tab_1):
    def __init__(self, parent=None):
        super(Camera, self).__init__(parent)
        self.setupUi(self)
        self.screen_width, self.screen_height = 720, 520
        self.screen.resize(self.screen_width, self.screen_height)
        self.width_sub_screen, self.height_sub_sceen = 200, 200

        self.run_button.clicked.connect(self.run)
        self.stop_button.clicked.connect(self.stop)

        self.log = Log()
        self.log.flag = False
        self.show()

    def run(self):
        global use_camera, thread_1_running
        if use_camera != 1:
            use_camera = 1
            thread_1_running = False
        if not thread_1_running:
            play_sound(8)
            time.sleep(0.5)

            self.log.flag = True

            self.thread = DetectThread(self.log)
            self.thread.change_pixmap_signal.connect(self.update_image_main_screen)
            self.thread.change_infor_signal.connect(self.update_timekeep)
            self.thread.start()
            thread_1_running = True

    def stop(self):
        global thread_1_running
        try:
            self.thread.stop()
            thread_1_running = False
            self.log.flag = False
        except:
            pass

    @pyqtSlot(np.ndarray)
    def update_timekeep(self, data):
        try:
            face = data['face']
            qt_img = self.convert_cv_qt(face, self.width_sub_screen, self.height_sub_sceen)
            self.sub_screen.setPixmap(qt_img)
            self.name_screen.setText(data['Name'])
            self.position_screen.setText(data['Position'])
            self.office_screen.setText(data['Office'])
            self.time_screen.setText(data['Time'])
        except Exception:
            print(traceback.format_exc())
            print(sys.exc_info()[2])

    def update_image_main_screen(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img, self.screen_width, self.screen_height)
        self.screen.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img, w_screen, h_screen):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        rgb_image = cv2.resize(rgb_image, (w_screen, h_screen))
        #rgb_image = cv2.flip(rgb_image, flipCode=1)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(w_screen, h_screen, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

class AddEmployee(QWidget, Tab_2):
    def __init__(self, root_path='Employee_Infomation'):
        super(AddEmployee, self).__init__()
        self.setupUi(self)

        self.root_path = root_path

        self.cap_button.clicked.connect(self.shot)
        self.create_person.clicked.connect(self.create_data)

        self.face_model = Face_Model()
        self.shot_flag = False

        self.thread = CapThread()
        self.thread.change_pixmap_signal.connect(self.update_image_main_screen)
        self.thread_cap_run = False
        self.show()
    def shot(self):
        try:
            if self.name.text().strip() != '':
                list_name = glob(self.root_path + '/*')
                list_name = [i.split('/')[1] for i in list_name]
                if self.name.text() in list_name and self.shot_flag is False:
                    ret = QMessageBox.question(self, 'Warning', "This name is avaiable in database \n Create new name (Yes) or update (No)", QMessageBox.No|QMessageBox.Yes )
                    if (ret == QMessageBox.Yes):
                        first_chr = 97
                        now_name = self.name.text()
                        while self.name.text() in list_name:
                            self.name.setText(now_name + '_' + chr(first_chr))
                            first_chr += 1
                    self.shot_flag = True
                global use_camera
                if use_camera != 2:
                    self.thread_cap_run = False
                    use_camera = 2
                time.sleep(0.5)
                if self.thread_cap_run is False:
                    self.thread.start()
                    self.thread_cap_run = True
                    self.shot_flag = True
                else:
                    # shot image task
                    self.shot_flag = True
                    name = self.name.text()
                    if not os.path.exists(os.path.join(self.root_path, name)):
                        os.mkdir(os.path.join(self.root_path, name))
                    save_new_image(os.path.join(self.root_path, name), self.image)
            else:
                QMessageBox.warning(self, 'Warning!', 'Fill name first')
        except Exception:
            print(traceback.format_exc())
            print(sys.exc_info()[2])
            QMessageBox.warning(self, 'Warning!', 'Fill name first')
    def create_data(self):
        try:
            self.shot_flag = False
            name = self.name.text()
            postion = self.position.text()
            office = self.office.text()

            self.face_model.create_data_file(name, postion, office)

            self.name.setText('')
            self.position.setText('')
            self.office.setText('')

            QMessageBox.warning(self, 'Completed!', '')
        except:
            QMessageBox.warning(self, 'Warning!', "Can't create data")

    @pyqtSlot(np.ndarray)
    def update_image_main_screen(self, cv_img):
        """Updates the image_label with a new opencv image"""
        self.image = cv_img
        qt_img = self.convert_cv_qt(cv_img, 720, 480)
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
