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


from multiprocessing import Pool


class PotThread:
    def __init__(self, thread_nums):
        self.thread_nums = thread_nums

    def run_pot_threads(self, func, agrs):
        thread_pool = Pool(self.thread_nums)
        thread_pool.map(func, agrs)
        thread_pool.close()
        thread_pool.join()

    def run_async_thread(self, func, agrs):
        thread_pool = Pool(self.thread_nums)
        thread_pool.map_async(func, agrs)
        thread_pool.close()
