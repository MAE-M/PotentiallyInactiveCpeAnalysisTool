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

from src.cpePaser import week_extract
import pandas as pd
from src.setting import setting
from src.cpePaser import day_extract
import numpy as np
from src.timeOperator import timeOpt
import os
from src.compress import compress
from src.potThread import potThread
import time
import multiprocessing

from src.logger_setting.my_logger import get_logger

logger = get_logger()


def get_month_data(first_day, last_day, columns=setting.month_column_name):
    all_file = week_extract.get_file_by_range(first_day, last_day)
    df = merge_month_data(all_file, columns=columns)
    return df


def merge_month_data(month_files, columns):
    df = pd.DataFrame(columns=columns)
    for file in month_files:
        file_df = pd.read_csv(file, error_bad_lines=False, index_col=False)[setting.month_column_name]
        df = df.append(file_df)
    grouped = day_extract.groupby_calc(df).apply(calc_month_data)
    df = pd.DataFrame(grouped)
    return df


def calc_month_data(df):
    esn = df['esn'].values
    active_day = np.sum(df['isActive'])
    total_connect_time = np.sum(df['TotalConnectTime'].values)
    total_download = np.sum(df['TotalDownload'].values) / setting.gb
    total_upload = np.sum(df['TotalUpload'].values) / setting.gb
    total_traffic = total_download + total_upload
    dl_traffic_ratio = divide(total_download, total_traffic)
    total_traffic_per_day = divide(total_traffic, active_day)
    dl_traffic_per_day = divide(total_download, active_day)
    ul_traffic_per_day = divide(total_upload, active_day)
    connect_time_per_day = divide(total_connect_time, active_day)

    rsrp_sinr = calc_rsrp_sinr(df)

    data = {'esn': esn[0],
            'activeDay': [active_day],
            'totalConnectTime': [total_connect_time],
            'dlTraffic': [total_download],
            'ulTraffic': [total_upload],
            'totalDlUlTrafficMonthly': [total_traffic],
            'dlTrafficRatioMonthly': [dl_traffic_ratio],
            'totalDlUlTrafficPerday': [total_traffic_per_day],
            'dlTrafficPerday': [dl_traffic_per_day],
            'ulTrafficPerday': [ul_traffic_per_day],
            'totalConnectTimePerday': [connect_time_per_day],
            'MinRSRP': rsrp_sinr['MinRSRP'],
            'MaxRSRP': rsrp_sinr['MaxRSRP'],
            'AvgRSRP': rsrp_sinr['AvgRSRP'],
            'StdRSRP': rsrp_sinr['StdRSRP'],
            'MinSINR': rsrp_sinr['MinSINR'],
            'MaxSINR': rsrp_sinr['MaxSINR'],
            'AvgSINR': rsrp_sinr['AvgSINR'],
            'StdSINR': rsrp_sinr['StdSINR']}

    result = pd.DataFrame(data)
    return result


def calc_rsrp_sinr(df):
    rsrp = day_extract.get_avg_max_min(df, 'AvgRSRP', 'MaxRSRP', 'MinRSRP', 'CntRSRP')
    df['DayAvgRSRP'] = df.apply(lambda x: day_extract.get_avg(x['AvgRSRP'], x['CntRSRP']), axis=1)
    day_avg_rsrp = list(filter(lambda x: int(x) != setting.INVALID_VALUE, df['DayAvgRSRP'].values))
    std_rsrp = day_extract.get_std(day_avg_rsrp)

    sinr = day_extract.get_avg_max_min(df, 'AvgSINR', 'MaxSINR', 'MinSINR', 'CntSINR')
    df['DayAvgSINR'] = df.apply(lambda x: day_extract.get_avg(x['AvgSINR'], x['CntSINR']), axis=1)
    day_avg_sinr = list(filter(lambda x: int(x) != setting.INVALID_VALUE, df['DayAvgSINR'].values))
    std_sinr = day_extract.get_std(day_avg_sinr)
    return {'MinRSRP': rsrp['MinRSRP'],
            'MaxRSRP': rsrp['MaxRSRP'],
            'AvgRSRP': rsrp['AvgRSRP'],
            'StdRSRP': [std_rsrp],
            'MaxSINR': sinr['MaxSINR'],
            'MinSINR': sinr['MinSINR'],
            'AvgSINR': sinr['AvgSINR'],
            'StdSINR': [std_sinr]
            }


def divide(numerator, denominator, default_value=0):
    if denominator == 0:
        return default_value
    else:
        return numerator / denominator


def get_train_month():
    min_month = week_extract.get_min_month()
    month_list = [(1, min_month, timeOpt.add_months(min_month, 1)),
                  (2, timeOpt.add_months(min_month, 1), timeOpt.add_months(min_month, 2))]
    return month_list


def get_pre_month():
    min_month = week_extract.get_min_month()
    month_list = [(1, timeOpt.add_months(min_month, 1), timeOpt.add_months(min_month, 2)),
                  (2, timeOpt.add_months(min_month, 2), timeOpt.add_months(min_month, 3))]
    return month_list


def merge_train_month(month):
    df = get_month_data(month[1], month[2])
    df.to_csv(os.path.join(setting.data_path, 'trainMonth', "month" + str(month[0]) + r".csv"), index=False)


def merge_pre_month(month):
    df = get_month_data(month[1], month[2])
    df.to_csv(os.path.join(setting.data_path, 'predictMonth', "month" + str(month[0]) + r".csv"), index=False)


def test():
    compress.empty_folder(os.path.join(setting.data_path, 'trainMonth'))
    compress.empty_folder(os.path.join(setting.data_path, 'predictMonth'))
    train_month = get_train_month()
    print(train_month)
    pre_month = get_pre_month()
    print(pre_month)
    train_pool = potThread.PotThread(2)
    train_pool.run_pot_threads(merge_train_month, train_month)
    pre_pool = potThread.PotThread(2)
    pre_pool.run_pot_threads(merge_pre_month, pre_month)


if __name__ == "__main__":
    print(time.localtime(time.time()))
    multiprocessing.freeze_support()
    test()
    print(time.localtime(time.time()))
