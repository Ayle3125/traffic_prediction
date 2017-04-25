# Copyright (c) 2016 PaddlePaddle Authors, Inc. All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from paddle.trainer.PyDataProvider2 import *
import sys
import numpy as np
TERM_NUM = 12
FORECASTING_NUM = 1
LABEL_VALUE_NUM = 4


def initHook(settings, file_list, **kwargs):
    """
    Init hook is invoked before process data. It will set obj.slots and store data meta.

    :param settings: global object. It will passed to process routine.
    :type obj: object
    :param file_list: the meta file object, which passed from trainer_config.py,but unused in this function.
    :param kwargs: unused other arguments.
    """
    del kwargs  #unused

    settings.pool_size = sys.maxint
    #Use a time seires of the past as feature.
    #Dense_vector's expression form is [float,float,...,float]

    settings.input_types =[integer_value_sequence(TERM_NUM) ,
                            integer_value_sequence(TERM_NUM) ,
                            integer_value_sequence(TERM_NUM) ,
                            integer_value_sequence(TERM_NUM) ,
                            integer_value_sequence(TERM_NUM) ,
                            integer_value(LABEL_VALUE_NUM),]
                            #[dense_vector(TERM_NUM)]
    #There are next FORECASTING_NUM fragments you need predict.
    #Every predicted condition at time point has four states.
    #for i in range(FORECASTING_NUM):
    #    settings.input_types.append(integer_value(LABEL_VALUE_NUM))


@provider(
    init_hook=initHook, cache=CacheType.CACHE_PASS_IN_MEM, should_shuffle=True)
def process(settings, file_name):
    with open(file_name) as f:
        #abandon fields name
        line = f.readline()
        time_sequence = line.rstrip('\r\n').split(",")[1:]
        time = []
        week = []

        for i in range(len(time_sequence)):
            tmp_time = int(time_sequence[i])
            time.append ( (tmp_time%10000)/100 ) #+ int(time_sequence[i][10:12])/60.0)
            #2016 0301 0000 - 2016 0420 0800
            month = (tmp_time%10000000)/1000000
            date = ((tmp_time%1000000)/10000)
            if month == 3:
                week.append (( date + 2 ) / 7 )
            else:
                week.append (( date + 5 ) / 7 )
        while 1:
            line1 = f.readline()
            line2 = f.readline()
            line3 = f.readline()
            if not line3:
                break
            _pre_road = map(int, line1.rstrip('\r\n').split(",")[1:])
            speeds = map(int, line2.rstrip('\r\n').split(",")[1:])
            _fol_road = map(int, line3.rstrip('\r\n').split(",")[1:])
            end_time = len(speeds)-1
            # Scanning and generating samples
            for i in range(TERM_NUM, end_time - FORECASTING_NUM):
                # For dense slot
                pre_road = map(int, _pre_road[i - TERM_NUM:i])
                pre_spd = map(int, speeds[i - TERM_NUM:i])
                fol_road = map(int, _fol_road[i - TERM_NUM:i])
                pre_time = map(int,time[i - TERM_NUM:i])
                pre_week = map(int,week[i - TERM_NUM:i])
                # Integer value need predicting, values start from 0, so every one minus 1.
                fol_spd = [int(j - 1) for j in speeds[i:i + FORECASTING_NUM]]

                # Predicting label is missing, abandon the sample.
                if -1 in fol_spd:
                    continue
                #yield  [pre_spd, pre_time, pre_week ]+fol_spd
                #yield  [pre_spd ]+fol_spd
                yield [pre_road, pre_spd, fol_road, pre_time, pre_week] + fol_spd


def predict_initHook(settings, file_list, **kwargs):
        del kwargs  #unused

        settings.pool_size = sys.maxint
        #Use a time seires of the past as feature.
        #Dense_vector's expression form is [float,float,...,float]

        settings.input_types =[integer_value_sequence(TERM_NUM) ,
                                integer_value_sequence(TERM_NUM) ,
                                integer_value_sequence(TERM_NUM) ,

                                integer_value_sequence(TERM_NUM) ,
                                integer_value_sequence(TERM_NUM) ,
                                integer_value(LABEL_VALUE_NUM),integer_value(LABEL_VALUE_NUM),integer_value(LABEL_VALUE_NUM),integer_value(LABEL_VALUE_NUM),
                                integer_value(LABEL_VALUE_NUM),integer_value(LABEL_VALUE_NUM),integer_value(LABEL_VALUE_NUM),integer_value(LABEL_VALUE_NUM),
                                integer_value(LABEL_VALUE_NUM),integer_value(LABEL_VALUE_NUM),integer_value(LABEL_VALUE_NUM),integer_value(LABEL_VALUE_NUM),
                                integer_value(LABEL_VALUE_NUM),integer_value(LABEL_VALUE_NUM),integer_value(LABEL_VALUE_NUM),integer_value(LABEL_VALUE_NUM),
                                integer_value(LABEL_VALUE_NUM),integer_value(LABEL_VALUE_NUM),integer_value(LABEL_VALUE_NUM),integer_value(LABEL_VALUE_NUM),
                                integer_value(LABEL_VALUE_NUM),integer_value(LABEL_VALUE_NUM),integer_value(LABEL_VALUE_NUM),integer_value(LABEL_VALUE_NUM),]


@provider(init_hook=predict_initHook, should_shuffle=False)
def process_predict(settings, file_name):
    with open(file_name) as f:
    #abandon fields name
        #f.next()
        line = f.readline()
        time_sequence = line.rstrip('\r\n').split(",")[1:]
        time = []
        week = []
        for i in range(len(time_sequence)):
            tmp_time = int(time_sequence[i])
            time.append ( (tmp_time%10000)/100 ) #+ int(time_sequence[i][10:12])/60.0)
            #2016 0301 0000 - 2016 0420 0800
            month = (tmp_time%10000000)/1000000
            date = ((tmp_time%1000000)/10000)
            if month == 3:
                week.append (( date + 2 ) / 7 )
            else:
                week.append (( date + 5 ) / 7 )
        while 1:
            line1 = f.readline()
            line2 = f.readline()
            line3 = f.readline()
            if not line3:
                break
            _pre_road = map(int, line1.rstrip('\r\n').split(",")[1:])
            speeds = map(int, line2.rstrip('\r\n').split(",")[1:])
            _fol_road = map(int, line3.rstrip('\r\n').split(",")[1:])
            end_time = len(speeds)-1
            # Scanning and generating samples
            pre_spd = map(int, speeds[end_time - TERM_NUM:end_time])
            pre_time = map(int, time[end_time - TERM_NUM:end_time])
            pre_week = map(int, week[end_time - TERM_NUM:end_time])
            yield [pre_road, pre_spd, fol_road, pre_time, pre_week]
            #yield [pre_spd, pre_time, pre_week]
