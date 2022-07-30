# python3 kalibr_bagcreater.py --folder /mnt/e/data/2022_07_25_11_31_46_imu_cali --imu /mnt/e/data/2022_07_25_11_31_46_imu_cali/gyro_accel.csv --video /mnt/e/data/2022_07_25_11_31_46_imu_cali/movie.mp4 --video_time_file /mnt/e/data/2022_07_25_11_31_46_imu_cali/movie_metadata.csv --output_bag /mnt/e/data/2022_07_25_11_31_46_imu_cali/slam.bag

# IMU生成bag
path="/mnt/e/data/2022_07_30_03_08_26_mate20_imu_cali_2"
python3 kalibr_bagcreater.py --folder $path --imu $path/gyro_accel.csv --output_bag $path/imu.bag
