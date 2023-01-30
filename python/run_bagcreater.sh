# ------------------------- WORK -----------------------------------------
# 用于将IMU转为rosbag
# root=/mnt/d/work/data/phone_data/slam/2022_07_25_15_33_52_slam
# python3 kalibr_bagcreater.py --folder $root --imu $root/gyro_accel.csv --output_bag $root/imu2.bag

# 用于将图片转为rosbag
# python3 create_rosbag_for_images_in_dir.py "/mnt/d/work/data/phone_data/android/monocular_imgs/aprilgrid" "/mnt/d/work/data/phone_data/android/monocular_imgs/aprilgrid/img.bag"
# python3 create_rosbag_for_images_in_dir.py "/mnt/d/work/data/phone_data/slam/2022_08_09_11_26_09_img_cali" "/mnt/d/work/data/phone_data/slam/2022_08_09_11_26_09_img_cali/img.bag"

# 用于将标定视频转为rosbag
# root="/mnt/d/work/data/phone_data/slam/2022_09_07_17_02_04_imu_cam_cali_horizontal_big_screen_0.382"
# python3 kalibr_bagcreater.py --folder $root --imu $root/gyro_acc.csv --video $root/movie.mp4 --video_time_file $root/frame_timestamps.txt --output_bag $root/cam+imu2.bag

# 用于将视频和IMU数据转化为euroc数据格式(用于跑vio，不是为了标定)
# root="/mnt/d/work/data/phone_data/slam/2022_08_09_17_12_14_slam"
# python3 video-imu-to-frames_v1.py $root/movie.mp4 $root/mav0/cam0/data --choose-every-n 1 --downsample-by-2 --video_time_file $root/frame_timestamps.txt --imu $root/gyro_accel.csv --imu-output-folder $root/mav0/imu0


# 用SlamDemo保存的Cam+Imu转换成rosbag(用于标定)
# root="/mnt/d/work/data/phone_data/slam/2022_09_07_17_02_04_imu_cam_cali_horizontal_big_screen_0.382"
# root="/mnt/e/data/slam/2022_09_07_17_21_09_imu_cali_slamdemo"
# python3 images_to_video_ffmpeg_format.py $root/images $root/ffmpeg.txt      # step 1.
# $root/run_ffmpeg_images_combined.bat -y                                   # step 2. run on Windows
# python3 kalibr_bagcreater.py --folder $root --imu $root/gyro_acc_col_added.csv --video $root/movie.mp4 --video_time_file $root/frame_timestamps.txt --output_bag $root/cam+imu2.bag

# 视频分解为图片，imu单独做修改，生成cam.bag和imu.bag，再合并为cam+imu.bag（用于标定）
# root="/mnt/d/work/data/phone_data/slam/2022_09_07_17_02_04_imu_cam_cali_horizontal_big_screen_0.382"
# python3 video-imu-to-frames_v1.py $root/movie.mp4 $root/mav0/cam0/data --choose-every-n 1 --video_time_file $root/frame_timestamps.txt --imu $root/gyro_acc.csv --imu-output-folder $root/mav0/imu0
# python3 create_rosbag_for_images_in_dir.py $root/images $root/cam.bag
# python3 imu_data_add_current_timestamp_and_make_frame_timestamps.py $root/gyro_acc.csv $root/images $root/frame_timestamps.txt
# python3 kalibr_bagcreater.py --folder $root --imu $root/gyro_acc_col_added.csv --output_bag $root/imu.bag
# python3 merge_rosbag.py -v $root/cam+imu.bag $root/cam.bag $root/imu.bag


# 将SlamDemo采集的数据转化为cam+imu数据格式（用于跑VIO）
root="/media/psf/work/project/20230116 slam数据采集/data"
# python3 create_rosbag_for_images_in_dir.py "$root/mav0/cam0/data" "$root/cam.bag"
python3 imu_data_add_current_timestamp_and_make_frame_timestamps.py "$root/mav0/imu0/data.csv" "$root/mav0/cam0/data" "$root/mav0/cam0/data.csv"
python3 kalibr_bagcreater.py --folder "$root" --imu "$root/mav0/imu0/data_col_added.csv" --output_bag "$root/cam+imu.bag"


# 将SlamDemo采集的数据转化为cam+imu.bag（用于标定）


# ------------------------- WORK -----------------------------------------




# ------------------------- HOME -----------------------------------------
# IMU生成bag
# path="/mnt/e/data/2022_07_30_03_08_26_mate20_imu_cali_2"
# python3 kalibr_bagcreater.py --folder $path --imu $path/gyro_accel.csv --output_bag $path/imu.bag
# ------------------------- HOME -----------------------------------------
