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

import xgboost as xgb
import os
import pandas as pd
from src.setting import setting
import json
from src.compress import compress


class PotXGBoost:
    params = setting.load_parameter()['xgboost_param']

    def __int__(self):
        self.model = ''
        self.pre_result = ''
        self.features_importance = ''

    def train(self, data):
        train_data = data.drop(['esn', 'churnLabel', 'ENODEBID', 'CELLID'], axis=1)
        label = data['churnLabel']
        dtain = xgb.DMatrix(train_data, label=label)
        self.model = xgb.train(PotXGBoost.params, dtain)
        self.features_importance = self.model.get_fscore()

    def predict(self, data):
        pre_data = data.drop(['esn', 'churnLabel', 'ENODEBID', 'CELLID'], axis=1)
        dpredict = xgb.DMatrix(pre_data)
        result = self.model.predict(dpredict)
        result_df = pd.DataFrame(result).rename(columns={0: "churnLabel"})
        self.pre_result = pd.concat([data.drop(['churnLabel'], axis=1), result_df], axis=1)\
            .sort_values('churnLabel', ascending=False, ignore_index=True)

    def save_model(self, path):
        self.model.save_model(path)


def get_xgboost_predict_result():
    pot_xgboost = PotXGBoost()
    data = pd.read_csv(os.path.join(setting.model_path, 'trainData.csv'), error_bad_lines=False, index_col=False)
    pre = pd.read_csv(os.path.join(setting.model_path, 'predictData.csv'), error_bad_lines=False, index_col=False)
    data = data[setting.parameter_json["train_pre_columns"]]
    pre = pre[setting.parameter_json["train_pre_columns"]]
    is_use_rsrp = setting.load_parameter()['use_rsrp_sinr']
    if not is_use_rsrp.lower() == 'true':
        data = data.drop(setting.rsrp_sinr_columns, axis=1)
        pre = pre.drop(setting.rsrp_sinr_columns, axis=1)
    pot_xgboost.train(data)
    pot_xgboost.predict(pre)
    compress.empty_folder(setting.result_path)
    pot_xgboost.pre_result.to_csv(os.path.join(setting.result_path, 'predict_result.csv'))
    importance_df = json_to_df(pot_xgboost.features_importance)
    importance_df.to_csv(os.path.join(setting.result_path, 'features_importance.csv'))


def json_to_df(json_data):
    json_data = json.loads(json.dumps(json_data))
    json_data_keys = [str(key) for key in json_data.keys()]
    json_data_values = [value for value in json_data.values()]
    keys = pd.Series(json_data_keys, name='feature')
    values = pd.Series(json_data_values, name='importance')
    df = pd.concat([keys, values], axis=1)
    return df.sort_values('importance', ascending=False, ignore_index=True)


if __name__ == '__main__':
    get_xgboost_predict_result()
