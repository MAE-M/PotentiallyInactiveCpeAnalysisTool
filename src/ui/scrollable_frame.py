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


import tkinter as tk
from tkinter import ttk
from tkinter import *


class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        win_width = self.winfo_screenwidth()
        win_height = self.winfo_screenheight()
        canvas = tk.Canvas(self, width=int(win_width), height=int(win_height))
        scrollbar_vertical = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar_horizontal = ttk.Scrollbar(self, orient="horizontal", command=canvas.xview)

        self.scrollable_frame = Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        # 鼠标滚轮事件
        def on_mousewheel(event):
            shift = (event.state & 0x1) != 0
            scroll = -1 if event.delta > 0 else 1
            if shift:
                canvas.xview_scroll(scroll, "units")
            else:
                canvas.yview_scroll(scroll, "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar_vertical.set, xscrollcommand=scrollbar_horizontal.set)

        # 顺序很重要！画布一定要最后pack，不能提前pack
        scrollbar_vertical.pack(side="right", fill="y")
        scrollbar_horizontal.pack(side="bottom", fill="x")
        canvas.pack(fill="both", expand=True)
