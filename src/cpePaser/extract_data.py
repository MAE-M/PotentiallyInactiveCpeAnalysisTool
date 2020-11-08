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

import numpy

from src.compress import compress
import pandas as pd
import re
from src.setting import setting
import time
import math

from src.logger_setting.my_logger import get_logger

logger = get_logger()

PAT_DATA = re.compile(r"\d+.+\d+")
PAT_NUM = re.compile(r"\d+")
PAT_DATA_LOW = re.compile(r"-?\d+")
PAT_CQI0 = re.compile(r"CQI0.+?(\d+)")
PAT_CQI1 = re.compile(r"CQI1.+?(\d+)")
PAT_ECGI = re.compile(r"\d+-\d+")


def get_extract_data():
    compress.empty_folder(os.path.join(setting.data_path, 'extractData'))
    all_file = compress.get_all_csv_file(compress.cpe_unzip_path)
    return all_file


def extract_data_thread(file):
    if not os.stat(file).st_size > 0:
        return
    df = pd.DataFrame(columns=setting.parameter_json["extract_data_columns"]).rename(
        columns=setting.parameter_json["extract_data_columns_rename"])
    file_df = pd.read_csv(file, error_bad_lines=False, index_col=False, engine='python').rename(
        columns=setting.parameter_json["extract_data_columns_rename"])
    if not file_df.empty:
        file_df['collectTime'] = pd.to_datetime(file_df['collectTime'])
        file_df['collectTime'] = file_df.collectTime.dt.strftime('%Y-%m-%d %H:%M:%S')
        date = str(file_df['collectTime'].values[0]).split(" ")[0].replace("-", "").replace("/", "")
        df = df.append(file_df)
        df = day_data_operate(df)
        now_time = str(int(round(time.time() * 10000)))
        df.to_csv(os.path.join(setting.data_path, 'extractData', date + '_' + now_time + r".csv"), index=False)


def day_data_operate(df):
    col_names = df.columns
    col_i_need = list(filter(lambda c: get_column(c), col_names))
    df = df[col_i_need]
    df['TotalDownload'] = df['TotalDownload'].apply(lambda x: get_traffic(x, PAT_DATA))
    df['TotalUpload'] = df['TotalUpload'].apply(lambda x: get_traffic(x, PAT_DATA))
    df['MaxDLThroughput'] = df['MaxDLThroughput'].apply(lambda x: get_throughput(x, PAT_DATA))
    df['MaxULThroughput'] = df['MaxULThroughput'].apply(lambda x: get_throughput(x, PAT_DATA))
    df['RSRP'] = df['RSRP'].apply(lambda x: get_number(x, PAT_DATA_LOW))
    df['RSRQ'] = df['RSRQ'].apply(lambda x: get_number(x, PAT_DATA_LOW))
    df['RSSI'] = df['RSSI'].apply(lambda x: get_number(x, PAT_DATA_LOW))
    df['SINR'] = df['SINR'].apply(lambda x: get_number(x, PAT_DATA_LOW))
    df['CQI'] = df['CQI'].apply(get_cqi)
    df.loc[:, 'ECGI'] = df.apply(lambda x: get_ecgi(x['ECGI'], PAT_ECGI, x['ENODEBID'], x['CELLID']), axis=1)
    return df


def get_data(value):
    if type(value) == float and math.isnan(value):
        return ''
    else:
        return value


def get_column(column):
    columns_name = setting.parameter_json.get("extract_filter_columns")
    for i in range(0, len(columns_name)):
        if re.match(columns_name[i], column):
            return True
    return False


def get_number(data, pat, invalid_value=setting.INVALID_VALUE):
    result = pat.findall(str(data))
    if result:
        return float(result[0])
    else:
        return invalid_value


# 流量转化为 Byte
def get_traffic(data, pat):
    str_data = str(data)
    result = get_number(data, pat, 0)
    if result != 0:
        if "KB" in str_data:
            return result * 1024
        elif "MB" in str_data:
            return result * 1024 * 1024
        elif "GB" in str_data:
            return result * 1024 * 1024 * 1024
        else:
            return result * setting.parameter_json["to_Byte"] if result != setting.INVALID_VALUE else result
    else:
        return result


# 速率转Mbps
def get_throughput(data, pat):
    str_data = str(data)
    result = get_number(data, pat)
    if result != setting.INVALID_VALUE:
        if "Byte/s" in str_data:
            return result * 8 / 1024 / 1024
        elif "B/s" in str_data:
            return result * 8 / 1024 / 1024
        elif "KB/s" in str_data:
            return result * 8 / 1024
        elif "MB/s" in str_data:
            return result * 8
        elif "GB/s" in str_data:
            return result * 8 * 1024
        elif "Kbps" in str_data:
            return result / 1024
        elif "bps" in str_data:
            return result / 1024 / 1024
        else:
            return result
    else:
        return result


def get_ecgi(ecgi, pat, enodebid, cellid):
    result = pat.findall(str(ecgi))
    if result:
        rel_ecgi = PAT_NUM.findall(result[0])
        return str(int(rel_ecgi[0])) + "-" + str(int(rel_ecgi[1]))
    elif pat.findall(str(cellid)):
        result = pat.findall(str(cellid))
        rel_ecgi = PAT_NUM.findall(result[0])
        return str(int(rel_ecgi[0])) + "-" + str(int(rel_ecgi[1]))
    elif (type(enodebid) == float and math.isnan(enodebid)) or (type(cellid) == float and math.isnan(cellid)):
        return setting.INVALID_STRING
    else:
        return str(int(enodebid)) + "-" + str(int(cellid))


def get_cqi(data):
    if 'CQI' in str(data):
        result = get_number(data, PAT_CQI0)
        if result == '127' or int(result) < 0:
            result = get_number(data, PAT_CQI1)
            if result == '127' or int(result) < 0:
                return setting.INVALID_VALUE
        return result
    else:
        result = get_number(data, PAT_DATA)
        if result == '127' or int(result) < 0:
            return setting.INVALID_VALUE
        else:
            return result


def extract_data():
    all_files = get_extract_data()
    for file in all_files:
        extract_data_thread(file)


if __name__ == '__main__':
    print(time.localtime(time.time()))
    extract_data()
    print(time.localtime(time.time()))
