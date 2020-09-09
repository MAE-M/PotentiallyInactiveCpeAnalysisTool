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

path = r"F:\test\CpeLog_data_20200520174328\CpeLog_data.csv"

workspace = r'F:\test\CpeLog_data_20200520174328'

# with open(path, 'r', newline='') as file:
#     csvreader = csv.reader(file)
#     a = next(csvreader)
#     print(a)
#     i = j = 0
#     for row in csvreader:
#         f_name = row[0].split(" ")[0].replace("-", "")
#         print(f_name)
#         print(f'i is {i}, j is {f_name}')
#
#         csv_path = os.path.join(workspace, 'part_{}.csv'.format(f_name))
#
#         print(csv_path)
#         # 不存在此文件的时候，就创建
#         if not os.path.exists(csv_path):
#             with open(csv_path, 'w', newline='') as file:
#                 csvwriter = csv.writer(file)
#                 #csvwriter.writerow(['image_url'])
#                 print(a)
#                 csvwriter.writerow(a)
#                 csvwriter.writerow(row)
#             # with open(csv_path, 'a', newline='') as file:
#             #     csvwriter = csv.writer(file)
#             #     csvwriter.writerow(row)
#             i += 1
#         # 存在的时候就往里面添加
#         else:
#             with open(csv_path, 'a', newline='') as file:
#                 csvwriter = csv.writer(file)
#                 csvwriter.writerow(row)
#             i += 1
file=r"F:\test\频谱效率较好 1_73_011_2226_Wendywood_WBS_SGC_User Common Monitoring_20200722_114512@1.csv"
file_df = pd.read_csv(file, error_bad_lines=False, index_col=False)
print(file_df)
print(os.listdir(r"F:\test"))