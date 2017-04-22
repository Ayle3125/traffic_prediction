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
from paddle.trainer_config_helpers import *
import numpy as np
################################### DATA Configuration #############################################
is_predict = get_config_arg('is_predict', bool, False)
trn = './data/train.list' if not is_predict else None
tst = './data/test.list' if not is_predict else './data/pred.list'
process = 'process' if not is_predict else 'process_predict'
define_py_data_sources2(
    train_list=trn, test_list=tst, module="dataprovider", obj=process)
################################### Parameter Configuaration #######################################
TERM_NUM = 24
FORECASTING_NUM = 24
emb_size = 4
lstm_dim= 64
with_rnn =False #False
hidden_dim = 24 #TODO
initial_std = 0.0001
param_attr = ParamAttr(initial_std=initial_std)
batch_size = 128 if not is_predict else 1
settings(
    batch_size=batch_size,
    learning_rate=1e-2, #TODO
    regularization=L2Regularization(batch_size * 8e-4),
    learning_method=AdamOptimizer()) #RMSPropOptimizer()) #TODO ())AdaGradOptimizer
################################### Algorithm Configuration ########################################
output_label = []
forinput = []
pre_road = data_layer(name='pre_road', size=TERM_NUM)
pre_speed = data_layer(name='pre_speed', size=TERM_NUM)
fol_road = data_layer(name='fol_road', size=TERM_NUM)
#time = data_layer(name='time', size=TERM_NUM)
#week = data_layer(name='week', size=TERM_NUM)
forinput = [pre_road, pre_speed, fol_road] #, time, week
for i in xrange(FORECASTING_NUM):
    # Each task share same weight.
    '''
    link_param = ParamAttr(
        name=/ '_link_vec.w', initial_max=1.0, initial_min=-1.0)
    link_vec = fc_layer(input=link_encode, size=emb_size, param_attr=link_param)
    score = fc_layer(input=link_vec, size=4, act=SoftmaxActivation())
    '''
    link_param = ParamAttr(
        name='_par.w', initial_max=1.0, initial_min=-1.0)
    spd_vec = embedding_layer(input=pre_speed, size=emb_size, param_attr=ParameterAttribute(initial_std=0.))
    pre_road_vec = embedding_layer(input=pre_road, size=emb_size, param_attr=ParameterAttribute(initial_std=0.))
    fol_road_vec = embedding_layer(input=fol_road, size=emb_size, param_attr=ParameterAttribute(initial_std=0.))
    #time_vec = embedding_layer(input=time, size=emb_size, param_attr=ParameterAttribute(initial_std=0.))
    #week_vec = embedding_layer(input=week, size=emb_size, param_attr=ParameterAttribute(initial_std=0.))
    #cnt = concat_layer(input=[pre_speed,fol_speed])
    #emb_time = embedding_layer(input=time, size=emb_size, param_attr=ParamAttr(initial_mean=0.0,initial_std=0.01))
    hidden1 = mixed_layer(
        size=hidden_dim,
        #act=STanhActivation(),
        #act=SigmoidActivation(),
        bias_attr=True,
        input=[
            full_matrix_projection(pre_road_vec),
            full_matrix_projection(spd_vec),
            full_matrix_projection(fol_road_vec),
            #full_matrix_projection(time_vec),
            #full_matrix_projection(week_vec),
            #full_matrix_projection(spd_vec)
            ])

    bi_lstm = bidirectional_lstm(input=hidden1, size=lstm_dim)
    dropout = dropout_layer(input=bi_lstm, dropout_rate=0.5)
    #pool = pooling_layer(input=dropout,pooling_type=AvgPooling())
    score = fc_layer(
        size=4,
        act=SoftmaxActivation(),
        bias_attr=False,
        input=dropout,)

    if is_predict:
        maxid = maxid_layer(score)
        output_label.append(maxid)
    else:
        # Multi-task training.
        label = data_layer(name='label_%dmin' % ((i + 1) * 5), size=4)
        forinput.append(label)
        cls = classification_cost(
            input=score, label=label)
            #input=score, name="cost_%dmin" % ((i + 1) * 5), label=label)
        output_label.append(cls)
'''
        if i == 0:
            output_label = cls
        else:
            output_label = addto_layer(input=[cls,output_label], name = "sum_%d" %i, act=ReluActivation(), bias_attr=False)
'''
inputs(forinput)
outputs(output_label)
