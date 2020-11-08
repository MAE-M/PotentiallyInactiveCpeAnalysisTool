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
import sys
import json

import numpy as np

if hasattr(sys, '_MEIPASS'):
    app_path = os.path.dirname(os.path.realpath(sys.executable))
else:
    app_path, filename = os.path.split(os.path.abspath(__file__))
    app_path = os.path.abspath(os.path.join(app_path, ".."))

setting_path = os.path.join(app_path, 'setting')

my_logger_path = os.path.abspath(os.path.join(os.path.join(setting_path, '..'), 'logger_setting'))

template_path = os.path.join(setting_path, 'template')
template_file = os.path.join(template_path, 'LTE_template.zip')

# 1920x1080分辨率下的像素数量
resolution_1920x1080_pixel_width = 1920
resolution_1920x1080_pixel_height = 1080

outer_frame_in_1920x1080_pixel_width = 1000
outer_frame_in_1920x1080_pixel_height = 1000
outer_frame_padx_in_1920x1080_pixel = 20
outer_frame_pady_in_1920x1080_pixel = 20

inner_frame_padx_in_1920x1080_pixel = 5
inner_frame_pady_in_1920x1080_pixel = 5
inner_frame_in_1920x1080_pixel_width = 800
inner_frame_in_1920x1080_pixel_height = 300

font_size_in_1920x1080_pixel = 17

label_in_1920x1080_pixel_width = 10
label_in_1920x1080_pixel_height = 5

entry_in_1920x1080_pixel_width = 10
entry_in_1920x1080_pixel_height = 5

button_ipadx_in_1920x1080_pixel = 10
button_ipady_in_1920x1080_pixel = 1
button_padx_in_1920x1080_pixel = 3
button_pady_in_1920x1080_pixel = 3

ratChoice_in_1920x1080_pixel_width = 20
ratChoice_in_1920x1080_pixel_height = 0
ratChoice_ipadx_in_1920x1080_pixel = 1
ratChoice_ipady_in_1920x1080_pixel = 0
ratChoice_padx_in_1920x1080_pixel = 1
ratChoice_pady_in_1920x1080_pixel = 1

log_text_in_1920x1080_pixel_width = 100
log_text_in_1920x1080_pixel_height = 20

thre_template_file_name = 'Performance_Evaluation_Threshold_Template_V1.csv'
thre_template_file = os.path.join(template_path, thre_template_file_name)
thre_data_path = os.path.join(setting_path, 'thresholdParam')

cpe_data_path = os.path.join(setting_path, 'cpeLogZip')

exper_data_path = os.path.join(setting_path, 'experienceData')

capa_data_path = os.path.join(setting_path, 'capacityData')

data_path = os.path.join(app_path, 'data')

if not os.path.exists(data_path):
    os.mkdir(data_path)

if not os.path.exists(my_logger_path):
    os.mkdir(my_logger_path)

post_eva_path = os.path.join(data_path, 'postEva')

column_name = ['collectTime', 'esn', 'TotalDownload', 'TotalUpload', 'TotalConnectTime', 'MaxDLThroughput',
               'MaxULThroughput', 'RSRP', 'RSRQ', 'RSSI', 'SINR', 'WiFiUserQty', 'CQI', 'ModelName', 'IMSI', 'IMEI',
               'MSISDN', 'ECGI', 'HostNumberOfEntries']

month_column_name = ['esn', 'TotalDownload', 'TotalUpload', 'TotalConnectTime', 'AvgRSRP', 'isActive', 'MinRSRP',
                     'CntSINR', 'CntRSRP', 'AvgSINR', 'MinSINR', 'MaxSINR', 'MaxRSRP', 'ECGI']

parameter_path = os.path.join(setting_path, 'parameter.json')

rsrp_sinr_columns = ['MinRSRPMonth1', 'MaxRSRPMonth1', 'AvgRSRPMonth1', 'StdRSRPMonth1', 'MinRSRPMonth2',
                     'MaxRSRPMonth2',
                     'AvgRSRPMonth2', 'StdRSRPMonth2', 'MinRSRP', 'MaxRSRP', 'AvgRSRP', 'StdRSRP', 'MinSINRMonth1',
                     'MaxSINRMonth1', 'AvgSINRMonth1', 'StdSINRMonth1', 'MinSINRMonth2', 'MaxSINRMonth2',
                     'AvgSINRMonth2', 'StdSINRMonth2', 'MinSINR', 'MaxSINR', 'AvgSINR', 'StdSINR']

gb = 1024 * 1024 * 1024

mb = 1024 * 1024

model_path = os.path.join(data_path, 'model')

result_path = os.path.join(data_path, 'result')

INVALID_VALUE = -9999

INVALID_STRING = "-"

post_weak_coverage = 'Weak Coverage'
post_high_load = 'High Load'
post_high_interference = 'High Interference'

pre_for_post_columns = ['esn', 'churnLabel']

post_suite_columns = ['esn', 'IMSI', 'IMEI', 'MSISDN', 'TotalDownload', 'TotalUpload']

pre_top = 30


def load_parameter():
    with open(parameter_path, 'r') as param_json:
        param = json.load(param_json)
    return param


def write_param_json(param_json):
    with open(parameter_path, 'w') as json_file:
        json.dump(param_json, json_file)


def update_param_json(name, value):
    param_json = load_parameter()
    param_json[name] = value
    write_param_json(param_json)


parameter_json = load_parameter()

xgboost_columns = ['esn', 'TotalDownloadWeek1', 'TotalUploadWeek1', 'TotalConnectTimeWeek1', 'TotalDownloadWeek2',
                   'TotalUploadWeek2', 'TotalConnectTimeWeek2', 'TotalDownloadWeek3', 'TotalUploadWeek3',
                   'TotalConnectTimeWeek3', 'TotalDownloadWeek4', 'TotalUploadWeek4', 'TotalConnectTimeWeek4',
                   'TotalDownloadWeek5', 'TotalUploadWeek5', 'TotalConnectTimeWeek5', 'TotalDownloadWeek6',
                   'TotalUploadWeek6', 'TotalConnectTimeWeek6', 'TotalDownloadWeek7', 'TotalUploadWeek7',
                   'TotalConnectTimeWeek7', 'TotalDownloadWeek8', 'TotalUploadWeek8', 'TotalConnectTimeWeek8',
                   'TotalDownloadWeek9', 'TotalUploadWeek9', 'TotalConnectTimeWeek9', 'activeDayMonth1',
                   'totalConnectTimeMonth1', 'dlTrafficMonth1', 'ulTrafficMonth1', 'totalDlUlTrafficMonthly1',
                   'dlTrafficRatioMonthly1', 'totalDlUlTrafficPerdayMonth1', 'dlTrafficPerdayMonth1',
                   'ulTrafficPerdayMonth1', 'totalConnectTimePerdayMonth1', 'MinRSRPMonth1', 'MaxRSRPMonth1',
                   'AvgRSRPMonth1', 'StdRSRPMonth1', 'activeDayMonth2', 'totalConnectTimeMonth2', 'dlTrafficMonth2',
                   'ulTrafficMonth2', 'totalDlUlTrafficMonthly2', 'dlTrafficRatioMonthly2',
                   'totalDlUlTrafficPerdayMonth2', 'dlTrafficPerdayMonth2', 'ulTrafficPerdayMonth2',
                   'totalConnectTimePerdayMonth2', 'MinRSRPMonth2', 'MaxRSRPMonth2', 'AvgRSRPMonth2', 'StdRSRPMonth2',
                   'MinRSRP', 'MaxRSRP', 'AvgRSRP', 'StdRSRP', 'churnLabel', 'dlTrafficMonth2Compare1',
                   'ulTrafficMonth2Compare1', 'dlTrafficPerdayMonth2Compare1', 'ulTrafficPerdayMonth2Compare1',
                   'connectTimeMonth2Compare1', 'ulDlTrafficPerdayMonth2Compare1', 'dlTrafficWeek9Compare8',
                   'dlTrafficWeek8Compare7', 'ulTrafficWeek9Compare8', 'ulTrafficWeek8Compare7',
                   'connectTimeWeek9Compare8', 'connectTimeWeek8Compare7', 'ENODEBID', 'CELLID']

if __name__ == '__main__':
    print(gb)
