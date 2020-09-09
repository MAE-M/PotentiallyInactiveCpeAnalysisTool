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


class InnerFrame:
    def __init__(self, outer_frame, screen_width_rate, screen_height_rate):
        self.inner_frame = Frame(outer_frame,
                                 padx=int(setting.inner_frame_padx_in_1920x1080_pixel * screen_width_rate),
                                 pady=int(setting.inner_frame_pady_in_1920x1080_pixel * screen_height_rate),
                                 width=int(setting.inner_frame_in_1920x1080_pixel_width * screen_width_rate),
                                 height=int(setting.inner_frame_in_1920x1080_pixel_height * screen_height_rate),
                                 )

        self.inner_frame.grid(row=0,
                              column=0,
                              in_=outer_frame,
                              )

    def get_inner_frame_object(self):
        return self.inner_frame
