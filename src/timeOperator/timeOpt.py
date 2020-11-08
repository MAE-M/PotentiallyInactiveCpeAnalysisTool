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


from dateutil.relativedelta import relativedelta
from datetime import datetime
from datetime import timedelta
import time
weekSet = []

from src.logger_setting.my_logger import get_logger

logger = get_logger()


def get_week_day(date):
    week = datetime.strptime(date, "%Y%m%d").weekday()
    return week


def add_days(date, num):
    return (datetime.strptime(date, "%Y%m%d") + timedelta(days=num)).strftime("%Y%m%d")


def add_months(date, num):
    return (datetime.strptime(date, "%Y%m%d") + relativedelta(months=num)).strftime("%Y%m%d")


def get_week_set(first_day, last_day):
    week = get_week_day(first_day)
    next_day = add_days(first_day, 7 - int(week))
    if next_day > last_day:
        if first_day < last_day:
            weekSet.append(first_day)
        weekSet.append(last_day)
    else:
        weekSet.append(first_day)
        get_week_set(next_day, last_day)
    return weekSet


def change_week_set(week_set):
    if len(week_set) > 10:
        if (datetime.strptime(week_set[1], "%Y%m%d") - datetime.strptime(week_set[0], "%Y%m%d")).days >= \
                (datetime.strptime(week_set[10], "%Y%m%d") - datetime.strptime(week_set[9], "%Y%m%d")).days:
            del week_set[10]
        else:
            del week_set[0]
    return week_set


def is_in_time(date, first_day, last_day):
    if first_day <= date < last_day:
        return True
    else:
        return False


def get_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


if __name__ == '__main__':
    datetime_now = datetime.now()

    print(get_week_set("20200101", "20200201"))
    print((datetime.strptime(weekSet[4], "%Y%m%d") - datetime.strptime(weekSet[3], "%Y%m%d")).days >
          (datetime.strptime(weekSet[1], "%Y%m%d") - datetime.strptime(weekSet[0], "%Y%m%d")).days)
    print(is_in_time("20200513", "20200511", "20200518"))
    print(is_in_time("20200513", "20200514", "20200518"))
