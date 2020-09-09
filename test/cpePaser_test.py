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
from src.compress import compress
import pandas as pd

if __name__ == '__main__':
    all_file = compress.get_all_csv_file(compress.cpe_unzip_path)
    new_file = list(filter(lambda x: 'export_monitordata' in x, all_file))
    print(new_file)
    filter_df = pd.read_csv(new_file[0], error_bad_lines=False, index_col=False)
    filter_df = filter_df[(filter_df['ESN'] == 'YRE7S17B25000055') | (filter_df['ESN'] == 'YRE7S18209004018') | (
                filter_df['ESN'] == 'YRE7S17B25003854')]
    for f in new_file[1:]:
        print(f)
        df = pd.read_csv(f, error_bad_lines=False, index_col=False)
        new_df = df[
            (df['ESN'] == 'YRE7S17B25000055') | (df['ESN'] == 'YRE7S18209004018') | (df['ESN'] == 'YRE7S17B25003854')]
        new_df = pd.DataFrame(new_df)
        if not new_df.empty:
            print(new_df)
            filter_df = filter_df.append(new_df)
    filter_df.to_csv(os.path.join(compress.cpe_unzip_path, 'filter.csv'), index=False)
