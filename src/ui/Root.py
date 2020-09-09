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


class Root:
    def __init__(self):
        self.root = Tk()
        self.root.title("Potentially inactive CPE analysis Tool V1.0.3")

        # 获取屏幕的长和宽
        root_window_width = self.root.winfo_screenwidth()
        root_window_height = self.root.winfo_screenheight()

        self.screen_width_rate = root_window_width / setting.resolution_1920x1080_pixel_width
        self.screen_height_rate = root_window_height / setting.resolution_1920x1080_pixel_height

        # 除以2，代表把屏幕分两半，起始像素点在中间
        place_width = root_window_width // 2
        place_height = root_window_height // 2

        # 初始打开的时候，放置的位置置于屏幕中央,需要把起始像素点向上和向左移动一半
        self.root.geometry("{}x{}+{}+{}".format(place_width, place_height, place_width // 2, place_height // 2))

    def get_root_object(self):
        return self.root

    def get_screen_width_rate(self):
        return self.screen_width_rate

    def get_screen_height_rate(self):
        return self.screen_height_rate
