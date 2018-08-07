###########################################
#      DSFG ~ Katie House ~ 8/6/18
# DESCTIPTION: preprocesses Camera FTP data
# INPUT: directory name with .zip files
# OUTPUT: pictures for every 15 minutes
###########################################

import os, zipfile
import re
import shutil

# NOTE: Update dir_name with local directory
dir_name = 'C:\\Users\\house\\Documents\\GitHub\\DSFG\\DSFG-Parking-Utilization\\preprocessing\\townhall-data\\data-by-day'
dest = 'C:\\Users\\house\\Google Drive (khouse@umass.edu)\\DS4Good - Parking Area Utilization\\Datasets\\Town Hall Lot Dataset\\pictures' 
# Define initial file format to unzip
extension = ".zip"

# Remove old g-drive directory
try:
	shutil.rmtree(dest)
	os.remove(dest)
except:
	os.mkdir(dest)

# Loop through each file in data directory
for filename in os.listdir(dir_name):
	sub_dirname = dir_name + '\\' + filename
	os.chdir(sub_dirname) # change directory from working dir to dir with files
	
	# Unzip each file in data directory
	for item in os.listdir(sub_dirname): # loop through items in dir
	    if item.endswith(extension): # check for ".zip" extension
	        file_name = os.path.abspath(item) # get full path of files
	        zip_ref = zipfile.ZipFile(file_name) # create zipfile object
	        zip_ref.extractall(sub_dirname) # extract file to dir
	        zip_ref.close() # close file
	        os.remove(file_name) # delete zipped file

	# Translate to 15 minute increments
	file_list = os.listdir(sub_dirname)
	sorted(file_list)  # sort by time

	# Initialize previous file names
	prev_file = ''
	prev_file_min = -1
	for file in file_list:
		file_min = file[10]
		file_hour = int(file[7:9])
		file_path = os.path.dirname(os.path.abspath(file)) + '\\' + file
		# Only save files within 15-minute increments
		# Test if exact 15-minute increment is missing,
		# If exact time is missing, use 16 minutes
		if file_hour < 20 and file_hour > 5:
			if file_min == '1' and prev_file_min == '9' \
				and file[9] in('0','3'):
				shutil.copy(file_path, dest)
				#print('saving: %s' % file)
			elif (file_min == '6') and (prev_file_min == '4')\
				and file[9] in('1','4'):
				shutil.copy(file_path, dest)
				#print('saving: %s' % file)
			elif file_min == '5' and file[9] in('1','4'):
				shutil.copy(file_path, dest)
				#print('saving: %s' % file)
			elif file_min == '0' and file[9] in('0','3'):
				shutil.copy(file_path, dest)
				#print('saving: %s' % file)
		else:
			prev_file = file
			prev_file_min = prev_file[10]
			print('removing: %s' % file)
			#os.remove(file)
		prev_file = file
		prev_file_min = prev_file[10]
		
		