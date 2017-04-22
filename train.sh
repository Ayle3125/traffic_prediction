#!/bin/bash
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
set -e

cfg=trainer_config.py
log="train.log"
paddle train \
  --config=$cfg \
  --save_dir=./output \
  --trainer_count=4 \
  --log_period=1000 \
  --dot_period=10 \
  --num_passes=10 \
  --use_gpu=false\
  2>&1 | tee $log

paddle usage -l $log -e $? -n "test" >/dev/null 2>&1
#python -m paddle.utils.plotcurve -i $log > plot.png
#python plot_curve.py -i $log -o "ploterror.png" classification_error_evaluator
