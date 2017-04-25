import os

for i in range(0,20):
    print "!!!!!!!!!!!!!!!!!!!!!!!!!!Predicting number "+str(i+1)+'\n'
    os.system('sh predict.sh')
    os.system('cd data && python preprocess.py && cd ..')
