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


class Cell:
    def __init__(self):
        self.enodeb_id = ''
        self.cell_id = ''
        self.poor_performace_nums = 0
        self.pot_inactive_nums = 0
        self.weak_converage_nums = 0
        self.high_interference_nums = 0
        self.high_load_nums = 0

    def add_poor_performance(self, value):
        self.poor_performace_nums = self.poor_performace_nums + value

    def add_pot_inactive(self, value):
        self.pot_inactive_nums = self.pot_inactive_nums + value

    def add_weak_converage(self, value):
        self.weak_converage_nums = self.weak_converage_nums + value

    def add_high_interference(self, value):
        self.high_interference_nums = self.high_interference_nums + value

    def add_high_load(self, value):
        self.high_load_nums = self.high_load_nums + value
