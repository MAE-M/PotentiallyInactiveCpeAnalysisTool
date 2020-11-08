#  Copyright (c) Huawei Technologies Co., Ltd. 2019-2020. All rights reserved.
import logging
import os

from src.setting.setting import my_logger_path

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d-%(funcName)s - %(message)s "

log_parent_path = os.path.join(my_logger_path, 'log_dir')

log_path = os.path.join(log_parent_path, 'example_file_name.log')

if not os.path.exists(log_parent_path):
    os.mkdir(log_parent_path)

logging.basicConfig(filename=log_path,
                    filemode='a',
                    format=LOG_FORMAT,
                    level=logging.DEBUG)


def get_logger():
    return logging.getLogger()
