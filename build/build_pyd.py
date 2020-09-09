# Copyright (c) 2020. Huawei Technologies Co., Ltd.
# foss@huawei.com

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import os
from distutils.core import setup
from Cython.Build import cythonize

app_path, filename = os.path.split(os.path.abspath(__file__))
app_path = os.path.abspath(os.path.join(app_path, ".."))


def get_need_compile_files():
    need_compile_files = []
    exclude_files = ['__init__.py', 'PotentiallyInactiveCpeAnalysisTool.py']
    file_path = os.path.join(app_path, "src")
    for path, dir_list, file_list in os.walk(file_path):
        for f in file_list:
            if f.endswith('.py') and (f not in exclude_files):
                need_compile_files.append(os.path.join(path, f))
    return need_compile_files


target_compile_files = get_need_compile_files()

setup(
    name='Potentially inactive CPE analysis tool',
    ext_modules=cythonize(target_compile_files),
)
