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
from src.cpePaser import day_extract
from src.cpePaser import month_extract
import os
from src.compress import compress
import pandas as pd
from src.setting import setting
from src.timeOperator import timeOpt
import time
import multiprocessing


MONTH1 = '1'
MONTH2 = '2'
TRAIN = '0'
PREDICT = '1'
MAX_INVALID_VALUE = 9999


def get_data_by_range(first_day, last_day):
    df = pd.DataFrame(columns=setting.month_column_name)
    date_file_map = week_extract.get_date_map()
    print(date_file_map)
    for k, v in date_file_map.items():
        if timeOpt.is_in_time(k, first_day, last_day):
            print(v)
            day_df = pd.read_csv(v, error_bad_lines=False, index_col=False)[setting.month_column_name]
            day_df['date'] = k
            df = df.append(day_df)
    return df


def build_feature(df):
    start_day = week_extract.get_min_month()
    print("begin build_feature")
    df_train = df[(df['date'] >= start_day) & (df['date'] < timeOpt.add_months(start_day, 2))]
    df_pre = df[(df['date'] >= timeOpt.add_months(start_day, 1)) & (df['date'] < timeOpt.add_months(start_day, 3))]
    df_for_churn = set(
        df[(df['date'] >= timeOpt.add_months(start_day, 2)) & (df['date'] < timeOpt.add_months(start_day, 3))][
            'esn'].values)

    compress.empty_folder(setting.model_path)
    train_result_df = build(df_train, df_for_churn, TRAIN)
    train_result_df.to_csv(os.path.join(setting.model_path, r"trainData.csv"), index=False)
    pre_result_df = build(df_pre, df_for_churn, PREDICT)
    pre_result_df[(pre_result_df['churnLabel'] < 1)].to_csv(
        os.path.join(setting.model_path, r"predictData.csv"), index=False)
    return 0


def build(data, not_churn_esn, build_type):
    print("begin build")
    df_rsrp_sinr = get_rsrp_df(data)

    result_df = calc_week(data, build_type)

    df_month1 = calc_month(data, MONTH1, build_type)
    df_month2 = calc_month(data, MONTH2, build_type)
    result_df = merge_data(result_df, df_month1)
    result_df = merge_data(result_df, df_month2)
    result_df = merge_data(result_df, df_rsrp_sinr)

    result_df['churnLabel'] = result_df.esn.apply(lambda x: 0 if x in not_churn_esn else 1)
    result_df = pd.DataFrame(result_df, columns=setting.parameter_json["xgboost_columns"])
    result_df['dlTrafficMonth2Compare1'] = result_df.apply(
        lambda x: calc_compare(x['dlTrafficMonth1'], x['dlTrafficMonth2']), axis=1)
    result_df['ulTrafficMonth2Compare1'] = result_df.apply(
        lambda x: calc_compare(x['ulTrafficMonth1'], x['ulTrafficMonth2']), axis=1)
    result_df['dlTrafficPerdayMonth2Compare1'] = result_df.apply(
        lambda x: calc_compare(x['dlTrafficPerdayMonth1'], x['dlTrafficPerdayMonth2']), axis=1)
    result_df['ulTrafficPerdayMonth2Compare1'] = result_df.apply(
        lambda x: calc_compare(x['ulTrafficPerdayMonth1'], x['ulTrafficPerdayMonth2']), axis=1)
    result_df['ulTrafficPerdayMonth2Compare1'] = result_df.apply(
        lambda x: calc_compare(x['totalDlUlTrafficPerdayMonth1'], x['totalDlUlTrafficPerdayMonth2']), axis=1)
    result_df['connectTimeMonth2Compare1'] = result_df.apply(
        lambda x: calc_compare(x['totalConnectTimeMonth1'], x['totalConnectTimeMonth2']), axis=1)
    result_df['ulDlTrafficPerdayMonth2Compare1'] = result_df.apply(
        lambda x: calc_compare(x['totalDlUlTrafficPerdayMonth1'], x['totalDlUlTrafficPerdayMonth2']), axis=1)
    result_df['dlTrafficWeek9Compare8'] = result_df.apply(
        lambda x: calc_compare(x['TotalDownloadWeek8'], x['TotalDownloadWeek9']), axis=1)
    result_df['dlTrafficWeek8Compare7'] = result_df.apply(
        lambda x: calc_compare(x['TotalDownloadWeek7'], x['TotalDownloadWeek8']), axis=1)
    result_df['ulTrafficWeek9Compare8'] = result_df.apply(
        lambda x: calc_compare(x['TotalUploadWeek8'], x['TotalUploadWeek9']), axis=1)
    result_df['ulTrafficWeek8Compare7'] = result_df.apply(
        lambda x: calc_compare(x['TotalUploadWeek7'], x['TotalUploadWeek8']), axis=1)
    result_df['connectTimeWeek9Compare8'] = result_df.apply(
        lambda x: calc_compare(x['TotalConnectTimeWeek8'], x['TotalConnectTimeWeek9']), axis=1)
    result_df['connectTimeWeek8Compare7'] = result_df.apply(
        lambda x: calc_compare(x['TotalConnectTimeWeek7'], x['TotalConnectTimeWeek8']), axis=1)
    return result_df


def calc_compare(data1, data2):
    if not data1 and not data2:
        return MAX_INVALID_VALUE
    elif not data1:
        return MAX_INVALID_VALUE
    elif not data2:
        return -1
    else:
        return (data2 - data1) / data1


def get_rsrp_df(df):
    train_group_month = day_extract.groupby_calc(df).apply(calc_rsrp_month).reset_index(drop=True)
    df = pd.DataFrame(train_group_month)
    return df


def calc_rsrp_month(df):
    esn = df['esn'].values
    rsrp_sinr = month_extract.calc_rsrp_sinr(df)
    data = {'esn': esn[0],
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


def calc_week(df, build_type):
    if build_type == TRAIN:
        week_list = week_extract.get_train_week()
    else:
        week_list = week_extract.get_pre_week()
    result_df = pd.DataFrame(columns=['esn'])
    for week in week_list:
        week_df = df[(df['date'] >= week[1]) & (df['date'] < week[2])]
        grouped = day_extract.groupby_calc(week_df).apply(week_extract.calc_week_data).reset_index(drop=True)
        week_df = pd.DataFrame(grouped).rename(columns={'TotalDownload': 'TotalDownloadWeek' + str(week[0]),
                                                        'TotalUpload': 'TotalUploadWeek' + str(week[0]),
                                                        'TotalConnectTime': 'TotalConnectTimeWeek' + str(week[0])})
        result_df = merge_data(result_df, week_df)
    return result_df


def calc_month(df, month_type, build_type):
    start_day = week_extract.get_min_month()
    if build_type == TRAIN and month_type == MONTH1:
        df_month = df[(df['date'] >= start_day) & (df['date'] < timeOpt.add_months(start_day, 1))]
    elif (build_type == TRAIN and month_type == MONTH2) or (build_type == PREDICT and month_type == MONTH1):
        df_month = df[
            (df['date'] >= timeOpt.add_months(start_day, 1)) & (df['date'] < timeOpt.add_months(start_day, 2))]
    else:
        df_month = df[
            (df['date'] >= timeOpt.add_months(start_day, 2)) & (df['date'] < timeOpt.add_months(start_day, 3))]

    group_month1 = day_extract.groupby_calc(df_month).apply(month_extract.calc_month_data).reset_index(drop=True)
    df = pd.DataFrame(group_month1)\
        .rename(columns={'activeDay': 'activeDayMonth' + month_type,
                         'totalConnectTime': 'totalConnectTimeMonth' + month_type,
                         'dlTraffic': 'dlTrafficMonth' + month_type,
                         'ulTraffic': 'ulTrafficMonth' + month_type,
                         'totalDlUlTrafficMonthly': 'totalDlUlTrafficMonthly' + month_type,
                         'dlTrafficRatioMonthly': 'dlTrafficRatioMonthly' + month_type,
                         'totalDlUlTrafficPerday': 'totalDlUlTrafficPerdayMonth' + month_type,
                         'dlTrafficPerday': 'dlTrafficPerdayMonth' + month_type,
                         'ulTrafficPerday': 'ulTrafficPerdayMonth' + month_type,
                         'totalConnectTimePerday': 'totalConnectTimePerdayMonth' + month_type,
                         'MinRSRP': 'MinRSRPMonth' + month_type,
                         'MaxRSRP': 'MaxRSRPMonth' + month_type,
                         'AvgRSRP': 'AvgRSRPMonth' + month_type,
                         'StdRSRP': 'StdRSRPMonth' + month_type,
                         'MinSINR': 'MinSINRMonth' + month_type,
                         'MaxSINR': 'MaxSINRMonth' + month_type,
                         'AvgSINR': 'AvgSINRMonth' + month_type,
                         'StdSINR': 'StdSINRMonth' + month_type})
    return df


def merge_data(df1, df2):
    if not df2.empty:
        df1 = pd.merge(df1, df2, on='esn', how='outer')
    return df1


def run():
    multiprocessing.freeze_support()
    start_day = week_extract.get_min_month()
    df = get_data_by_range(start_day, timeOpt.add_months(start_day, 3))
    build_feature(df)


if __name__ == '__main__':
    print(time.localtime(time.time()))
    run()
    print(time.localtime(time.time()))
