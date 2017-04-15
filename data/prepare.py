import sys
import numpy as np
#  import packages


TERM_NUM = 24
FORECASTING_NUM = 24
LABEL_VALUE_NUM = 4
with open("speeds.csv") as f:
    line = f.readline()
    f.next()
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
                




