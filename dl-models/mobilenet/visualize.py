import cv2
import numpy
import os
import sys
import subprocess
import re
import shutil
from os import listdir
from os.path import isfile, join

# Get image path from command line argument
try:
    lot_image_path = sys.argv[1]
except:
	raise ValueError('You must pass an image path')

if os.path.isdir('temp'):
    shutil.rmtree('temp')
path = "temp"
os.mkdir(path, 0755);

lot_image = cv2.imread(lot_image_path)

# Loop through each image and crop/save
print("\nProcessing image...")
crop = [lot_image[88:110, 480:502] , lot_image[101:123, 476:498],lot_image[113:135, 469:491],\
	lot_image[122:144, 460:482], lot_image[137:164, 445:472],lot_image[155:182, 451:478], \
	lot_image[170:197, 436:463], lot_image[183:218, 414:449], lot_image[208:243, 399:434],\
	lot_image[230:271, 381:422], lot_image[255:296, 375:416], lot_image[287:328, 357:398],\
	lot_image[311:359, 328:376], lot_image[357:412, 300:355], lot_image[399:454, 276:331], \
	lot_image[445:503, 245:303], lot_image[503:567, 219:283], lot_image[70:102, 709:741],\
	lot_image[93:117, 729:753], lot_image[103:127, 732:756], lot_image[119:143, 734:758], \
	lot_image[143:167, 736:760], lot_image[158:182, 743:767], lot_image[171:204, 745:778], \
	lot_image[189:222, 759:792], lot_image[214:258, 771:815], lot_image[251:301, 776:826], \
	lot_image[277:332, 799:854], lot_image[317:372, 815:870], lot_image[355:410, 828:883], \
	lot_image[412:467, 845:900]]
for j in range(len(crop)):
    p = crop[j]
    cv2.resize(p, (128, 128)) 
    cv2.imwrite("temp/" + "p" + str(j+1) + "-1.jpg", p)

for file in os.listdir("temp"):
    if file.endswith(".jpg"):
        print(file)
        cmd = "python -m scripts.label_image \
            --graph=tf_files/retrained_graph.pb  \
            --image=temp/" + file + "  \
            --input_height=128  \
            --input_width=128"
        out_str = subprocess.check_output(cmd, shell=True)
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
        print("occ: " + str(occ_prob))
        print("vac: " + str(vac_prob))
        if file == "p1-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (480, 88), 22, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (480, 88), 22, (0,0,255), 2)
        elif file == "p2-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (476, 101), 22, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (476, 101), 22, (0,0,255), 2)
        elif file == "p3-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (469, 113), 22, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (469, 113), 22, (0,0,255), 2)
        elif file == "p4-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (460, 122), 22, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (460, 122), 22, (0,0,255), 2)
        elif file == "p5-1.jpg":           
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (445, 137), 27, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (445, 137), 27, (0,0,255), 2)
        elif file == "p6-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (451, 155), 27, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (451, 155), 27, (0,0,255), 2)
        elif file == "p7-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (436, 170), 27, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (436, 170), 27, (0,0,255), 2)
        elif file == "p8-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (414, 183), 35, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (414, 183), 35, (0,0,255), 2)
        elif file == "p9-1.jpg":  
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (399, 208), 35, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (399, 208), 35, (0,0,255), 2)
        elif file == "p10-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (381, 230), 41, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (381, 230), 41, (0,0,255), 2)
        elif file == "p11-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (375, 255), 41, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (375, 255), 41, (0,0,255), 2)
        elif file == "p12-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (357, 287), 41, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (357, 287), 41, (0,0,255), 2)
        elif file == "p13-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (328, 311), 48, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (328, 311), 48, (0,0,255), 2)
        elif file == "p14-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (300, 357), 55, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (300, 357), 55, (0,0,255), 2)
        elif file == "p15-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (276, 399), 55, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (276, 399), 55, (0,0,255), 2)
        elif file == "p16-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (245, 445), 58, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (245, 445), 58, (0,0,255), 2)
        elif file == "p17-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (219, 503), 64, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (219, 503), 64, (0,0,255), 2)
        elif file == "p18-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (709, 70), 32, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (709, 70), 32, (0,0,255), 2)
        elif file == "p19-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (729, 93), 24, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (729, 93), 24, (0,0,255), 2)
        elif file == "p20-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (732, 103), 24, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (732, 103), 24, (0,0,255), 2)
        elif file == "p21-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (734, 119), 24, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (734, 119), 24, (0,0,255), 2)
        elif file == "p22-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (736, 143), 24, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (736, 143), 24, (0,0,255), 2)
        elif file == "p23-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (743, 158), 24, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (743, 158), 24, (0,0,255), 2)
        elif file == "p24-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (745, 171), 33, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (745, 171), 33, (0,0,255), 2)
        elif file == "p25-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (759, 189), 33, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (759, 189), 33, (0,0,255), 2)
        elif file == "p26-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (771, 214), 44, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (771, 214), 44, (0,0,255), 2)
        elif file == "p27-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (776, 251), 50, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (776, 251), 50, (0,0,255), 2)
        elif file == "p28-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (799, 277), 55, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (799, 277), 55, (0,0,255), 2)
        elif file == "p29-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (815, 317), 55, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (815, 317), 55, (0,0,255), 2)
        elif file == "p30-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (828, 355), 55, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (828, 355), 55, (0,0,255), 2)
        elif file == "p31-1.jpg":
            if vac_prob > occ_prob:
                cv2.circle(lot_image, (845, 412), 55, (0,255,0), 2)
            else:
                cv2.circle(lot_image, (845, 412), 55, (0,0,255), 2)
        else:      
            raise ValueError('THERE WAS A .JPG WITH A WRONG NAME')

cv2.imshow('image',lot_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

