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


from src.setting import setting
from src.cpePaser import day_extract
from src.cpePaser import week_extract
import pandas as pd
from src.timeOperator import timeOpt
import numpy as np
import math
import os
from src.postEva.exper_paser import exper_paser
from src.postEva.capacity_paser import capacity_paser
from src.postEva.capacity_paser import cell


engineer_map = {}
threshold_map = {}


def get_post_df():
    min_month = week_extract.get_min_month()
    all_file = week_extract.get_file_by_range(timeOpt.add_months(min_month, 2), timeOpt.add_months(min_month, 3))
    df = pd.DataFrame(columns=setting.parameter_json["post_eva_from_day_column_name"])
    for f in all_file:
        file_df = pd.read_csv(f, error_bad_lines=False, index_col=False)[setting.parameter_json[
            "post_eva_from_day_column_name"]]
        df = df.append(file_df)
    return df


def post_evaluation():
    df = get_post_df()
    grouped = day_extract.groupby_calc(df).apply(calc_post_eva)
    result = pd.DataFrame(grouped)
    result.to_csv(os.path.join(setting.post_eva_path, 'post_eva_data.csv'), index=False)


def calc_post_eva(df):
    print(df.columns)
    esn = df['esn'].values

    total_download = np.sum(df['TotalDownload'].values) / setting.mb
    total_upload = np.sum(df['TotalUpload'].values) / setting.mb

    df_sort_by_date = df.sort_values('date')[['IMSI', 'IMEI', 'MSISDN']]
    newst_imsi = df_sort_by_date['IMSI'].values[-1]
    newst_imei = df_sort_by_date['IMEI'].values[-1]
    newst_msisdn = df_sort_by_date['MSISDN'].values[-1]

    data = {'esn': esn[0],
            'TotalDownload': [total_download],
            'TotalUpload': [total_upload],
            'IMSI': [newst_imsi],
            'IMEI': [newst_imei],
            'MSISDN': [newst_msisdn]}
    result = pd.DataFrame(data)
    return result


def exper_evaluate_with_suite():
    pre_result_df = pd.read_csv(os.path.join(setting.result_path, 'predict_result.csv'))[
        setting.pre_for_post_columns]
    total_line = pre_result_df.shape[0]
    pre_result_df = pre_result_df.head(int(total_line * setting.parameter_json["top_n"] / 100))
    post_result_df = pd.read_csv(os.path.join(setting.post_eva_path, 'post_eva_data.csv'))[setting.post_suite_columns]
    exper_df = exper_paser.get_expericece_data()
    pre_and_post_df = pd.merge(pre_result_df, post_result_df, on='esn', how='left')
    df = pd.merge(pre_and_post_df, exper_df, on='esn', how='left')
    result_df = exper_suite_analysis(df)
    result_df.loc[result_df['IMEI'] == 0, 'IMEI'] = '-'
    result_df.loc[result_df['MSISDN'] == 0, 'MSISDN'] = '-'
    result_df.loc[result_df['CPE Model'] == 0, 'CPE Model'] = '-'
    result_df.replace(setting.INVALID_VALUE, '-').to_csv(os.path.join(setting.result_path, 'post_analysis_result.csv'),
                                                         index=False)


def exper_suite_analysis(df):
    global threshold_map
    threshold_map = setting.load_parameter().get('threshold')
    df = exper_paser.exper_analysis(df)
    df['Low Traffic Index'] = df.apply(lambda x: is_low_traffic(x['TotalDownload']), axis=1)
    df['High Wifi User Index'] = df.apply(
        lambda x: is_over_wifi_user(x['Activated Wi-Fi Connections'], x['Max. Host Connections']), axis=1)
    df = df.drop(['Poor-Performance CPE Analysis'], axis=1).rename(
        columns=setting.parameter_json["post_with_suite_result_rename"])
    return df


def is_low_traffic(value):
    if (float(value) / 1024) < float(threshold_map['Threshold for Low Traffic']):
        return 'Yes'
    else:
        return 'No'


def is_over_wifi_user(wifi_user, host_connect):
    if type(wifi_user) == str and wifi_user == '-':
        wifi_user = setting.INVALID_VALUE
    else:
        wifi_user = float(wifi_user)

    if type(host_connect) == str and host_connect == '-':
        host_connect = setting.INVALID_VALUE
    else:
        host_connect = float(host_connect)

    if wifi_user >= 0:
        if wifi_user > threshold_map['Threshold for High Wi-Fi User Number']:
            return 'Yes'
        else:
            return 'No'
    elif host_connect >= 0:
        if host_connect > threshold_map['Threshold for High Wi-Fi User Number']:
            return 'Yes'
        else:
            return 'No'
    elif (not wifi_user and not host_connect) or (wifi_user < 0 and host_connect < 0) \
            or (math.isnan(wifi_user) and math.isnan(host_connect)):
        return '-'
    else:
        return 'No'


def merge_exper_capa_data():
    exper_df = pd.read_csv(os.path.join(setting.result_path, 'post_analysis_result.csv'))
    exper_cell_map = statistic_reson_by_cell(exper_df)
    capa_df = capacity_paser.get_capacity_data()
    capa_df['Poor Performance CPEs'] = capa_df.apply(
        lambda x: exper_cell_map[(float(x['eNodeB ID']), float(x['Cell ID']))].poor_performace_nums
        if (float(x['eNodeB ID']), float(x['Cell ID'])) in exper_cell_map.keys() else '-', axis=1)
    capa_df['Potentially Inactive CPEs'] = capa_df.apply(
        lambda x: exper_cell_map[(float(x['eNodeB ID']), float(x['Cell ID']))].pot_inactive_nums
        if (float(x['eNodeB ID']), float(x['Cell ID'])) in exper_cell_map.keys() else '-', axis=1)
    capa_df['Weak Coverage CPEs'] = capa_df.apply(
        lambda x: exper_cell_map[(float(x['eNodeB ID']), float(x['Cell ID']))].weak_converage_nums
        if (float(x['eNodeB ID']), float(x['Cell ID'])) in exper_cell_map.keys() else '-', axis=1)
    capa_df['High Load CPEs'] = capa_df.apply(
        lambda x: exper_cell_map[(float(x['eNodeB ID']), float(x['Cell ID']))].high_load_nums
        if (float(x['eNodeB ID']), float(x['Cell ID'])) in exper_cell_map.keys() else '-', axis=1)
    capa_df['High Interference CPEs'] = capa_df.apply(
        lambda x: exper_cell_map[(float(x['eNodeB ID']), float(x['Cell ID']))].high_interference_nums
        if (float(x['eNodeB ID']), float(x['Cell ID'])) in exper_cell_map.keys() else '-', axis=1)
    capa_df.to_csv(os.path.join(setting.result_path, 'capacity_analysis_result.csv'), index=False, encoding='utf_8_sig')


def statistic_reson_by_cell(df):
    cell_map = {}
    for index, row in df.iterrows():
        if (type(row['eNodeB ID']) == float and math.isnan(row['eNodeB ID'])) or (
                type(row['Cell ID']) == float and math.isnan(row['Cell ID'])) or str(row['eNodeB ID']) == '-' or str(
                row['Cell ID']) == '-':
            continue
        key = (float(row['eNodeB ID']), float(row['Cell ID']))
        if key in cell_map.keys():
            one_cell = cell_map[key]
            cell_map[key] = statistic_one_cell(one_cell, row)
        else:
            key = (float(row['eNodeB ID']), float(row['Cell ID']))
            one_cell = cell.Cell()
            one_cell.enodeb_id = float(row['eNodeB ID'])
            one_cell.cell_id = float(row['Cell ID'])
            cell_map[key] = statistic_one_cell(one_cell, row)
    return cell_map


def statistic_one_cell(one_cell, row):
    one_cell.add_high_interference(1 if row['High Interference CPE Index'] == 'Yes' else 0)
    one_cell.add_high_load(1 if row['High Load CPE Index'] == 'Yes' else 0)
    one_cell.add_poor_performance(1 if row['Low Throughput CPE Index'] == 'Yes' else 0)
    one_cell.add_pot_inactive(1)
    one_cell.add_weak_converage(1 if row['Weak Coverage CPE Index'] == 'Yes' else 0)
    return one_cell


def main(has_suite):
    post_evaluation()
    if has_suite:
        exper_evaluate_with_suite()
        merge_exper_capa_data()


if __name__ == '__main__':
    main(True)
