#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import argparse

import rosbag
import rospy

from cv_bridge import CvBridge
import cv2

import play_images_in_rosbag


def decide_output_encoding(cv_img):
    """
    For 16UC1 input image, we need to use mono16 as output encoding option.
    see http://library.isr.ist.utl.pt/docs/roswiki/cv_bridge(2f)Tutorials(2f)
    UsingCvBridgeToConvertBetweenROSImagesAndOpenCVImages.html
    :param cv_img:
    :return:
    """

    coding = 'passthrough'
    if cv_img.dtype == 'uint16':
        coding = 'mono16'
    return coding

def main():
    parser = argparse.ArgumentParser(
        description=("Downscale images and shift timestamps for sensor messages in "
        "a ROS bag with topics '/cam0/image_raw', '/cam1/image_raw', '/imu0'."))
    parser.add_argument("bag_file", help="Input ROS bag.")
    parser.add_argument(
        '--time_delay',
        help="unit nanoseconds, time delay + original.header.stamp = "
        "shifted.header.stamp. If not provided, time delay will set as "
        "ros message time - message[0].header.stamp",
        type=int,
        default=None)
    parser.add_argument("--out_bag_file",
                        help="Output ROS bag file.",
                        default=None)

    args = parser.parse_args()
    out_bag_file = args.out_bag_file
    if args.out_bag_file is None:
        out_bag_file = os.path.join(
            os.path.splitext(args.bag_file)[0] + '_half.bag')

    in_bag = rosbag.Bag(args.bag_file, "r")
    out_bag = rosbag.Bag(out_bag_file, 'w')

    time_shift = None
    if args.time_delay is not None:
        time_shift = rospy.Duration(args.time_delay // 1000000000,
                                    args.time_delay % 1000000000)
        print('Raw message time offset set to {}'.format(time_shift))

    count = 0
    for topic, msg, t in in_bag.read_messages(topics=['/imu0']):
        if time_shift is None:
            time_shift = t - msg.header.stamp
            print('Raw message time offset set to {}'.format(time_shift))
        msg.header.stamp = time_shift + msg.header.stamp
        out_bag.write(topic, msg, msg.header.stamp)
        count += 1
    print('Saved {} messages on topic /imu0'.format(count))

    bridge = CvBridge()
    for k in range(2):
        count = 0
        image_topic = '/cam{}/image_raw'.format(k)
        encoding = ''
        for _, msg, t in in_bag.read_messages(topics=[image_topic]):
            cv_img = bridge.imgmsg_to_cv2(msg, desired_encoding="passthrough")
            h, w = cv_img.shape[:2]
            cv_half_img = cv2.pyrDown(cv_img, dstsize=(w // 2, h // 2))
            if count == 0:
                print('Image info before and after half sampling:')
                play_images_in_rosbag.print_image_info(cv_img)
                play_images_in_rosbag.print_image_info(cv_half_img)
                encoding = decide_output_encoding(cv_img)

            cv2.imshow('Downsampled frame', cv_half_img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            count += 1

            rosimage = bridge.cv2_to_imgmsg(cv_half_img, encoding=encoding)
            rosimage.header.stamp = time_shift + msg.header.stamp
            out_bag.write(image_topic, rosimage, rosimage.header.stamp)
        print('Saved {} images on topic {}'.format(count, image_topic))

    cv2.destroyAllWindows()
    out_bag.close()
    in_bag.close()

    print("Output bag: {}".format(out_bag_file))

if __name__ == '__main__':
    main()
