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


class OuterFrame:
    def __init__(self, main_frame, screen_width_rate, screen_height_rate):
        self.outer_frame = Frame(main_frame,
                                 width=int(setting.outer_frame_in_1920x1080_pixel_width * screen_width_rate),
                                 height=int(setting.outer_frame_in_1920x1080_pixel_height * screen_height_rate)
                                 )
        self.outer_frame.pack(fill="both",
                              expand=True,
                              padx=int(setting.outer_frame_padx_in_1920x1080_pixel * screen_width_rate),
                              pady=int(setting.outer_frame_pady_in_1920x1080_pixel * screen_height_rate),
                              )

    def get_outer_frame_object(self):
        return self.outer_frame
