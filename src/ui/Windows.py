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


from src.ui.inner_frame import InnerFrame
from src.ui.main_frame import MainFrame
from src.ui.outer_frame import OuterFrame
from src.ui.root import Root


class Windows:
    def __init__(self):
        # root窗口，最外层的整个框
        self.root = Root()

        self.screen_width_rate = self.root.get_screen_width_rate()
        self.screen_height_rate = self.root.get_screen_height_rate()

        # 创建包含滚动条的main_frame，在root里面
        main_frame = MainFrame(self.root.get_root_object()).get_main_frame_object()

        # 创建一个outer_frame，在main_frame里面
        outer_frame = OuterFrame(main_frame, self.screen_width_rate, self.screen_height_rate).get_outer_frame_object()

        # 创建一个inner_frame, 在outer_frame里面
        self.inner_frame = InnerFrame(outer_frame, self.screen_width_rate,
                                      self.screen_height_rate).get_inner_frame_object()

    def get_root_Tk(self):
        return self.root.get_root_object()

    def get_inner_frame(self):
        return self.inner_frame

    def get_screen_width_rate(self):
        return self.screen_width_rate

    def get_screen_height_rate(self):
        return self.screen_height_rate

