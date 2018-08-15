from os import listdir
from os.path import isfile, join
import numpy
import cv2
import sys

# DELETE .DS-STORE in dataset folder if issues with first file in array

if os.path.isdir('cropped-images'):
    shutil.rmtree('cropped-images')
os.mkdir("cropped-images", 0755);

mypath = 'pictures-1280by720'
img_path = []

# Store all images in an Array
print("Collecting all Images in Path...")
onlyfiles = [ f for f in sorted(listdir(mypath)) if isfile(join(mypath,f)) ]
images = numpy.empty(len(onlyfiles), dtype=object)
for n in range(0, len(onlyfiles)):
	try:
		images[n] = cv2.imread(join(mypath,onlyfiles[n]) )
		img_path += onlyfiles
	except:
		print('error')

# Loop through each image and crop/save
print("\nProcessing all Images in Path...")
count = 0
for image in images[:-1]:
    image_name = img_path[count][:-4]
    print("Processing %s Image" % image_name)
    crop = [image[88:110, 480:502] , image[101:123, 476:498],image[113:135, 469:491],\
		image[122:144, 460:482], image[137:164, 445:472],image[155:182, 451:478], \
		image[170:197, 436:463], image[183:218, 414:449], image[208:243, 399:434],\
		image[230:271, 381:422], image[255:296, 375:416], image[287:328, 357:398],\
		image[311:359, 328:376], image[357:412, 300:355], image[399:454, 276:331], \
		image[445:503, 245:303], image[503:567, 219:283], image[70:102, 709:741],\
		image[93:117, 729:753], image[103:127, 732:756], image[119:143, 734:758], \
		image[143:167, 736:760], image[158:182, 743:767], image[171:204, 745:778], \
		image[189:222, 759:792], image[214:258, 771:815], image[251:301, 776:826], \
		image[277:332, 799:854], image[317:372, 815:870], image[355:410, 828:883], \
		image[412:467, 845:900]]
    for j in range(len(crop)):
    	p = crop[j]
    	cv2.imwrite("cropped-images/" + image_name + "-p" + str(j) + ".jpg", p)
    count += 1

print("Processing Complete!")

cv2.destroyAllWindows()
