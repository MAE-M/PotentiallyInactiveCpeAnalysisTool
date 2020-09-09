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
import time
from src.potThread import uiThread
from src.postEva import post_evaluate


class Layout:
    def __init__(self, inner_frame, setting_map, input_path, thread_flag):
        self.input_path = input_path
        self.THREAD_FLAG = thread_flag

        # 从这里开始，所有grid()方法里面的row和column，是表格参数，代表第几行第几列
        # 如row=0,column=0代表第0行第0列；
        # 这里的设置是每行有三列，所以row是递增的，而column是0 1 2的循环。

        # RAT
        Label(inner_frame,
              text="RAT:",
              font=setting_map['label_font'],
              anchor=setting_map['label_anchor'],
              ).grid(row=0,
                     column=0,
                     ipadx=setting_map['label_width'],
                     ipady=setting_map['label_height'],
                     sticky=setting_map['label_sticky']
                     )

        self.ratChoice = ttk.Combobox(inner_frame,
                                      value=['LTE'],
                                      state='readonly',
                                      width=setting_map['ratChoice_width'],
                                      height=setting_map['ratChoice_height'],
                                      font=setting_map['label_font'],
                                      )

        self.ratChoice.current(0)
        self.ratChoice.grid(row=0,
                            column=1,
                            ipadx=setting_map['ratChoice_ipadx'],
                            ipady=setting_map['ratChoice_ipady'],
                            padx=setting_map['ratChoice_padx'],
                            pady=setting_map['ratChoice_pady'],
                            sticky=setting_map['ratChoice_sticky']
                            )

        Button(inner_frame,
               text='Export template',
               command=self.export_template,
               font=setting_map['button_font']
               ).grid(row=0,
                      column=2,
                      ipadx=setting_map['button_ipadx'],
                      ipady=setting_map['button_ipady'],
                      padx=setting_map['button_padx'],
                      pady=setting_map['button_pady'],
                      sticky=setting_map['button_sticky']
                      )

        # Evaluation Threshold
        Label(inner_frame,
              text="Evaluation Threshold:",
              font=setting_map['label_font'],
              anchor=setting_map['label_anchor'],
              ).grid(row=1,
                     column=0,
                     ipadx=setting_map['label_width'],
                     ipady=setting_map['label_height'],
                     sticky=setting_map['label_sticky']
                     )

        self.thre_entry = Entry(inner_frame,
                                font=setting_map['entry_font'],
                                state=DISABLED,
                                )
        self.thre_entry.grid(row=1,
                             column=1,
                             ipadx=setting_map['entry_width'],
                             ipady=setting_map['entry_height'],
                             )

        Button(inner_frame,
               text='Import file',
               command=self.import_thre_data,
               font=setting_map['button_font'],
               ).grid(row=1,
                      column=2,
                      ipadx=setting_map['button_ipadx'],
                      ipady=setting_map['button_ipady'],
                      padx=setting_map['button_padx'],
                      pady=setting_map['button_pady'],
                      sticky=setting_map['button_sticky']
                      )

        # CPE Log Data
        Label(inner_frame,
              text="CPE Log Data:",
              font=setting_map['label_font'],
              anchor=setting_map['label_anchor'],
              ).grid(row=2,
                     column=0,
                     ipadx=setting_map['label_width'],
                     ipady=setting_map['label_height'],
                     sticky=setting_map['label_sticky']
                     )

        self.cpe_entry = Entry(inner_frame,
                               font=setting_map['entry_font'],
                               state=DISABLED,
                               )
        self.cpe_entry.grid(row=2,
                            column=1,
                            ipadx=setting_map['entry_width'],
                            ipady=setting_map['entry_height'],
                            )

        Button(inner_frame,
               text='Import file',
               command=self.import_cpe_data,
               font=setting_map['button_font'],
               ).grid(row=2,
                      column=2,
                      ipadx=setting_map['button_ipadx'],
                      ipady=setting_map['button_ipady'],
                      padx=setting_map['button_padx'],
                      pady=setting_map['button_pady'],
                      sticky=setting_map['button_sticky']
                      )

        # WTTx Suite Data
        Label(inner_frame,
              text="WTTx Suite Data:",
              font=setting_map['label_font'],
              anchor=setting_map['label_anchor'],
              ).grid(row=3,
                     column=0,
                     ipadx=setting_map['label_width'],
                     ipady=setting_map['label_height'],
                     sticky=setting_map['label_sticky']
                     )

        # Experience Insight Data
        Label(inner_frame,
              text="Experience Insight Data:",
              font=setting_map['label_font'],
              anchor=setting_map['label_anchor'],
              ).grid(row=4,
                     column=0,
                     ipadx=setting_map['label_width'],
                     ipady=setting_map['label_height'],
                     sticky=setting_map['label_sticky']
                     )

        self.exper_entry = Entry(inner_frame,
                                 font=setting_map['entry_font'],
                                 state=DISABLED,
                                 )
        self.exper_entry.grid(row=4,
                              column=1,
                              ipadx=setting_map['entry_width'],
                              ipady=setting_map['entry_height'],
                              )

        Button(inner_frame,
               text='Import file',
               command=self.import_exper_data,
               font=setting_map['button_font'],
               ).grid(row=4,
                      column=2,
                      ipadx=setting_map['button_ipadx'],
                      ipady=setting_map['button_ipady'],
                      padx=setting_map['button_padx'],
                      pady=setting_map['button_pady'],
                      sticky=setting_map['button_sticky']
                      )

        # Capacity Insight Data
        Label(inner_frame,
              text="Capacity Insight Data:",
              font=setting_map['label_font'],
              anchor=setting_map['label_anchor'],
              ).grid(row=5,
                     column=0,
                     ipadx=setting_map['label_width'],
                     ipady=setting_map['label_height'],
                     sticky=setting_map['label_sticky']
                     )

        self.capa_entry = Entry(inner_frame,
                                font=setting_map['entry_font'],
                                state=DISABLED,
                                )
        self.capa_entry.grid(row=5,
                             column=1,
                             ipadx=setting_map['entry_width'],
                             ipady=setting_map['entry_height'],
                             )

        Button(inner_frame,
               text='Import file',
               command=self.import_capa_data,
               font=setting_map['button_font'],
               ).grid(row=5,
                      column=2,
                      ipadx=setting_map['button_ipadx'],
                      ipady=setting_map['button_ipady'],
                      padx=setting_map['button_padx'],
                      pady=setting_map['button_pady'],
                      sticky=setting_map['button_sticky']
                      )

        # Button---"reset", "Analyze", "Export"
        Button(inner_frame,
               text='Reset',
               command=self.reset,
               font=setting_map['button_font'],
               ).grid(row=6,
                      column=0,
                      ipadx=setting_map['button_ipadx'],
                      ipady=setting_map['button_ipady'],
                      padx=setting_map['button_padx'],
                      pady=setting_map['button_pady'],
                      sticky=""
                      )

        self.analysis_button = Button(inner_frame,
                                      text='Analyze',
                                      command=self.run,
                                      font=setting_map['button_font'],
                                      )
        self.analysis_button.grid(row=6,
                                  column=1,
                                  ipadx=setting_map['button_ipadx'],
                                  ipady=setting_map['button_ipady'],
                                  padx=setting_map['button_padx'],
                                  pady=setting_map['button_pady'],
                                  sticky=""
                                  )

        self.export_button = Button(inner_frame,
                                    text='Export',
                                    command=self.export_result,
                                    font=setting_map['button_font'],
                                    )
        self.export_button.grid(row=6,
                                column=2,
                                ipadx=setting_map['button_ipadx'],
                                ipady=setting_map['button_ipady'],
                                padx=setting_map['button_padx'],
                                pady=setting_map['button_pady'],
                                sticky=""
                                )

        # 用来显示日志的文本框
        self.log_text = tk.scrolledtext.ScrolledText(inner_frame,
                                                     state='disabled',
                                                     width=setting_map['log_text_width'],
                                                     height=setting_map['log_text_height'],
                                                     wrap=tk.WORD
                                                     )

        self.log_text.insert(END, "Potentially inactive CPE analysis. \n")
        self.log_text.grid(row=7,
                           rowspan=3,
                           column=0,
                           columnspan=3,
                           )

    def open_file(self, file_type=('zip', '*.zip')):
        filename = tk.filedialog.askopenfilename(title='open zip file', filetypes=[file_type],
                                                 initialdir=self.input_path)
        return filename

    @staticmethod
    def open_dir():
        dest_dir = tk.filedialog.askdirectory(title='select dir to save')
        return dest_dir

    @staticmethod
    def copy_file(source, dest):
        try:
            if dest:
                copy(source, dest)
                return True
        except IOError:
            tk.messagebox.showerror("ERROR", message='Operate file failed!')
            raise Exception('Operate file failed!')

    def export_template(self):
        dest = self.open_dir()
        success = self.copy_file(setting.template_file, dest)
        if success:
            tk.messagebox.showinfo("Success", message="Finish Export data!")
        else:
            tk.messagebox.showinfo("ERROR", message="Failed Export data!")

    def export_result(self):
        if os.path.exists(os.path.join(setting.data_path, 'result.zip')):
            dest = self.open_dir()
            success = self.copy_file(os.path.join(setting.data_path, 'result.zip'), dest)
            if success:
                tk.messagebox.showinfo("Success", message="Finish Export data!")
            else:
                tk.messagebox.showinfo("ERROR", message="Failed Export data!")
        else:
            self.show_log(timeOpt.get_time() + ": No result to export.")
            tk.messagebox.showerror("ERROR", message='No result to export!')

    def import_with_suite_thread(self):
        self.show_log(timeOpt.get_time() + ": import Experience data.")
        self.copy_data(self.exper_entry.get(), setting.exper_data_path)
        self.show_log(timeOpt.get_time() + ": import Capacity data.")
        self.copy_data(self.capa_entry.get(), setting.capa_data_path)
        self.show_log(timeOpt.get_time() + ": import CPE data.")
        self.copy_data(self.cpe_entry.get(), setting.cpe_data_path)

    def import_cpe_thread(self):
        self.show_log(timeOpt.get_time() + ": import CPE data.")
        self.copy_data(self.cpe_entry.get(), setting.cpe_data_path)

    def import_data(self, entry, file_type):
        source = self.open_file(file_type)
        if source is not '':
            self.input_path = source
            entry.delete(0, END)
            entry['state'] = NORMAL
            entry.insert('insert', source)

    def copy_data(self, source, path):
        compress.empty_folder(path)
        self.copy_file(source, path)

    def import_pm_data(self):
        self.import_data(self.pm_entry, ('csv', '*.csv'))

    def import_en_data(self):
        self.import_data(self.engineer_entry, ('csv', '*.csv'))

    def import_cm_data(self):
        self.import_data(self.cm_entry, ('zip', '*.zip'))

    def import_package_data(self):
        self.import_data(self.package_entry, ('csv', '*.csv'))

    def import_thre_data(self):
        self.import_data(self.thre_entry, ('csv', '*.csv'))

    def import_cpe_data(self):
        self.import_data(self.cpe_entry, ('zip', '*.zip'))

    def import_exper_data(self):
        self.import_data(self.exper_entry, ('csv', '*.csv'))

    def import_capa_data(self):
        self.import_data(self.capa_entry, ('csv', '*.csv'))

    def show_log(self, log_info):
        self.log_text['state'] = 'normal'
        self.log_text.insert(END, log_info + "\n")
        self.log_text['state'] = 'disabled'

    def reset(self):
        self.ratChoice.current(0)
        self.pm_entry.delete(0, END)
        self.engineer_entry.delete(0, END)
        self.cm_entry.delete(0, END)
        self.package_entry.delete(0, END)
        self.thre_entry.delete(0, END)
        self.cpe_entry.delete(0, END)
        self.exper_entry.delete(0, END)
        self.capa_entry.delete(0, END)
        self.show_log(timeOpt.get_time() + ": reset configure.")

    def check(self):
        if self.cpe_entry.get() and self.thre_entry.get() and self.exper_entry.get() and self.capa_entry.get():
            return 2
        elif self.cpe_entry.get()  and not self.thre_entry.get() \
                and not self.exper_entry.get() and not self.capa_entry.get():
            return 3
        else:
            return 0

    def run(self):
        self.THREAD_FLAG = True
        status = self.check()
        if status == 0:
            self.show_log(timeOpt.get_time() + ": Please import the specified data.")
            tk.messagebox.showwarning("WARNING",
                                      message="Please import the specified data!\nExperience data "
                                              "& Performance Evaluation Threshold & Capacity data & CPE data\nor\nCPE "
                                              "data")
        else:
            self.analysis_button['state'] = DISABLED
            self.export_button['state'] = DISABLED
            try:
                uiThread.UiThread(self.cpe_analysis, [status])
            except Exception as e:
                self.show_log(timeOpt.get_time() + ": Analysis failed!\n" + str(e))
                tk.messagebox.showerror("ERROR", message='Analysis failed!\n' + str(e))

    def xg_pre(self):
        self.show_log(timeOpt.get_time() + ": Begin analyzing.")
        compress.decompress_cpe_data()
        self.show_log(timeOpt.get_time() + ": Finish unzip cpe file.")
        extract_data.extract_data()
        self.show_log(timeOpt.get_time() + ": Finish extract cpe data.")
        day_extract.day_extract()
        self.show_log(timeOpt.get_time() + ": Finish build cpe day data.")
        feature_build.run()
        self.show_log(timeOpt.get_time() + ": Finish build cpe features data.")
        PotXGBoost.get_xgboost_predict_result()
        self.show_log(timeOpt.get_time() + ": Finish predict Potentially inactive CPE.")

    def cpe_analysis(self, status):
        print(status)
        try:
            uiThread.UiThread(self.check_health)
            if status[0] == 3:
                self.import_cpe_thread()
                self.xg_pre()
            elif status[0] == 2:
                compress.empty_folder(setting.post_eva_path)
                self.import_with_suite_thread()
                self.xg_pre()
                post_evaluate.main(True)
            compress.compress_result()
            self.analysis_button['state'] = NORMAL
            self.export_button['state'] = NORMAL
            self.show_log(timeOpt.get_time() + ": click Export button to export the data.")
            self.THREAD_FLAG = False
        except Exception as e:
            self.THREAD_FLAG = False
            self.show_log(timeOpt.get_time() + ": Analysis failed!\n" + str(e))
            tk.messagebox.showerror("ERROR", message='Analysis failed!\n' + str(e))
            self.analysis_button['state'] = NORMAL
            self.export_button['state'] = NORMAL

    def check_health(self):
        while self.THREAD_FLAG:
            time.sleep(60 * 5)
            self.show_log(timeOpt.get_time() + ": The tool is running ....")
        self.show_log(timeOpt.get_time() + ": The tool is stopped")
