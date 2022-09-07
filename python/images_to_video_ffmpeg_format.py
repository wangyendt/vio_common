#!/usr/bin/env python


import argparse
import os

def main():
    parser = argparse.ArgumentParser(description='Create ffmpeg format for several images combining to a video.')
    parser.add_argument('images_dir', help='input images directory')
    parser.add_argument('output_txt_path', help='output txt file path')


    args = parser.parse_args()
    assert os.path.exists(args.images_dir)
    # assert os.path.exists(args.output_txt_path)

    ts_list = []
    for file in os.listdir(args.images_dir):
        ts = int(file[:file.index('.')]) / 1e9
        ts_list.append(ts)
    ts_diff = [ts_list[i+1]-ts_list[i] for i in range(len(ts_list)-1)]
    # print(ts_diff)
    # print(len(ts_diff))
    #     print(os.path.join(args.images_dir, file))
    with open(args.output_txt_path, 'w') as f:
        for i, file in enumerate(os.listdir(args.images_dir)):
            # f.write(f'file {os.path.join(args.images_dir, file)}\n')
            if i:
                f.write(f'duration {ts_diff[i-1]}\n')
            f.write(f'file images/{file}\n')
    with open(os.path.join(os.path.dirname(args.output_txt_path), 'run_ffmpeg_images_combined.bat'), 'w') as f:
        f.write("ffmpeg -f concat -i ffmpeg.txt movie.mp4\npause")
    with open(os.path.join(os.path.dirname(args.output_txt_path), 'frame_timestamps.txt'), 'w') as f:
        f.write("Frame timestamp[nanosec],Unix time[nanosec]\n")
        for ts in ts_list:
            f.write(f'{int(ts*1e9)},{int(ts*1e9)}\n')



if __name__ == '__main__':
    main()