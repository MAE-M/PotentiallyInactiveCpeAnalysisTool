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

from src.logger_setting.my_logger import get_logger

logger = get_logger()


def get_file(path):
    return os.path.join(path, os.listdir(path)[0])


def get_df(path):
    file = get_file(path)
    df = pd.read_csv(file, error_bad_lines=False, index_col=False)
    return df
