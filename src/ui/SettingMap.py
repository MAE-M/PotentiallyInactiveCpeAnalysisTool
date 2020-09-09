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


from tkinter import *
from src.setting import setting


class SettingMap:
    def __init__(self, inner_frame, screen_width_rate, screen_height_rate):
        self.setting_map = {
            'label_font': ("Roboto-Regular", int(setting.font_size_in_1920x1080_pixel * screen_width_rate)),
            'label_width': int(setting.label_in_1920x1080_pixel_width * screen_width_rate),
            'label_height': int(setting.label_in_1920x1080_pixel_height * screen_height_rate), 'label_anchor': E,
            'label_sticky': E, 'entry_width': int(setting.entry_in_1920x1080_pixel_width * screen_width_rate),
            'entry_height': int(setting.entry_in_1920x1080_pixel_height * screen_height_rate),
            'entry_font': ("Roboto-Regular", int(setting.font_size_in_1920x1080_pixel * screen_width_rate)),
            'button_sticky': N + S,
            'button_font': ("Roboto-Regular", int(setting.font_size_in_1920x1080_pixel * screen_width_rate)),
            'button_ipadx': int(setting.button_ipadx_in_1920x1080_pixel * screen_width_rate),
            'button_ipady': int(setting.button_ipady_in_1920x1080_pixel * screen_height_rate),
            'button_padx': int(setting.button_padx_in_1920x1080_pixel * screen_width_rate),
            'button_pady': int(setting.button_pady_in_1920x1080_pixel * screen_height_rate),
            'ratChoice_width': int(setting.ratChoice_in_1920x1080_pixel_width * screen_width_rate),
            'ratChoice_height': int(setting.ratChoice_in_1920x1080_pixel_height * screen_height_rate),
            'ratChoice_ipadx': int(setting.ratChoice_ipadx_in_1920x1080_pixel * screen_width_rate),
            'ratChoice_ipady': int(setting.ratChoice_ipady_in_1920x1080_pixel * screen_height_rate),
            'ratChoice_padx': int(setting.ratChoice_padx_in_1920x1080_pixel * screen_width_rate),
            'ratChoice_pady': int(setting.ratChoice_pady_in_1920x1080_pixel * screen_height_rate),
            'ratChoice_sticky': N + S,
            'log_text_width': int(setting.log_text_in_1920x1080_pixel_width * screen_width_rate),
            'log_text_height': int(setting.log_text_in_1920x1080_pixel_height * screen_height_rate)
        }

        # 下面这行，设置所有的下拉框的字体为label_font
        inner_frame.option_add('*TCombobox*Listbox.font', self.setting_map['label_font'])

    def get_setting_map(self):
        return self.setting_map
