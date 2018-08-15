from os import listdir
from os.path import isfile, join
import numpy
import os, shutil
import cv2, re
import sys, time, datetime, csv
from scripts import label_parking_space
# DELETE .DS-STORE in dataset folder if issues with first file in array

if os.path.isdir('cropped-images'):
    shutil.rmtree('cropped-images')
os.mkdir("cropped-images", 0755);

mypath = "../../preprocessing/townhall-data/cropped-images"
file_list = sorted(os.listdir(mypath))
   
count = 0
image_path_list = [["P18072806000510", [0, 0]]]
image_path_list
current_index = 0
print("\nProcessing all Images in Path...")
for idx, image in enumerate(file_list):
    image_name = image.split("-")[0]
    if not (any(image_name in sublist for sublist in image_path_list)):
        temp = [image_name, [0, 0]]
        image_path_list.append(temp)
        current_index += 1
        print("Added " + image_name + " to image_path_list")
    print("Now Processing %s Image" % image)         
    out_str = label_parking_space.process_image(mypath + "/" + image)
    list = out_str.splitlines()
    occ_prob = -1.0
    vac_prob = -1.0
    for line in list:
        if line.startswith('occupied'):
            x = re.findall("\d+\.\d+", line)
            occ_prob = x[0]
        if line.startswith('vacant'):
            y = re.findall("\d+\.\d+", line)
            vac_prob = y[0]
    print("vac: " + vac_prob + " occ: " + occ_prob)
    #for index, item in enumerate(image_path_list):
    #    if image_name.split("-")[0] in item:
    if occ_prob > vac_prob:
    	image_path_list[current_index][1] = [image_path_list[current_index][1][0], image_path_list[current_index][1][1] + 1]
    else:
    	image_path_list[current_index][1] = [image_path_list[current_index][1][0] + 1, image_path_list[current_index][1][1]]
    #    else:
    print(image_path_list[current_index][1])

print(image_path_list)
for idx, image in enumerate(image_path_list):
    image_name = image_path_list[idx][0]
    year = image_name[1:3]
    month = image_name[3:5]
    day = image_name[5:7]
    hour = image_name[7:9]
    min = image_name[9:11]
    new_time = month + "/" + day + "/" + year + " " + hour + ":" + min
    print(new_time)
    d = datetime.datetime.strptime(new_time, '%m/%d/%y %H:%M').strftime('%m/%d/%y %H:%M').lstrip('0')
    with open('results.csv', 'wb') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow([d, image_path_list[idx][1][0]])
        wr.write('\n')
cv2.destroyAllWindows()

