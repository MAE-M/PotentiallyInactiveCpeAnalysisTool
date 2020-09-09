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


from src.postEva import util
from src.setting import setting


def get_expericece_data():
    exper_df = util.get_df(setting.exper_data_path)[setting.parameter_json["experience_df_extract_columns"]].rename(
        columns=setting.parameter_json["experience_df_columns_rename"])
    return exper_df


def exper_analysis(exper_df):
    exper_df['Weak Coverage CPE Index'] = exper_df.apply(
        lambda x: post_analysis(x['Poor-Performance CPE Analysis'], setting.post_weak_coverage), axis=1)
    exper_df['High Interference CPE Index'] = exper_df.apply(
        lambda x: post_analysis(x['Poor-Performance CPE Analysis'], setting.post_high_interference), axis=1)
    exper_df['High Load CPE Index'] = exper_df.apply(
        lambda x: post_analysis(x['Poor-Performance CPE Analysis'], setting.post_high_load), axis=1)
    return exper_df


def post_analysis(value, post_type):
    value = str(value)
    if not value or str(value) == 'nan':
        return setting.INVALID_STRING
    elif post_type in value:
        return 'Yes'
    else:
        return 'No'


if __name__ == '__main__':
    print(get_expericece_data()["CPE Movement Index"])
