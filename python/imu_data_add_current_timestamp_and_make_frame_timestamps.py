#!/usr/bin/env python


import argparse
import enum
import imp
import os
import pandas as pd
import time
from datetime import datetime
import numpy as np
from natsort import natsorted

def main():
    parser = argparse.ArgumentParser(description='Add a column to gyro_acc.csv collected by SlamDemo')
    parser.add_argument('imu_path', help='input imu path')
    parser.add_argument('images_path', help='input images path')
    parser.add_argument('frame_ts_path', help='input frame timestamp path')

    args = parser.parse_args()
    assert os.path.exists(args.imu_path)

    path = args.imu_path
    data = pd.read_csv(path)
    cur_time = datetime.now().timestamp()
    ts = data['#timestamp [ns]'].values / 1e9
    # data["current_timestamp"] = (1e9*(np.arange(0,ts[-1]-ts[0]+0.001,0.002)+cur_time)).astype(int)
    data["current_timestamp"] = (1e9*(ts - ts[0] + cur_time)).astype(int)
    # data["timestamp"] += 4e15
    # data["timestamp"] /= 1e9
    # data = data.astype(float)
    data.to_csv(path.replace('.csv','_col_added.csv'),index=None)
    # if os.path.exists(args.frame_ts_path):
    #     os.remove(args.frame_ts_path)
    with open(args.frame_ts_path.replace('.csv','_col_added.csv'), 'w') as f:
        f.write('Frame timestamp[nanosec],Unix time[nanosec]\n')
        for i, file in enumerate(natsorted(os.listdir(args.images_path))):
            if not file.endswith('.png'): continue
            save_time = int(file[:file.index('.')]) - data.loc[0, "#timestamp [ns]"] + data.loc[0, "current_timestamp"]
            # print(f"{file[:file.index('.')]},{save_time}\n",save_time)
            f.write(f"{file[:file.index('.')]},{save_time}\n")





if __name__ == '__main__':

    main()
