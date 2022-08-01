# ------------------------- WORK -----------------------------------------
# 用于将IMU转为rosbag
# root=/mnt/d/work/data/phone_data/android/2022_07_25_15_33_52_slam
# python3 kalibr_bagcreater.py --folder $root --imu $root/gyro_accel.csv --output_bag $root/imu2.bag

# 用于将图片转为rosbag
# python3 create_rosbag_for_images_in_dir.py "/mnt/d/work/data/phone_data/android/monocular_imgs/aprilgrid" "/mnt/d/work/data/phone_data/android/monocular_imgs/aprilgrid/img.bag"

# 用于将标定视频转为rosbag
root="/mnt/d/work/data/phone_data/android/2022_07_29_11_47_06_imu_cam_cali_horizontal_dark_bs_fast_1"
python3 kalibr_bagcreater.py --folder $root --imu $root/gyro_accel.csv --video $root/movie.mp4 --video_time_file $root/frame_timestamps.txt --output_bag $root/cam+imu.bag
# ------------------------- WORK -----------------------------------------




# ------------------------- HOME -----------------------------------------
# IMU生成bag
path="/mnt/e/data/2022_07_30_03_08_26_mate20_imu_cali_2"
python3 kalibr_bagcreater.py --folder $path --imu $path/gyro_accel.csv --output_bag $path/imu.bag
# ------------------------- HOME -----------------------------------------
