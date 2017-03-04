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
emb_size = 24
with_rnn =True #False
hidden_dim = 4 #TODO
initial_std = 0.0001
param_attr = ParamAttr(initial_std=initial_std)
batch_size = 128 if not is_predict else 1
settings(
    batch_size=batch_size,
    learning_rate=5e-2, #TODO
    regularization=L2Regularization(batch_size * 1e-5),
    learning_method=RMSPropOptimizer()) #TODO ())AdaGradOptimizer
################################### Algorithm Configuration ########################################

output_label = []
forinput = []
pre_speed = data_layer(name='pre_speed', size=TERM_NUM)
#fol_speed = data_layer(name='fol_speed', size=TERM_NUM)
forinput.append(pre_speed)
for i in xrange(FORECASTING_NUM):
    # Each task share same weight.
    '''
    link_param = ParamAttr(
        name='_link_vec.w', initial_max=1.0, initial_min=-1.0)
    link_vec = fc_layer(input=link_encode, size=emb_size, param_attr=link_param)
    score = fc_layer(input=link_vec, size=4, act=SoftmaxActivation())
    '''
    link_param = ParamAttr(
        name='_par.w', initial_max=1.0, initial_min=-1.0)
    spd_vec = embedding_layer(input=pre_speed, size=emb_size, param_attr=ParameterAttribute(initial_std=0.))
    #cnt = concat_layer(input=[pre_speed,fol_speed])
    #emb_time = embedding_layer(input=time, size=emb_size, param_attr=ParamAttr(initial_mean=0.0,initial_std=0.01))
    hidden1 = mixed_layer(
        size=hidden_dim,
        #act=STanhActivation(),
        #act=SigmoidActivation(),
        bias_attr=True,
        input=[
            #full_matrix_projection(emb_time),
            #table_projection(pre_speed, param_attr=ParamAttr(initial_mean=0.0,initial_std=0.0001))
            #full_matrix_projection(input=pre_speed, size=emb_size,)
            full_matrix_projection(spd_vec),
            #full_matrix_projection(spd_vec)
            ])


    if with_rnn:
        rnn1 = recurrent_layer(
            input=hidden1,
            act=SigmoidActivation(),
            bias_attr=True,
            param_attr=param_attr, )

    hidden2 = mixed_layer(
        size=hidden_dim,
        #act=STanhActivation(),
        act=SigmoidActivation(),
        bias_attr=True,
        input=[full_matrix_projection(hidden1)] +
            ([full_matrix_projection(
            rnn1, param_attr=ParamAttr(initial_mean=0.0,initial_std=0.0001))] if with_rnn else []), )

    if with_rnn:
        rnn2 = recurrent_layer(
            input=hidden2,
            reverse=True,
            act=SigmoidActivation(),
            bias_attr=True,
            param_attr=ParamAttr(initial_mean=0.0,initial_std=0.0001), )
    pool_input = mixed_layer(
        size=hidden_dim,
        #act=STanhActivation(),
        act=SigmoidActivation(),
        bias_attr=True,
        input=[full_matrix_projection(hidden2)] +
            ([full_matrix_projection(
            rnn2, param_attr=ParamAttr(initial_mean=0.0,initial_std=0.0001))] if with_rnn else []), )

    pool = pooling_layer(input=pool_input,pooling_type=AvgPooling())

    score = fc_layer(
        size=4,
        act=SoftmaxActivation(),
        bias_attr=False,
        input=pool,)

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
