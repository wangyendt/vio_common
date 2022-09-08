#!/usr/bin/env python


import argparse
import imp
import os
import pandas as pd
import time
from datetime import datetime
import numpy as np

def main():
    parser = argparse.ArgumentParser(description='Add a column to gyro_acc.csv collected by SlamDemo')
    parser.add_argument('imu_path', help='input imu path')

    args = parser.parse_args()
    assert os.path.exists(args.imu_path)

    path = args.imu_path
    data = pd.read_csv(path)
    cur_time = datetime.now().timestamp()
    ts = data['timestamp'].values / 1e9
    data["current_timestamp"] = (1e9*(np.arange(0,ts[-1]-ts[0]+0.001,0.002)+cur_time)).astype(int)
    # data["timestamp"] += 4e15
    # data["timestamp"] /= 1e9
    # data = data.astype(float)
    data.to_csv(path.replace('.csv','_col_added.csv'),index=None)




if __name__ == '__main__':

    main()
