import sys
import csv
import numpy as np
#  import packages

def process_gap():
    with open("speeds.csv",'r') as f_in:
        with open("new_speed.csv",'w') as f_out:
            f_spd = csv.reader(f_in)
            headers = next(f_spd)
            csv_out = csv.writer(f_out)
            csv_out.writerow(headers)
            for speeds in f_spd:
                end_time = len(speeds)
                for i in range(1,end_time-1):
                    if int(speeds[i]) == 0:
                        #print "no"
                        speeds[i] = 1
                    elif abs(int(speeds[i])-int(speeds[i+1]))>2:
                        print speeds[i],speeds[i+1]
                        #print abs(int(speeds[i])-int(speeds[i+1]))
                csv_out.writerow(speeds)


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
                sum_start[start] = sum_start[start]+1
            else:
                sum_start[start] = 1
            if sum_end.has_key(end):
                sum_end[end] = sum_end[end]+1
            else:
                sum_end[end] = 1
    for key,value in sum_start.items():
        print key,value,sum_end.get(key, 0)

process_gap()
#process_graph()


'''
    for row_num, line in enumerate(f):
        speeds = map(int, line.rstrip('\r\n').split(",")[1:])
        end_time = len(speeds)
        # Scanning and generating samples
        for i in range(TERM_NUM, end_time - FORECASTING_NUM):
            fol_spd = [j - 1 for j in speeds[i:i + FORECASTING_NUM]]
            for r in range(len(fol_spd)):
                if fol_spd[r]== -1:
                    if r==0:
                        if fol_spd[r+1]!=-1 :
                            fol_spd[r]=fol_spd[r+1]
                        if fol_spd[r+2]!=-1:
                            fol_spd[r]=fol_spd[r+2]
                        else:
                            continue
                    elif r==len(fol_spd)-1:
                        if fol_spd[r-1]!=-1 :
                            fol_spd[r]=fol_spd[r-1]
                        if fol_spd[r-2]!=-1:
                            fol_spd[r]=fol_spd[r-2]
                        else:
                            continue
                    else :
                        if fol_spd[r-1]!=-1:
                            fol_spd[r]=fol_spd[r-1]
                        if fol_spd[r+1]!=-1:
                            fol_spd[r]=fol_spd[r+1]
                        else:
                            continue
'''
