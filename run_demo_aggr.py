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
    args = parser.parse_args()
    annotation_dir = args.annotation
    rootdir = 'D:\\study\\ml\\scnn\\TH14_Temporal_annotations_test\\TH14_Temporal_Annotations_Test\\annotations\\annotation'
    outfile = open("d:\\study\\text.txt", "w")
    namefile = open("d:\\study\\name.txt", "w")
    file_list = os.listdir(rootdir)
    file_set = set()
    for i in range(0,len(file_list)):
      path = os.path.join(rootdir,file_list[i])
      file_part = file_list[i].split('_')
      namefile.write(file_part[0] + "\n")
      #print(path)
      if os.path.isfile(path):
        annotation_file = open(path, 'r')
        for line in annotation_file:
           line_info = line.split()	
           file_set.add(line_info[0])
    
    for file_name in file_set:
    	outfile.write(file_name + "\n")
    	
    outfile.close()
    namefile.close()
    start_time = time.time()


if __name__ == "__main__":
    main()
