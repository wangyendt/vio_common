root=$1  # "/media/psf/work/data/slam/mate20/calibration"
dataset_root=$1
# python3 kalibr_bagcreater.py --folder $dataset_root --output_bag $dataset_root/cam.bag
# python3 kalibr_bagcreater.py --imu $dataset_root/mav0/imu0/data.csv --output_bag $dataset_root/imu.bag
# python3 create_rosbag_for_images_in_dir.py "$root/mav0/cam0" "$root/cam.bag"
# python3 merge_rosbag.py -v $root/cam+imu.bag $root/cam.bag $root/imu.bag
python3 imu_data_add_current_timestamp_and_make_frame_timestamps.py "$dataset_root/mav0/imu0/data.csv" "$dataset_root/mav0/cam0/data" "$dataset_root/mav0/cam0/data.csv"
python3 kalibr_bagcreater.py --folder "$dataset_root" --imu "$dataset_root/mav0/imu0/data_col_added.csv" --output_bag "$dataset_root/cam+imu.bag"

