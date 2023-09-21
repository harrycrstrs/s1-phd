# Imports
import os.path as path
import os
import glob
import subprocess

# ZIP_DIR set to storage place of COSSC images 
ZIP_DIR = '/exports/csce/datastore/geos/groups/MitchardGroupData/FODEX/Raw_EO_Data/S1/Gabon/zipfiles'
####input('Folder to find S1 zip files: ')
# Create Folder to put split files in
SPLIT_DIR = '/disk/scratch/local.4/harry/S1/split'
####input('Folder to write split files: ')
if not path.exists(SPLIT_DIR):
    os.mkdir(SPLIT_DIR)

# Input Swath information
passdir = 'D'###input('Pass direction of input images: ')
swath = 'IW'+'3'###input('Swath number for TOPSAR-Split: ')
firstBurst = '6'###input('First Burst Index for TOPSAR-Split: ')
lastBurst = '9'###input('Last Burst Index for TOPSAR-Split: ')

files = glob.glob(path.join(ZIP_DIR,'*.zip')) # find zipfiles
files.sort() # Ensures they are in chronological order

N = len(files) # total number of images
print('Discovered '+str(N)+' S1 zip files')
dates = [f.split('_')[-4].split('T')[0] for f in files] # Get list of image dates
outfiles = [path.join(SPLIT_DIR,
                       '_'.join(['S1',passdir,D,'split.dim'])
                       ) for  D in dates] # get list of output file names
exists = [path.exists(o) for o in outfiles] # true if already done
to_do = [not x for x in exists]
print('Already completed '+str(sum(exists))+' files')

for i in range(N):
    if exists[i] == False:
        subprocess.check_output(['python',
                                 '/home/s1332488/code/S1/get_split_file.py',
                                 files[i],
                                 outfiles[i],
                                 swath,
                                 firstBurst,
                                 lastBurst
                                 ], stderr=subprocess.STDOUT)
        to_go = sum(to_do[i+1:])
        print('*******************************')
        print(str(to_go)+' FILES REMAINING')