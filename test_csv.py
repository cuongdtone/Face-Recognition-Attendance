from datetime import datetime, timedelta

# now = datetime.now()
# today = now.strftime('%Y-%m-%d')
# date_obj = datetime.strptime(today, '%Y-%m-%d')
# monday = (date_obj - timedelta(days=date_obj.weekday()))  # Monday
# log_2_week_ago = monday - timedelta(days=14)
# print(monday)
# print(log_2_week_ago)
#
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
#
# gauth = GoogleAuth()
# drive = GoogleDrive(gauth)
# gfile = drive.CreateFile({'parents': [{'id': '1aMVU05zx1h-3MD1YCA2omjPlwzpuewb-'}]})
#
# gfile.SetContentFile('week_log/2022-03-28/2022-04-03.csv')
# gfile.Upload()

import pandas as pd
from glob import glob

path_of_week = 'week_log/2022-04-04/'
day_log_list = glob(path_of_week + '/*.csv')
week_log_df = pd.read_csv(day_log_list[0])
for i in range(1, len(day_log_list)):
    try:
        df = pd.read_csv(day_log_list[i])
        week_log_df = week_log_df.append(df)
    except:
        continue
week_log_df = week_log_df.sort_values(by=['Name'])

print(week_log_df)


