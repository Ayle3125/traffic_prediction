import sys
import csv
import numpy as np
#  import packages
TERM_NUM=24
FORECASTING_NUM=24
def process_gap():
    sumNO=0;
    with open("speeds.csv",'r') as f_in:
        with open("new_speed.csv",'w') as f_out:
            f_spd = csv.reader(f_in)
            headers = next(f_spd)
            csv_out = csv.writer(f_out)
            csv_out.writerow(headers)
            for speeds in f_spd:
                end_time = len(speeds)
                for i in range(1,end_time-1):
                    if int(speeds[i]) == 0 :
                        #print "no"
                        sumNO=sumNO+1
                    #elif abs(int(speeds[i])-int(speeds[i+1]))>2:
                    #    print speeds[i],speeds[i+1]
                        #print abs(int(speeds[i])-int(speeds[i+1]))
                #csv_out.writerow(speeds)
    print sumNO

def process_graph():
    sum_start = {}
    sum_end = {}
    with open("graph.csv") as f:
        line = f.readline()
        f.next()
        for row_num, line in enumerate(f):
            point = map(int, line.rstrip('\r\n').split(","))
            start = point[0]
            end = point[1]
            if sum_start.has_key(start):
                sum_start[start].append(end)
            else:
                sum_start[start] = [end]
            if sum_end.has_key(end):
                sum_end[end].append(start)
            else:
                sum_end[end] = [start]
    for key,value in sum_start.items():
        print key,value,sum_end.get(key, 0)

def process(infile_name, outfile_name):
    sum_start = {}
    sum_end = {}
    with open("graph.csv") as f:
        line = f.readline()
        f.next()
        for row_num, line in enumerate(f):
            point = map(int, line.rstrip('\r\n').split(","))
            start = point[0]
            end = point[1]
            if sum_start.has_key(start):
                sum_start[start].append(end)
            else:
                sum_start[start] = [end]
            if sum_end.has_key(end):
                sum_end[end].append(start)
            else:
                sum_end[end] = [start]

    sum_speed = {}
    with open(infile_name) as f:
        #abandon fields name
        line = f.readline()
        time_sequence = line.rstrip('\r\n').split(",")[1:]
        time = []
        week = []
        TIMELEN = len(time_sequence)
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

        for row_num, line in enumerate(f):
            _tmp_speeds = map(int, line.rstrip('\r\n').split(","))
            road_id =  _tmp_speeds[0]
            sum_speed[ road_id ] = _tmp_speeds[1:]
            # Get the max index.
            _pre_road = sum_end.get(road_id,0)
            if _pre_road == 0:
                sum_end[road_id]=[road_id]
            _fol_road = sum_start.get(road_id,0)
            if _fol_road == 0:
                sum_start[road_id]=[road_id]
    pre_speeds=sum_speed;
    fol_speeds=sum_speed;
    for road_id in sum_speed:
        _pre_speed = pre_speeds.get(road_id)
        _fol_speed = fol_speeds.get(road_id)
        for i in range(TIMELEN):
            _sum_num=0
            _sum=0
            for end_id in sum_end[road_id]:
                speeds = sum_speed[end_id]
                if speeds[i] != 0:
                    _sum_num=_sum_num+1
                    _sum = _sum+speeds[i]
            if _sum_num == 0:
                _pre_speed[i]=0
            else:
                _pre_speed[i] = _sum/_sum_num
            _sum_num=0
            _sum=0
            for start_id in sum_start[road_id]:
                speeds = sum_speed[start_id]
                if speeds[i] != 0:
                    _sum_num=_sum_num+1
                    _sum = _sum+speeds[i]
            if _sum_num == 0:
                _fol_speed[i]=0
            else:
                _fol_speed[i] = _sum/_sum_num
    with open(infile_name,'r') as f_in:
        with open(outfile_name,'w') as f_out:
            f_spd = csv.reader(f_in)
            headers = next(f_spd)
            csv_out = csv.writer(f_out)
            csv_out.writerow(headers)
            road_id =  _tmp_speeds[0]
            for speeds in f_spd:
                road_id =  int(speeds[0])
                _pre_speed = pre_speeds.get(road_id,0)
                _fol_speed = fol_speeds.get(road_id,0)
                csv_out.writerow([road_id]+_pre_speed)
                csv_out.writerow(speeds)
                csv_out.writerow([road_id]+_fol_speed)

def test(file_name):
  with open(file_name) as f:
    line = f.readline()
    time_sequence = line.rstrip('\r\n').split(",")[1:]
    time = []
    week = []
    TIMELEN = len(time_sequence)
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
#        for row_num, line in enumerate(f):
    _tmp_sum=0
    while 1:
        print _tmp_sum
        _tmp_sum=_tmp_sum+1
        line1 = f.readline()
        line2 = f.readline()
        line3 = f.readline()
        if not line3:
            break
        _pre_road = map(int, line1.rstrip('\r\n').split(",")[1:])
        _tmp_speeds = map(int, line2.rstrip('\r\n').split(","))
        _fol_road = map(int, line3.rstrip('\r\n').split(",")[1:])
        road_id =  _tmp_speeds[0]
        speeds = _tmp_speeds[1:]
        end_time = len(speeds)
        # Scanning and generating samples
        for i in range(TERM_NUM, end_time - FORECASTING_NUM):
            # For dense slot
            pre_road = map(int, _pre_road[i - TERM_NUM:i])
            fol_road = map(int, _fol_road[i - TERM_NUM:i])
            pre_spd = map(int, speeds[i - TERM_NUM:i])
            pre_time = map(int,time[i - TERM_NUM:i])
            pre_week = map(int,week[i - TERM_NUM:i])
            # Integer value need predicting, values start from 0, so every one minus 1.
            fol_spd = [int(j - 1) for j in speeds[i:i + FORECASTING_NUM]]

            # Predicting label is missing, abandon the sample.
            if -1 in fol_spd:
                continue
            #yield  [pre_spd, pre_time, pre_week ]+fol_spd
            #print [pre_road,pre_spd,fol_road ]+fol_spd

#process_gap()
#process_graph()
process(infile_name="speeds.csv",outfile_name="new_speed.csv")
#test("new_speed.csv")
