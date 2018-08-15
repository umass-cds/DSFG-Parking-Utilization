###########################################
#      DSFG ~ Katie House ~ 8/6/18
# DESCTIPTION: preprocesses Camera FTP data
# INPUT: directory name with .zip files
# OUTPUT: pictures for every 15 minutes
###########################################

import os, zipfile
import re
import shutil
import sys
from PIL import Image
from PIL import ImageFile 
ImageFile.LOAD_TRUNCATED_IMAGES = True

# ~~~~ DEFINE VAIRABLES ~~~~~
# NOTE: Update dir_name with local directories
path_to_github = 'C:\\Users\\house\\Documents\\GitHub\\DSFG\\DSFG-Parking-Utilization'
github_data_path = '\\preprocessing\\townhall-data\\entire-dataset'
path_to_gdrive = 'C:\\Users\\house\\Google Drive (khouse@umass.edu)\\DS4Good - Parking Area Utilization'
gdrive_data_path = '\\Datasets\\Town Hall Lot Dataset\\pictures_8-6to8-12' 
dir_name = path_to_github + github_data_path
dest = path_to_gdrive + gdrive_data_path

# ~~~~ DEFINE FUNCTIONS ~~~~~
def save_image(file_path, file_name):
	# Compress Image
	new_width  = 800
	new_height = 600
	im = Image.open(file_path)
	im = im.resize((new_width, new_height), Image.ANTIALIAS)
	im.save(file_path)
	shutil.copy(file_path, dest) # Remove comment if sending to GDrive
	print('saving: %s' % file_name)

def main():
	'''
	# Remove old pictures from g-drive directory
	for the_file in os.listdir(dest):
	    file_path = os.path.join(dest, the_file)
	    try:
	        if os.path.isfile(file_path):
	            os.unlink(file_path)
	    except Exception as e:
	        print(e)
	'''
	# Loop through each file in data directory
	for filename in os.listdir(dir_name):
		sub_dirname = dir_name + '\\' + filename
		os.chdir(sub_dirname) # change directory from working dir to dir with files
		
		# Unzip each file in data directory
		extension = ".zip"
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
					save_image(file_path, file)
				elif (file_min == '6') and (prev_file_min == '4')\
					and file[9] in('1','4'):
					save_image(file_path, file)
				elif file_min == '5' and file[9] in('1','4'):
					save_image(file_path, file)
				elif file_min == '0' and file[9] in('0','3'):
					save_image(file_path, file)
			else:
				prev_file = file
				prev_file_min = prev_file[10]
				print('removing: %s' % file)
				os.remove(file)
			prev_file = file
			prev_file_min = prev_file[10]
		
		
# ~~~~ RUN MAIN FUNCTION ~~~~~
if __name__ == '__main__':
    main()
