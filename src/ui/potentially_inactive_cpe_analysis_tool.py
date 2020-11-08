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
from collections import Counter
import re
import math
from src.cpePaser import month_extract
from src.cpePaser import week_extract
import xgboost as xgb
import json
import time
import multiprocessing
import numpy as np
from src.potThread import potThread
import random
import csv
from src.postEva.threshold_param_paser import threshold_param_paser
from src.postEva import util
from itertools import combinations
from src.postEva.exper_paser import exper_paser
from src.postEva.capacity_paser import capacity_paser
from src.postEva.capacity_paser import cell
import pandas as pd
from multiprocessing import Pool
import threading
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from tkinter import scrolledtext
from shutil import copy
from src.setting import setting
import os
from src.cpePaser import extract_data
from src.cpePaser import day_extract
from src.cpePaser import feature_build
from src.compress import compress
from src.timeOperator import timeOpt
from src.cpePaser import PotXGBoost
from src.potThread import uiThread
import sys
from src.postEva import post_evaluate
from src.ui.layout import Layout
from src.ui.setting_map import SettingMap
from src.ui.windows import Windows
from src.ui import inner_frame
from src.ui import main_frame
from src.ui import outer_frame
from src.ui import root
from src.ui import scrollable_frame
from src.logger_setting import my_logger

sys.setrecursionlimit(100)


class Application:
    def __init__(self):
        windows = Windows()
        screen_width_rate = windows.get_screen_width_rate()
        screen_height_rate = windows.get_screen_height_rate()

        # 获取inner_frame,以后所有Label,Button,Entry等元素都放在这个inner_frame里面
        inner_frame = windows.get_inner_frame()

        setting_map = SettingMap(inner_frame, screen_width_rate, screen_height_rate).get_setting_map()

        Layout(inner_frame, setting_map, input_path=setting.app_path, thread_flag=True)

        multiprocessing.freeze_support()

        windows.get_root_Tk().mainloop()


if __name__ == '__main__':
    app = Application()
