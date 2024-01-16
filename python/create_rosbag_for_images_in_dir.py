#!/usr/bin/env python

from __future__ import print_function
import sys

import kalibr_bagcreater


def main():
    if len(sys.argv) < 3:
        print("Usage: {} <folder from which images will be recursively found> <output bag path>".format(sys.argv[0]))
        sys.exit(1)
    if len(sys.argv) == 3:
        # data_dir, output_dir
        kalibr_bagcreater.create_rosbag_for_images_in_dir(sys.argv[1], sys.argv[2])
    if len(sys.argv) == 4:
        # data_dir, output_dir, bootstrap_n_samples
        kalibr_bagcreater.create_rosbag_for_images_in_dir(sys.argv[1], sys.argv[2], bootstrap_n_samples=int(sys.argv[3]))
    if len(sys.argv) == 5:
        # data_dir, output_dir, bootstrap_n_samples, bootstrap_n_trials
        print(int(sys.argv[3]), int(sys.argv[4]))
        kalibr_bagcreater.create_rosbag_for_images_in_dir(sys.argv[1], sys.argv[2], bootstrap_n_samples=int(sys.argv[3]), bootstrap_n_trials=int(sys.argv[4]))


if __name__ == "__main__":
    main()
