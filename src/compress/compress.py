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


import zipfile
import gzip
import os
from src.setting import setting
import re
import time

from src.logger_setting.my_logger import get_logger

logger = get_logger()
cpe_unzip_path = os.path.join(setting.data_path, 'unzipCpe')


def decompress_cpe_data():
    cpe_zip_file = os.path.join(setting.cpe_data_path, os.listdir(setting.cpe_data_path)[0])
    empty_folder(cpe_unzip_path)
    decompress(cpe_zip_file, cpe_unzip_path)


def decompress(file, path):
    zf = zipfile.ZipFile(file, 'r')
    zf.extractall(path)
    for name in list(filter(lambda f: filter_file(f, r".*zip$|.*gz$"), zf.namelist())):
        if name.endswith('zip'):
            cpezf = zipfile.ZipFile(os.path.join(path, name))
            cpezf.extractall(path)
            cpezf.close()
        else:
            cpegz = gzip.GzipFile(os.path.join(path, name), 'rb')
            open(os.path.join(path, name.replace('.gz', "")), "wb").write(cpegz.read())
            cpegz.close()
    zf.close()


def compress_result():
    f = zipfile.ZipFile(os.path.join(setting.data_path, 'result.zip'), 'w', zipfile.ZIP_DEFLATED)
    for dirpath, dirnames, filenames in os.walk(setting.result_path):
        for filename in filenames:
            f.write(os.path.join(dirpath, filename), filename)
    f.close()


def empty_folder(path):
    if os.path.exists(path):
        for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
    else:
        os.mkdir(path)


def filter_file(file_name, file_type):
    if re.match(file_type, file_name):
        return True
    else:
        return False


def get_all_csv_file(file_path):
    all_file = []
    for path, dir_list, file_list in os.walk(file_path):
        for f in file_list:
            all_file.append(os.path.join(path, f))
    return list(filter(lambda x: filter_file(x, r".*csv$"), all_file))


def get_all_day_csv(file_path):
    all_file = []
    data_path = ""
    for path, dir_list, file_list in os.walk(file_path):
        for f in file_list:
            all_file.append(f)
        data_path = path
    file_name = list(filter(lambda x: filter_file(x, r"\d{8}.csv$"), all_file))
    files = list(map(lambda f_name: os.path.join(data_path, f_name), file_name))
    return files


if __name__ == '__main__':
    print(time.asctime(time.localtime(time.time())))
    decompress_cpe_data()
    print(time.asctime(time.localtime(time.time())))
