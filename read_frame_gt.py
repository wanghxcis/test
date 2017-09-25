import sys, os
import shutil
import csv
import struct
import operator
import time
import numpy as np
from argparse import ArgumentParser
from math import log
import math

def main():
    annotation_files_dir = 'D:\\'
    video_allframe_dir = 'D:\\'
    video_allbin_dir
    
    
    class_dict = {}
    class_dict['BaseballPitch'] = 1
    class_dict['BasketballDunk'] = 2
    class_dict['Billiards'] = 3
    class_dict['CleanAndJerk'] = 4
    class_dict['CliffDiving'] =5
    class_dict['CricketBowling'] = 6
    class_dict['CricketShot'] = 7
    class_dict['Diving'] = 8
    class_dict['FrisbeeCatch'] = 9
    class_dict['GolfSwing'] = 10
    class_dict['HammerThrow'] = 11
    class_dict['HighJump'] = 12
    class_dict['JavelinThrow'] = 13
    class_dict['LongJump'] = 14
    class_dict['PoleVault'] = 15
    class_dict['Shotput'] = 16
    class_dict['SoccerPenalty'] = 17
    class_dict['TennisSwing'] = 18
    class_dict['ThrowDiscus'] = 19
    class_dict['VolleyballSpiking'] = 20
    
    
    # get the test video, and initialize the frame array for each video
    
    video_class_frame_gt = {}
    video_class_interval_gt = {}
    
    annotation_list = os.listdir(annotation_file_dir)
    for i in range(len(annotation_list)):
        annotation_path = os.path.join(annotation_files_dir, annotation_list[i])
        anno_file = open(path, 'r')
        anno_class_name = annotation_list[i].split('_')[0]
        anno_class_label = class_dict.get(anno_class_name)
        for line in anno_file:
            line_content = line.split()
            time_interval = (float(line_content[1]), float(line_content(2))
            interval_frame_index = (int(time_interval[0] * 25), int(time_interval[1] *25) )
            video_name = line_content[0]
            if video_name in video_class_frame_gt:
                video_class_frame_gt[video_name][anno_class_label].append(interval_frame_index)
            else:
                video_class_frame_gt[video_name] = [[] for _ in range(21)]
                video_class_frame_gt[video_name][anno_class_label].append(interval_frame_index)
        anno_file.close()    
    


# response row is class_label * frame_num 32
def read_binary_blob(filename):
    f = open(filename, 'rb')
    s = struct.unpack('iiiii', f.read(20)) # the first five are integers
    length = s[0]*s[1]*s[2]*s[3]*s[4]
    data = struct.unpack('f'*length, f.read(4*length))
    f.close()
    return list(data)
    
def read_video_test_allframe_blob(video_name):
    需要确认文件路径video_frame_dir = os.path.join(video_allframe_dir, video_name.split('_')[-1])
    frame_num = 0
    if os.path.exists(video_frame_dir):
        frame_list = os.listdir(video_frame_dir)
        frame_num = len(frame_list)
    需要确认文件路径video_bin_dir = os.path.join(video_allbin_dir, video_name.split('_')[-1])
    
    
    # 0 for background 21 for anbiguous  normal class 1:20
    res = np.empty(shape=(0,22))
    if os.path.exists(video_bin_dir):
        bin_list = os.listdir(video_bin_dir)
        for i in range(len(bin_list)):
            blob = read_binary_blob(os.path.join(video_bin_dir, bin_list[i]))
            blob_np_arr = np.array(blob)
            # class by frame 22 * 32
            tmp = np.reshape(22,-1)
            # frame by class  32 * 22
            frame_result = np.transpose(tmp)
            res = np.concatenate(res, frame_result)
    new_res = np.zeros((frame_num, 22), dtype='float')
    bin_num = len(bin_list)
    if frame_num == 32 * bin_num:
        new_res = res
    elif frame_num < 32 * bin_num:
        idx = [i for i in range(32 * (bin_num -1))]
        new_res[idx] = res[idx]
        idx_last_frame = [i  + 32 * (bin_num -1) for i in range(frame_num - 32 * (bin_num-1))]
        dix_last_frame_bin = [ -i for i in range(frame_num - 32 * (bin_num-1), 0, -1)]
        new_res[idx_last + 32] = res[dix_last_frame_bin]
        
    else:
        print error frame num and bin num !!! 
    
    return new_res[:, 0:21]
    
#for every video file, we generate seg_swin(sccn) and the cdc probability matrix frame by class    
def fine_scnn(seg_swin):
    for i in range(len(seg_swin)):
        video_name = seg_swin[i][0]  需要确认
        prob_res = read_video_test_allframe_blob(video_name)
        seg_swin[i][2] = max(1, seg_swin[i][2] - seg_swin[i][1]/8)
        seg_swin[i][3] = min(seg_swin[i][3] + seg_swin[i][1] / 8, len(prob_res))
        #frame index start from 1 in seg_swin
        seg_prob = prob[ (seg_swin[i][2]-1) : seg_swin[i][3]]
        mean_prob = seg_prob.mean(axis=0)
        #class_lable 0 : background 1:
        class_label = np.argmax(mean_prob)
        seg_swin[i][10] = class_label
        seg_class_prob = seg_prob[:, label]
        mu = seg_class_prob.mean()
        seg_len = len(seg_class_prob)
        sigma = seg_class_prob.std() * math.sqrt(float(seg_len)/ (seg_len-1))
        minthre = mu - sigma
        idx_arr = np.where(seg_class_prob >= minthre)[0]
        s = seg_swin[i][2]
        seg_swin[i][2] = s + ind_arr[0]
        seg_swin[i][3] = s + ind_arr[-1]
        seg_swin[i][4] = seg_swin[i][2]/25
        seg_swin[i][5] = seg_swin[i][3]/25
        seg_swin[i][1] = seg_swin[i][3] - seg_swin[i][2] + 1
        seg_swin[i][8] = prob[ (seg_swin[i][2] - 1) : seg_swin[i][3], class_label].mean(axis = 0)
    return seg_swin    
        
        
        	
def get_mean_average_pre:
    for i in range(21):
        get_pre_perclass(i+1)
        
        
def get_pre_perclass(class_label, threshold):
    gd_class_interval_num = 0
    unsort_conf = []
    unsort_flag = []
    for video_name in video_set:
        res_swin = read_video_res_swin(video_name, threshold)
        intervals = video_class_frame_gt[video_name][class_label]
        gd_class_interval_num += len(intervals)
        new_res_swin = []
        for row in res_swin:
            if row[10] == class_label:
                new_res_swin.append(row)
        if len(new_res_swin) == 0:
            continue
        sorted(new_res_swin, key = lambda x:x[8], reverse = True)
        indfree = [1 for _ in len(new_res_swin)]
        ov = get_overlap(intervals, new_res_swin)
        for ov_idx in ov:
            for in
        
        
def get_overlap(gd_intervals, res_swin):

        
# different threshhold for differ res_swin
def read_video_res_swin(video_name, threshold):
        
        
if __name__ == "__main__":
    main()