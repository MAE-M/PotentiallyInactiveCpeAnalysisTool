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
import pandas as pd
from src.setting import setting
import numpy as np
import time
from src.compress import compress
from collections import Counter


def groupby_calc(df):
    df = df.groupby(['esn'])
    return df


def calc_total(total_value):
    count = 0
    for d in range(len(total_value)):
        if d < len(total_value) - 1:
            if total_value[d] == setting.INVALID_VALUE or total_value[d+1] == setting.INVALID_VALUE:
                continue
            if float(total_value[d]) <= float(total_value[d + 1]):
                count += float(total_value[d + 1]) - float(total_value[d])
            else:
                count += int(total_value[d + 1])
    return str(count)


def calc_sort_collect_time(df):
    df['collectTime'] = pd.to_datetime(df['collectTime'])
    df = df.sort_values('collectTime')[['esn', 'TotalDownload', 'TotalUpload', 'TotalConnectTime', 'ModelName', 'IMSI',
                                        'IMEI', 'MSISDN', 'collectTime']].fillna(0)
    newst_cpemodel = df['ModelName'].values[-1]
    newst_imsi = df['IMSI'].values[-1]
    newst_imei = df['IMEI'].values[-1]
    newst_msisdn = df['MSISDN'].values[-1]
    total_connect_time = calc_total(df['TotalConnectTime'].values)
    total_upload = calc_total(df['TotalUpload'].values)
    total_download = calc_total(df['TotalDownload'].values)

    return {'TotalDownload': [total_download],
            'TotalUpload': [total_upload],
            'TotalConnectTime': [total_connect_time],
            'ModelName': [newst_cpemodel],
            'IMSI': [newst_imsi],
            'IMEI': [newst_imei],
            'MSISDN': [newst_msisdn]}


def calc_day_data(df):
    esn = df['esn'].values
    rsrp = list(filter(lambda x: int(x) != setting.INVALID_VALUE, df['RSRP'].values))
    max_rsrp = get_max(rsrp)
    min_rsrp = get_min(rsrp)
    sum_rsrp = get_sum(rsrp)
    cnt_rsrp = len(rsrp)

    cqi = list(filter(lambda x: int(x) != setting.INVALID_VALUE, df['CQI'].values))
    max_cqi = get_max(cqi)
    min_cqi = get_min(cqi)
    sum_cqi = get_sum(cqi)
    cnt_cqi = len(cqi)

    rsrq = list(filter(lambda x: int(x) != setting.INVALID_VALUE, df['RSRQ'].values))
    max_rsrq = get_max(rsrq)
    min_rsrq = get_min(rsrq)
    sum_rsrq = get_sum(rsrq)
    cnt_rsrq = len(rsrq)

    rssi = list(filter(lambda x: int(x) != setting.INVALID_VALUE, df['RSSI'].values))
    max_rssi = get_max(rssi)
    min_rssi = get_min(rssi)
    sum_rssi = get_sum(rssi)
    cnt_rssi = len(rssi)

    sinr = list(filter(lambda x: int(x) != setting.INVALID_VALUE, df['SINR'].values))
    max_sinr = get_max(sinr)
    min_sinr = get_min(sinr)
    sum_sinr = get_sum(sinr)
    cnt_sinr = len(sinr)

    wifi = list(df['WiFiUserQty'].dropna().values)
    sum_wifi = get_sum(wifi)
    cnt_wifi = len(wifi)
    host = list(df['HostNumberOfEntries'].dropna().values)
    sum_host = get_sum(host)
    cnt_host = len(host)

    dl_throughput = list(filter(lambda x: x != setting.INVALID_VALUE, df['MaxDLThroughput'].values))
    sum_dl_throughput = get_sum(dl_throughput)
    cnt_dl_throughput = len(dl_throughput)

    ul_throughput = list(filter(lambda x: x != setting.INVALID_VALUE, df['MaxULThroughput'].values))
    sum_ul_throughput = get_sum(ul_throughput)
    cnt_ul_throughput = len(ul_throughput)

    total_value = calc_sort_collect_time(df)
    if float(total_value['TotalDownload'][0]) / setting.mb > 10:
        is_active = 1
    else:
        is_active = 0

    data = {'esn': esn[0],
            'MaxRSRP': [max_rsrp],
            'MinRSRP': [min_rsrp],
            'AvgRSRP': [sum_rsrp],
            'CntRSRP': [cnt_rsrp],
            'MaxCQI': [max_cqi],
            'MinCQI': [min_cqi],
            'AvgCQI': [sum_cqi],
            'CntCQI': [cnt_cqi],
            'MaxRSRQ': [max_rsrq],
            'MinRSRQ': [min_rsrq],
            'AvgRSRQ': [sum_rsrq],
            'CntRSRQ': [cnt_rsrq],
            'MaxRSSI': [max_rssi],
            'MinRSSI': [min_rssi],
            'AvgRSSI': [sum_rssi],
            'CntRSSI': [cnt_rssi],
            'MaxSINR': [max_sinr],
            'MinSINR': [min_sinr],
            'AvgSINR': [sum_sinr],
            'CntSINR': [cnt_sinr],
            'TotalDownload': total_value['TotalDownload'],
            'TotalUpload': total_value['TotalUpload'],
            'TotalConnectTime': total_value['TotalConnectTime'],
            'ModelName': total_value['ModelName'],
            'IMSI': total_value['IMSI'],
            'IMEI': total_value['IMEI'],
            'MSISDN': total_value['MSISDN'],
            'isActive': [is_active],
            'AvgDlThroughput': [sum_dl_throughput],
            'CntDlThroughput': [cnt_dl_throughput],
            'AvgUlThroughput': [sum_ul_throughput],
            'CntUlThroughput': [cnt_ul_throughput],
            'WiFiUserQty': [sum_wifi],
            'CntWiFiUserQty': [cnt_wifi],
            'HostNumberOfEntries': [sum_host],
            'CntHostNumberOfEntries': [cnt_host]}

    result = pd.DataFrame(data)
    return result


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
    all_day = compress.get_all_csv_file(os.path.join(setting.data_path, 'extractData'))
    day_list = []
    for day in all_day:
        day_list.append(day.split("_")[0].split("\\")[-1])
    return list(set(day_list))


def merge_day_data(day):
    print(day)
    df = pd.DataFrame(columns=setting.parameter_json["extract_data_columns"])
    all_file = compress.get_all_csv_file(os.path.join(setting.data_path, 'extractData'))
    all_day_file = list(filter(lambda x: day in x, all_file))
    for file in all_day_file:
        print(file)
        file_df = pd.read_csv(file, error_bad_lines=False, index_col=False)
        df = df.append(file_df)
    grouped = df.groupby(['esn']).apply(calc_day_data)
    df = pd.DataFrame(grouped)
    df['date'] = day
    df.to_csv(os.path.join(setting.data_path, 'day', day + r".csv"), index=False)


def day_extract():
    compress.empty_folder(os.path.join(setting.data_path, 'day'))
    all_day = get_all_day()
    for day in all_day:
        merge_day_data(day)


if __name__ == '__main__':
    print(time.localtime(time.time()))
    day_extract()
    print(time.localtime(time.time()))
