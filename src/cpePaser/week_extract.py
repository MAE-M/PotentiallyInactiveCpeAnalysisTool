#  Copyright (c) 2020 Huawei Technologies Co., Ltd.
#  foss@huawei.com
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.


from src.compress import compress
import os
from src.timeOperator import timeOpt
import pandas as pd
from src.setting import setting
from src.cpePaser import day_extract
import time
import multiprocessing
import numpy as np
from src.potThread import potThread

from src.logger_setting.my_logger import get_logger

logger = get_logger()


def get_min_month():
    all_day = day_extract.get_all_day()
    month_list = []
    for day in all_day:
        month_list.append(day[:6])
    month_list = list(set(month_list))
    month_list.sort()
    return str(month_list[0]) + "01"


def get_date_map():
    all_day_files = compress.get_all_day_csv(os.path.join(setting.data_path, 'day'))
    min_date = get_min_month()
    all_day_files.sort()
    date_file_map = {}
    date = min_date
    for i in range(len(all_day_files)):
        if i == 0:
            date_file_map[date] = all_day_files[i]
        else:
            date = timeOpt.add_days(date, 1)
            date_file_map[date] = all_day_files[i]
    return date_file_map


def get_file_by_range(first_day, last_day):
    date_file_map = get_date_map()
    files = []
    for k, v in date_file_map.items():
        if timeOpt.is_in_time(k, first_day, last_day):
            files.append(v)
    return files


def calc_week_data(df):
    esn = df['esn'].values
    total_connect_time = np.sum(df['TotalConnectTime'].values)
    total_upload = np.sum(df['TotalUpload'].values) / setting.gb
    total_download = np.sum(df['TotalDownload'].values) / setting.gb
    data = {'esn': esn[0],
            'TotalDownload': [total_download],
            'TotalUpload': [total_upload],
            'TotalConnectTime': [total_connect_time]}

    result = pd.DataFrame(data)
    return result


def merge_week_data(week_files):
    df = pd.DataFrame(columns=setting.column_name)
    for file in week_files:
        file_df = pd.read_csv(file, error_bad_lines=False, index_col=False)
        df = df.append(file_df)
    grouped = day_extract.groupby_calc(df).apply(calc_week_data)
    df = pd.DataFrame(grouped)
    return df


def merge_train_week(week):
    week_files = get_file_by_range(week[1], week[2])
    df = merge_week_data(week_files)
    df.to_csv(os.path.join(setting.data_path, 'trainWeek', "week" + str(week[0]) + r".csv"), index=False)


def merge_pre_week(week):
    week_files = get_file_by_range(week[1], week[2])
    df = merge_week_data(week_files)
    df.to_csv(os.path.join(setting.data_path, 'predictWeek', "week" + str(week[0]) + r".csv"), index=False)


def get_train_week():
    timeOpt.weekSet = []
    min_month = get_min_month()
    week_set = timeOpt.get_week_set(min_month, timeOpt.add_months(min_month, 2))
    week_set = timeOpt.change_week_set(week_set)
    week_list = []
    for i in range(len(week_set)):
        if i < len(week_set) - 1:
            week_list.append((i + 1, week_set[i], week_set[i + 1]))
    return week_list


def get_pre_week():
    timeOpt.weekSet = []
    min_month = get_min_month()
    week_set = timeOpt.get_week_set(timeOpt.add_months(min_month, 1), timeOpt.add_months(min_month, 3))
    week_set = timeOpt.change_week_set(week_set)
    week_list = []
    for i in range(len(week_set)):
        if i < len(week_set) - 1:
            week_list.append((i + 1, week_set[i], week_set[i + 1]))
    return week_list


def my_test():
    compress.empty_folder(os.path.join(setting.data_path, 'trainWeek'))
    compress.empty_folder(os.path.join(setting.data_path, 'predictWeek'))
    train_week = get_train_week()
    pre_week = get_pre_week()
    train_pool = potThread.PotThread(2)
    train_pool.run_pot_threads(merge_train_week, train_week)
    pre_pool = potThread.PotThread(2)
    pre_pool.run_pot_threads(merge_pre_week, pre_week)


if __name__ == "__main__":
    # get_min_month()
    # print get_min_month()
    # print compress.get_all_day_csv(os.path.join(compress.cpe_unzip_path, 'day'))
    # print get_week_file("20200201", "20200205")
    # print get_pre_week()
    # print(get_date_map())
    # print len(get_train_week())
    # print time.localtime(time.time())
    multiprocessing.freeze_support()
    my_test()
    print(time.localtime(time.time()))
