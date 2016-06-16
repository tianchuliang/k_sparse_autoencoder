# Author: Tianchu Liang
# Date: May 2 2016
'''
This Python script does prepares the data, this involves:
	1. Turn all images to greyscale[DONE]
	2. Save 80 percent of data as training and 20 percent for testing[DONE]
	3. Generate LMDB file for Caffe
	4. Genearte mean image binaryproto file for the autoencoder

To run this script, simply direct yourself to the 
directory where this script lives, and 
type the following in the terminal window:

python prepare_data.py -flag <path to the folder that contains all the images (RGB)>

-flag: 1: Turn all images to greyscale and split them into Train and Test folders with 80 and 20 
percent proportion. 

-flag: 2: Generate LMDB file and save this file in the data path folder

-flag: 3: Generate mean image binaryproto file and save this file in the data path folder

This script will generate two folders within the data path, 'Train' and 'Test'. 
These two folders will contain greyscale images. 
====
====
====
MODIFY THE FOLLOWING PATH VARIABLES TO YOUR ENVIRONMENT BEFORE RUNNING THIS
SCRIPT:
'''

CAFFE_ROOT = '/usr/local/caffe'
DATA_ROOT = '/Users/tianchuliang/Documents/GT_Acad/CSE6240Spring16/tliang37-project2/data'
CODE_ROOT = '/Users/tianchuliang/Documents/GT_Acad/CSE6240Spring16/tliang37-project2/code' 
import os
from os import listdir
import sys
from PIL import Image
import numpy as np 
# from sklearn.cross_validation import train_test_split
# Other global variables:
label_dict = {'fungus':'1','person':'2'}

# Functions:
def split_data(path):
	img_names = listdir(path)

	TRAIN_FOLDER = path + '/Train'
	TEST_FOLDER = path + '/Test'

	os.system('mkdir '+TRAIN_FOLDER)
	os.system('mkdir '+TEST_FOLDER)

	for img_name in img_names:
		try:
			img = Image.open(path+'/'+img_name)

			rand_number = np.random.random()
			
			if rand_number>0.2:
				#put this image into training folder
				img.save(TRAIN_FOLDER+'/'+img_name)
			else:
				#put this image into testing folder
				img.save(TEST_FOLDER+'/'+img_name)

			# os.system('rm '+path+'/'+img_name)
		except IOError:
			continue

def make_txt_file_lmdb(path):
	if (os.path.exists(path+'/Train') and os.path.exists(path+'/Test') ):
		file_names_train = listdir(path+'/Train')
		file_names_test = listdir(path+'/Test')
		os.chdir(path+'/Train')
		os.system('touch Train.txt')
		f = open('Train.txt','w')

		for file_name in file_names_train:
			file_type = file_name.split('.')[-1]
			label_info = file_name.split('_')[0]

			if file_type!='JPEG':
				continue
			else:
				line = '/Train'+'/'+file_name+' '+label_dict[label_info]+'\n'
				f.write(line)
		f.flush()
		f.close()

		os.chdir(path+'/Test')
		os.system('touch Test.txt')
		f_ = open('Test.txt','w')

		for file_name in file_names_test:
			file_type = file_name.split('.')[-1]
			label_info = file_name.split('_')[0]

			if file_type!='JPEG':
				continue
			else:
				line = '/Test'+'/'+file_name+' '+label_dict[label_info]+'\n'
				f_.write(line)
		f_.flush()
		f_.close()

	else:
		print 'Either Train, or Test, or neither exists.'
	
def make_lmdb(path):
	os.chdir(CODE_ROOT+'/Bash_scripts')
	os.system('chmod +x create_lmdb.sh')
	os.system('./create_lmdb.sh')
	 
def gen_mean_file(path):
	TRAIN_DIR = path +'/Train/fungus_person_train_lmdb'
	TEST_DIR = path + '/Test/fungus_person_test_lmdb'

	os.chdir(CAFFE_ROOT+'/build/tools')
	# os.system('ls')
	os.system('./compute_image_mean '+TRAIN_DIR+' '+DATA_ROOT+'/Train/train_mean.binaryproto')
	os.system('./compute_image_mean '+TEST_DIR+' '+DATA_ROOT+'/Test/test_mean.binaryproto')

if __name__ == '__main__':
	if len(sys.argv)>1:
		FLAG = sys.argv[1]
		PATH = sys.argv[2]

		if FLAG=='1':
			split_data(PATH)
		if FLAG=='2':
			make_txt_file_lmdb(PATH)
			# make_lmdb(PATH)
		if FLAG=='3':
			gen_mean_file(PATH)
	else:
		print 'Please provide the data folder path. '
		
