data_root="$1"
echo $data_root
python3 kalibr_bagcreater.py --imu "$data_root/data.csv" --output_bag "$data_root/imu.bag"