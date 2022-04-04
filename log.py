import datetime
import csv
import os.path
import os
from glob import glob

from utils import play_sound
import cv2
import pandas as pd
from datetime import datetime, timedelta
import shutil
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from threading import Thread
import time

gauth = GoogleAuth()
drive = GoogleDrive(gauth)
gfile = drive.CreateFile({'parents': [{'id': '1aMVU05zx1h-3MD1YCA2omjPlwzpuewb-'}]})

class Log():
    def __init__(self, root_path='week_log'):
        self.root_path = root_path
        self.log = pd.DataFrame({'Name': [], 'Position': [], 'Office': [], 'Time':[]})
        self.period_log = '' #time reset log
        self.thread = Thread(target=self.flow_thread)
        self.flag = True
        self.thread.start()

    def timekeep(self, data):
        # data is dict: {'frame':frame, 'people': people}
        # people is dict: [[Name, Sim (percent recognition), Position, Office, path, box]] (path to image in database

        # we need csv log file include: Name, Position, Office, Login Time, Late (true of false),
        # self.period_log is [{Name, Position, Office, Login Time, Late}, ...]
        now = datetime.now()
        today = now.strftime('%Y-%m-%d')
        date_obj = datetime.strptime(today, '%Y-%m-%d')
        monday = (date_obj - timedelta(days=date_obj.weekday())).strftime('%Y-%m-%d') # Monday
        if not os.path.exists(self.root_path + '/' + monday):
            os.mkdir(self.root_path + '/' + monday)
        path_csv_today = self.root_path + '/' + monday + '/' + today + '.csv'
        if not os.path.exists(path_csv_today):
            self.log = pd.DataFrame({'Name': [], 'Position': [], 'Office': [], 'Time':[]})
            self.log.to_csv(path_csv_today, index=False)
        self.log = pd.read_csv(path_csv_today)
        people = data['people']
        frame = data['frame']
        for idx, person in enumerate(people):
            name = person['Name']
            if name == 'uknown':
                face = cv2.imread('icon/unknown_person.jpg')
                #play_sound(1)
                #print()
            else:
                check_name_list = name in self.log.iloc[:, 0].tolist() # only one timekeep per one period
                if not check_name_list:
                    attendance_info = pd.DataFrame({"Name": [name],
                                                    "Position": [person['Position']],
                                                    'Office': [person['Office']],
                                                    'Time': now.strftime('%a %H:%M:%S')
                                                    })
                    self.log = self.log.append(attendance_info) # sucess
                    face_box = [int(i) for i in person['box']]
                    face = frame[face_box[1]:face_box[3], face_box[0]:face_box[2], :]
                    play_sound(6)
                    self.log.to_csv(path_csv_today, index=False)
                    break
        #info = {'face':face, 'Name': name, 'Position':person['Position'], 'Office': person['Office']}
        try:
            return {'face':face,
                    'Name': name,
                    'Position':person['Position'],
                    'Office': person['Office'],
                    'Time': now.strftime('%a %H:%M:%S')
                    }
        except:
            return None
    def flow_thread(self):
        while self.flag:
            #print('[INFO] Hiden Task for upload is running !')
            now = datetime.now()
            today = now.strftime('%Y-%m-%d')
            date_obj = datetime.strptime(today, '%Y-%m-%d')
            monday_obj = (date_obj - timedelta(days=date_obj.weekday()))
            monday = monday_obj.strftime('%Y-%m-%d')  # Monday
            if today == monday:
                # delete old log file to release memory
                try:
                    monday_of_2_week_ago = (monday_obj - timedelta(days=14)).strftime('%Y-%m-%d')
                    shutil.rmtree(self.root_path + '/' + monday_of_2_week_ago)
                except:
                    pass
                # upload log file of last week
                path_last_week_file = self.root_path + '/' + monday + '.csv'
                if not os.path.exists(path_last_week_file):
                    monday_of_last_week = (monday_obj - timedelta(days=7)).strftime('%Y-%m-%d')
                    path_of_week = self.root_path + '/' + monday_of_last_week
                    day_log_list = glob(path_of_week + '/*.csv')
                    week_log_df = pd.read_csv(day_log_list[0])
                    for i in range(1, len(day_log_list)):
                        try:
                            df = pd.read_csv(day_log_list[i])
                            week_log_df = week_log_df.append(df)
                        except:
                            continue
                    week_log_df = week_log_df.sort_values(by=['Name'])
                    week_log_df.to_csv(path_last_week_file, index=False)
                    gfile.SetContentFile(path_last_week_file)
                    gfile.Upload()
















