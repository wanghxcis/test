# ----------------------------------------------------------------------------------------------------------------
# Segment-CNN
# Copyright (c) 2016 , Digital Video & Multimedia (DVMM) Laboratory at Columbia University in the City of New York.
# Licensed under The MIT License [see LICENSE for details]
# Written by Zheng Shou, Dongang Wang, and Shih-Fu Chang.
# ----------------------------------------------------------------------------------------------------------------

import sys, os
import shutil
import csv
import struct
import operator
import time
from argparse import ArgumentParser
from math import log

def main():
  
	
    parser = ArgumentParser(description='SCNN demo, input the video\'s name and frame rate, will give the localization result.')
                                 
    parser.add_argument('-a','--annotation',required=True,
                        help='''annotation list''')
                        
                      
    # parse input arguments
    
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
    
    args = parser.parse_args()
    annotation_dir = args.annotation
    rootdir = 'D:\\study\\ml\\scnn\\TH14_Temporal_annotations_test\\TH14_Temporal_Annotations_Test\\annotations\\annotation'
    file_list = os.listdir(rootdir)
   
    
    outfile = open("d:\\t.txt", 'w')
    
    file_class_dict = {}
    
    for i in range(0,len(file_list)):
      path = os.path.join(rootdir,file_list[i])
      if os.path.isfile(path):
        file_part = file_list[i].split('_')
        label = class_dict.get(file_part[0], -1)
        annotation_file = open(path, 'r')
        for line in annotation_file:
        	line_split = line.split()
        	time_interval = (float(line_split[1]), float(line_split[2]))
        	file_name = line_split[0]
        	if file_name in file_class_dict:
        		file_class_dict[file_name][label].append(time_interval)
        	else:
        		file_class_dict[file_name] = [[] for i in range(21)]
        		file_class_dict[file_name][label].append(time_interval)
    #outfile.write(dict)
    outfile.close()
    print(file_class_dict)
    start_time = time.time()


if __name__ == "__main__":
    main()
