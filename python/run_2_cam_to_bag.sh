dataset_root=$1
output_bag=$2
python3 kalibr_bagcreater.py --folder $dataset_root --output_bag $output_bag
