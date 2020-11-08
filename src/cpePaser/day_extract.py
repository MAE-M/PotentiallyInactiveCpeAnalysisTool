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

import os
import time
from typing import Dict, List

import numpy as np
import pandas as pd
from collections import Counter

from src.compress import compress
# 日志器
from src.logger_setting.my_logger import get_logger
from src.setting import setting

LOGGER = get_logger()


def groupby_calc(df):
    df['esn'] = df['esn'].astype('str')
    df = df.groupby(['esn'])
    return df


def calc_total(series):
    series = series.values
    count = 0
    for d in range(len(series)):
        if d < len(series) - 1:
            if pd.isna(series[d]) or pd.isna(series[d + 1]):
                continue
            if float(series[d]) <= float(series[d + 1]):
                count += float(series[d + 1]) - float(series[d])
            else:
                count += float(series[d + 1])
    return count


def is_active(series):
    series = calc_total(series)
    if float(series) / setting.mb > 10:
        return 1
    else:
        return 0


def get_max(series):
    if series:
        return np.max(series)
    else:
        return setting.INVALID_VALUE


def get_min(series):
    if series:
        return np.min(series)
    else:
        return setting.INVALID_VALUE


def get_avg(values, counts):
    count = sum(counts) if type(counts) == list else counts
    if count == 0:
        return setting.INVALID_VALUE
    else:
        return sum(values) / count if type(values) == list else values / count


def get_avg_max_min(df, avg_name, max_name, min_name, counts):
    avg_list = list(filter(lambda x: int(x) != setting.INVALID_VALUE, df[avg_name].values))
    sum_value = get_sum(avg_list)
    cnt = get_sum(list(df[counts].values))
    avg = sum_value / cnt if cnt != 0 else setting.INVALID_VALUE
    max_list = list(filter(lambda x: int(x) != setting.INVALID_VALUE, df[max_name].values))
    max_value = get_max(max_list)
    min_list = list(filter(lambda x: int(x) != setting.INVALID_VALUE, df[min_name].values))
    min_value = get_min(min_list)
    return {avg_name: avg,
            max_name: max_value,
            min_name: min_value}


def get_sum(series):
    if series:
        return np.sum(series)
    else:
        return setting.INVALID_VALUE


def get_std(series):
    if series:
        return np.std(series)
    else:
        return setting.INVALID_VALUE


def get_all_day():
    all_day_file = compress.get_all_csv_file(os.path.join(setting.data_path, 'extractData'))
    day_list = []
    for file in all_day_file:
        day_list.append(os.path.split(file)[1].split("\\")[-1].split('_')[0])
    return list(set(day_list))


def merge_day_data(day_dict: Dict[str, List[str]]):
    for day in day_dict.keys():
        file_list: List[str] = day_dict.get(day)
        df = pd.concat(pd.read_csv(file, error_bad_lines=False, index_col=False) for file in file_list)
        df.columns = setting.parameter_json["extract_data_columns"]
        df = df.sort_values('collectTime', ascending=True)
        # 把-9999变成了NaN,但是原来是空的值，在读进来的时候已经变成NaN了，所有空值和-9999都变成了NaN
        df = df.replace(setting.INVALID_VALUE, np.nan)
        grouped = groupby_calc(df).agg(
            MaxRSRP=pd.NamedAgg(column='RSRP', aggfunc=max),
            MinRSRP=pd.NamedAgg(column='RSRP', aggfunc=min),
            AvgRSRP=pd.NamedAgg(column='RSRP', aggfunc=sum),
            CntRSRP=pd.NamedAgg(column='RSRP', aggfunc="count"),
            MaxCQI=pd.NamedAgg(column='CQI', aggfunc=max),
            MinCQI=pd.NamedAgg(column='CQI', aggfunc=min),
            AvgCQI=pd.NamedAgg(column='CQI', aggfunc=sum),
            CntCQI=pd.NamedAgg(column='CQI', aggfunc="count"),
            MaxRSRQ=pd.NamedAgg(column='RSRQ', aggfunc=max),
            MinRSRQ=pd.NamedAgg(column='RSRQ', aggfunc=min),
            AvgRSRQ=pd.NamedAgg(column='RSRQ', aggfunc=sum),
            CntRSRQ=pd.NamedAgg(column='RSRQ', aggfunc="count"),
            MaxRSSI=pd.NamedAgg(column='RSSI', aggfunc=max),
            MinRSSI=pd.NamedAgg(column='RSSI', aggfunc=min),
            AvgRSSI=pd.NamedAgg(column='RSSI', aggfunc=sum),
            CntRSSI=pd.NamedAgg(column='RSSI', aggfunc="count"),
            MaxSINR=pd.NamedAgg(column='SINR', aggfunc=max),
            MinSINR=pd.NamedAgg(column='SINR', aggfunc=min),
            AvgSINR=pd.NamedAgg(column='SINR', aggfunc=sum),
            CntSINR=pd.NamedAgg(column='SINR', aggfunc="count"),
            TotalDownload=pd.NamedAgg(column='TotalDownload', aggfunc=calc_total),
            TotalUpload=pd.NamedAgg(column='TotalUpload', aggfunc=calc_total),
            TotalConnectTime=pd.NamedAgg(column='TotalConnectTime', aggfunc=calc_total),
            ModelName=pd.NamedAgg(column='ModelName', aggfunc=lambda x: x.iloc[-1]),
            IMSI=pd.NamedAgg(column='IMSI', aggfunc=lambda x: x.iloc[-1]),
            IMEI=pd.NamedAgg(column='IMEI', aggfunc=lambda x: x.iloc[-1]),
            MSISDN=pd.NamedAgg(column='MSISDN', aggfunc=lambda x: x.iloc[-1]),
            isActive=pd.NamedAgg(column='TotalDownload', aggfunc=is_active),
            AvgDlThroughput=pd.NamedAgg(column='MaxDLThroughput', aggfunc=sum),
            CntDlThroughput=pd.NamedAgg(column='MaxDLThroughput', aggfunc="count"),
            AvgUlThroughput=pd.NamedAgg(column='MaxULThroughput', aggfunc=sum),
            CntUlThroughput=pd.NamedAgg(column='MaxULThroughput', aggfunc="count"),
            WiFiUserQty=pd.NamedAgg(column='WiFiUserQty', aggfunc=sum),
            CntWiFiUserQty=pd.NamedAgg(column='WiFiUserQty', aggfunc="count"),
            HostNumberOfEntries=pd.NamedAgg(column='HostNumberOfEntries', aggfunc=sum),
            CntHostNumberOfEntries=pd.NamedAgg(column='HostNumberOfEntries', aggfunc="count"),
            ECGI=pd.NamedAgg(column='ECGI', aggfunc=get_main_cell),)

        grouped[['TotalDownload', 'TotalUpload', 'TotalConnectTime', 'ModelName', 'IMSI',
                 'IMEI', 'MSISDN']] = grouped.sort_values('esn')[
            ['TotalDownload', 'TotalUpload', 'TotalConnectTime', 'ModelName', 'IMSI',
             'IMEI', 'MSISDN']].fillna(0)

        grouped = grouped.reset_index()
        grouped['date'] = day
        # 除了 'TotalDownload', 'TotalUpload', 'TotalConnectTime', 'ModelName', 'IMSI', 'IMEI', 'MSISDN' 这几列
        # 其他列的nan将转换还原为setting.INVALID_VALUE, 也就是-9999
        grouped = grouped.replace(np.nan, setting.INVALID_VALUE)
        grouped.to_csv(os.path.join(setting.data_path, 'day', day + r".csv"), index=False)


# return a dictionary with:
# key: date
# value: list of filenames of this date
def get_day_df_dict() -> Dict[str, List[str]]:
    all_day_file = compress.get_all_csv_file(os.path.join(setting.data_path, 'extractData'))
    day_dict = dict()
    for file in all_day_file:
        date = os.path.split(file)[1].split("\\")[-1].split('_')[0]
        if date not in day_dict:
            day_dict[date] = list()
        day_dict[date].append(file)
    return day_dict


def get_main_cell(series):
    count_map = Counter(list(filter(lambda x: x != setting.INVALID_STRING, series)))
    count = 0
    main_cell = "-"
    for cell, nums in count_map.items():
        if nums > count:
            count = nums
            main_cell = cell
    return main_cell


def day_extract():
    compress.empty_folder(os.path.join(setting.data_path, 'day'))
    day_dict = get_day_df_dict()
    merge_day_data(day_dict)


if __name__ == '__main__':
    print(time.localtime(time.time()))
    day_extract()
    print(time.localtime(time.time()))
