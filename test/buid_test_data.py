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
import os

all_file = compress.get_all_csv_file(r'F:\test\data\unzipCpe')
all_cell = ['2763-231', '2845-238', '2843-231', '2843-232', '2845-233', '2843-236', '2843-237', '2843-238', '2845-231',
            '2845-232', '2843-233', '2845-236', '2845-237', '2763-236']


for f in all_file:
    df = pd.read_csv(f, error_bad_lines=False, index_col=False, engine='python')
    df = df.sort_values('ESN').head(500)
    for i in range(500):
        df.iloc[i,df.columns.get_loc('ECGI')] = all_cell[i%14]
    df.to_csv(os.path.join(r"F:\test\data\test", f.split('\\')[-1]), index=False)

