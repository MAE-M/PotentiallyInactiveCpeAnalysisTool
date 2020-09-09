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


from src.ui.ScrollableFrame import ScrollableFrame


class MainFrame:
    def __init__(self, root):
        # 滚动条
        # 创建逻辑：把main_frame放到canvas中
        main_frame_scrollable_frame = ScrollableFrame(root)
        main_frame_scrollable_frame.pack(fill='y', expand=1)
        self.main_frame = main_frame_scrollable_frame.scrollable_frame

    def get_main_frame_object(self):
        return self.main_frame
