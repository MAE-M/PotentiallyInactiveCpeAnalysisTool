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
import pandas as pd

day_path = r"F:\test\data\day"
train_file = r"F:\jianpuzhai\output\with_upload\old_trainData.csv"
pre_file = r"F:\jianpuzhai\output\with_upload\old_predictData.csv"

all_file = compress.get_all_csv_file(day_path)
month3to5_file = list(filter(lambda x: '202003' in x or '202004' in x or '202005' in x, all_file))
print(month3to5_file)

month4to5_file = list(filter(lambda x: '202004' in x or '202005' in x, all_file))
print(month4to5_file)

month5_file = list(filter(lambda x:'202005' in x, all_file))

df3to5 = pd.DataFrame(columns=["esn","MaxRSRP","MinRSRP","AvgRSRP","CntRSRP","MaxCQI","MinCQI","AvgCQI","CntCQI","MaxRSRQ","MinRSRQ","AvgRSRQ","CntRSRQ","MaxRSSI","MinRSSI","AvgRSSI","CntRSSI","MaxSINR","MinSINR","AvgSINR","CntSINR","TotalDownload","TotalUpload","TotalConnectTime","ModelName","IMSI","IMEI","MSISDN","isActive","ECGI","AllCampedCell","AvgDlThroughput","CntDlThroughput","AvgUlThroughput","CntUlThroughput","WiFiUserQty","CntWiFiUserQty","HostNumberOfEntries","CntHostNumberOfEntries","date"])

for file in month3to5_file:
    df3to5 = df3to5.append(pd.read_csv(file, error_bad_lines=False, index_col=False))

esn_3to5 = set(df3to5['esn'].values)
print(esn_3to5)

df4to5 = pd.DataFrame(columns=["esn","MaxRSRP","MinRSRP","AvgRSRP","CntRSRP","MaxCQI","MinCQI","AvgCQI","CntCQI","MaxRSRQ","MinRSRQ","AvgRSRQ","CntRSRQ","MaxRSSI","MinRSSI","AvgRSSI","CntRSSI","MaxSINR","MinSINR","AvgSINR","CntSINR","TotalDownload","TotalUpload","TotalConnectTime","ModelName","IMSI","IMEI","MSISDN","isActive","ECGI","AllCampedCell","AvgDlThroughput","CntDlThroughput","AvgUlThroughput","CntUlThroughput","WiFiUserQty","CntWiFiUserQty","HostNumberOfEntries","CntHostNumberOfEntries","date"])

for file in month4to5_file:
    df4to5 = df4to5.append(pd.read_csv(file, error_bad_lines=False, index_col=False))

esn_4to5 = set(df4to5['esn'].values)
print(esn_4to5)

df5 = pd.DataFrame(columns=["esn","MaxRSRP","MinRSRP","AvgRSRP","CntRSRP","MaxCQI","MinCQI","AvgCQI","CntCQI","MaxRSRQ","MinRSRQ","AvgRSRQ","CntRSRQ","MaxRSSI","MinRSSI","AvgRSSI","CntRSSI","MaxSINR","MinSINR","AvgSINR","CntSINR","TotalDownload","TotalUpload","TotalConnectTime","ModelName","IMSI","IMEI","MSISDN","isActive","ECGI","AllCampedCell","AvgDlThroughput","CntDlThroughput","AvgUlThroughput","CntUlThroughput","WiFiUserQty","CntWiFiUserQty","HostNumberOfEntries","CntHostNumberOfEntries","date"])

for file in month5_file:
    df5 = df5.append(pd.read_csv(file, error_bad_lines=False, index_col=False))

esn_5 = list(set(df5['esn'].values))

train_df = pd.read_csv(train_file, error_bad_lines=False, index_col=False)
pre_df = pd.read_csv(pre_file, error_bad_lines=False, index_col=False)

print(train_df.shape[0])
print(pre_df.shape[0])

train_df = train_df[(train_df['esn'].isin(list(esn_3to5)))]
pre_df = pre_df[(pre_df['esn'].isin(list(esn_4to5)))]

print(train_df.shape[0])
print(pre_df.shape[0])

train_df['churnLabel'] = train_df.esn.apply(lambda x: 0 if x in esn_5 else 1)

train_df.to_csv(r"F:\jianpuzhai\output\with_upload\trainData.csv",index=False)
pre_df.to_csv(r"F:\jianpuzhai\output\with_upload\predictData.csv",index=False)