#!/usr/bin/env python
"""convert a video to a seq of images
   Ref: https://www.pyimagesearch.com/2017/01/09/count-the-total-number-of-frames-in-a-video-with-opencv-and-python/
   assume opencv3 is used
"""

from __future__ import print_function
from doctest import OutputChecker
from email import header
import time
import sys
import os
import shutil
import argparse
import cv2
import numpy as np
import pandas as pd


def parseArgs():
    # setup the argument list
    parser = argparse.ArgumentParser(
        description='Convert a video to a sequence of image frames, optionally downsample.')
    parser.add_argument('video',
                        nargs='?', help='Video filename')
    parser.add_argument('output_folder',
                        help='An folder to output the image sequences')
    parser.add_argument('--video_time_file', nargs='?',
                        help='The csv file containing timestamps of every '
                        'video frames in IMU clock(default: %(default)s).'
                        ' Except for the header, each row has the '
                        'timestamp in nanosec as its first component')
    parser.add_argument('--video-from-to', metavar='video_from_to', type=int,
                        nargs=2,
                        help='Use the video frames starting from up to this'
                             ' number based on the video frames(0-based indexing).')
    parser.add_argument('--choose-every-n', type=int,
                        nargs='?',
                        help='Downsample the frames to frame_count / choose_every_n.')
    parser.add_argument('--downsample-by-2',  action='store_true', dest='downsample_by_2',
                        help='Downsample a frame to half of its original width and length.')
    parser.add_argument('--save_rgb',  action='store_true',
                        help='Save RGB or gray.')
    parser.add_argument('--imu', metavar='imu', type=str,
                        help='IMU rawdata filename')
    parser.add_argument('--imu-output-folder', type=str, metavar='imu_output_folder',
                        help='Specify the imu output folder, typically /mav0/imu0')
    # print help if no argument is specified
    if len(sys.argv) < 2:
        msg = 'Example usage: {} video_and_frame_timestamps/IMG_2805.MOV ' \
            'video_and_frame_timestamps/IMG_2805/ ' \
              '--video-from-to 0 500 --choose-every-n 2 --downsample-by-2\n '.format(
                  sys.argv[0])

        print(msg)
        parser.print_help()
        sys.exit(1)

    parsed = parser.parse_args()
    return parsed


def emptyfolder(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)


def video_to_frames(input_loc, output_loc,
                    video_time_file=None,
                    video_from_to=None,
                    choose_every_n=None,
                    downsample_by_2=None,
                    save_rgb=False):
    """Function to extract frames from input video file
    and save them as separate frames in an output directory.
    Args:
        input_loc: Input video file.
        output_loc: Output directory to save the frames.
    Returns:
        None
    """
    try:
        os.makedirs(output_loc)
    except OSError:
        pass
    # emptyfolder(output_loc)
    # Log the time
    time_start = time.time()
    # Start capturing the feed
    cap = cv2.VideoCapture(input_loc)
    # Find the number of frames
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("#frames in video: %d" % video_length)

    if video_time_file:
        video_time_stamp = pd.read_csv(video_time_file).values[:, 0] * 1000
    if video_from_to:
        minframeid = max(0, video_from_to[0])
        maxframeid = min(video_length - 1, video_from_to[1])
    else:
        minframeid = 0
        maxframeid = video_length - 1

    if choose_every_n:
        frame_ids = range(minframeid, maxframeid + 1, choose_every_n)
    else:
        frame_ids = range(minframeid, maxframeid + 1)

    print("Converting video...\n")
    count = 0
    savedcount = 0
    df_dict = dict()
    while cap.isOpened():
        # Extract the frame
        ret, frame = cap.read()
        if frame is None:
            print('Empty frame, break the video stream, latest frame id %d.' % count)
            break
        if count in frame_ids:
            if save_rgb:
                image_np = frame
            else:
                image_np = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            h, w = image_np.shape[:2]
            if w < h:
                image_np = cv2.rotate(image_np, cv2.ROTATE_90_COUNTERCLOCKWISE)
                w, h = h, w
            if downsample_by_2:
                # image_np = cv2.resize(image_np, dsize=(h // 2, w // 2))
                image_np = cv2.pyrDown(image_np, dstsize=(w // 2, h // 2))
            # Write the results back to output location.
            cv2.imwrite(os.path.join(
                output_loc, f"{video_time_stamp[savedcount] // 1000}.png"), image_np)
            df_dict[savedcount] = {
                '#timestamp [ns]': video_time_stamp[savedcount] // 1000,
                'filename': f"{video_time_stamp[savedcount] // 1000}.png"
            }
            savedcount += 1
            cv2.imshow('frame', image_np)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        count += 1
        if count > (video_length - 1):
            print("Reach end of video, lastest frame id %d" % count)
            break

    # Save data.csv
    pd.DataFrame.from_dict(df_dict).T.to_csv(os.path.join(
        os.path.dirname(output_loc), 'data.csv'), index=False)
    np.savetxt(os.path.join(os.path.dirname(output_loc), 'timestamp.txt'), [
               df_dict[i]['#timestamp [ns]'] for i in df_dict], fmt='%d')

    # Log the time again
    time_end = time.time()
    # Release the feed
    cap.release()
    cv2.destroyAllWindows()
    # Print stats
    print("Done extracting %d from %d to %d out of video with %d frames." % (
        savedcount, minframeid, maxframeid, video_length))
    print("It took %d seconds for extraction." % (time_end-time_start))


def imu_to_frames(imu_path: str, out_path: str):
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    data = pd.read_csv(imu_path, delimiter=',')
    data.columns = '#timestamp [ns],w_RS_S_x [rad s^-1],w_RS_S_y [rad s^-1],w_RS_S_z [rad s^-1],a_RS_S_x [m s^-2],a_RS_S_y [m s^-2],a_RS_S_z [m s^-2],system_time'.split(',')
    data.drop('system_time', axis=1, inplace=True)
    data.to_csv(os.path.join(out_path, 'data.csv'), index=None)


def main():
    parsed = parseArgs()
    imu_to_frames(parsed.imu, parsed.imu_output_folder)
    video_to_frames(parsed.video, parsed.output_folder, parsed.video_time_file, parsed.video_from_to,
                    parsed.choose_every_n, parsed.downsample_by_2, parsed.save_rgb)


if __name__ == "__main__":
    main()
