from os import listdir
from os.path import isfile, join
import numpy
import cv2
import sys

# DELETE .DS-STORE in dataset folder if issues with first file in array

mypath='pictures'
onlyfiles = [ f for f in sorted(listdir(mypath)) if isfile(join(mypath,f)) ]
images = numpy.empty(len(onlyfiles), dtype=object)
for n in range(0, len(onlyfiles)):
  images[n] = cv2.imread( join(mypath,onlyfiles[n]) )


count = 0
for image in images:
    count += 1
    p1 = image[88:110, 480:502]
	p2 = image[101:123, 476:498]
	p3 = image[113:135, 469:491]
	p4 = image[122:144, 460:482]
	p5 = image[137:164, 445:472]
	p6 = image[155:182, 451:478]
	p7 = image[170:197, 436:463]
	p8 = image[183:218, 414:449]
	p9 = image[208:243, 399:434]
	p10 = image[230:271, 381:422]
	p11 = image[255:296, 375:416]
	p12 = image[287:328, 357:398]
	p13 = image[311:359, 328:376]
	p14 = image[357:412, 300:355]
	p15 = image[399:454, 276:331]
	p16 = image[445:503, 245:303]
	p17 = image[503:567, 219:283]
	p18 = image[70:102, 709:741]
	p19 = image[93:117, 729:753]
	p20 = image[103:127, 732:756]
	p21 = image[119:143, 734:758]
	p22 = image[143:167, 736:760]
	p23 = image[158:182, 743:767]
	p24 = image[171:204, 745:778]
	p25 = image[189:222, 759:792]
	p26 = image[214:258, 771:815]
	p27 = image[251:301, 776:826]
	p28 = image[277:332, 799:854]
	p29 = image[317:372, 815:870]
	p30 = image[355:410, 828:883]
	p31 = image[412:467, 845:900]
    #cv2.imshow("ps1", ps1)
    cv2.imwrite("p1-" + str(count) + ".jpg", p1);
	cv2.imwrite("p2-" + str(count) + ".jpg", p2);
	cv2.imwrite("p3-" + str(count) + ".jpg", p3);
	cv2.imwrite("p4-" + str(count) + ".jpg", p4);
	cv2.imwrite("p5-" + str(count) + ".jpg", p5);
	cv2.imwrite("p6-" + str(count) + ".jpg", p6);
	cv2.imwrite("p7-" + str(count) + ".jpg", p7);
	cv2.imwrite("p8-" + str(count) + ".jpg", p8);
	cv2.imwrite("p9-" + str(count) + ".jpg", p9);
	cv2.imwrite("p10-" + str(count) + ".jpg", p10);
	cv2.imwrite("p11-" + str(count) + ".jpg", p11);
	cv2.imwrite("p12-" + str(count) + ".jpg", p12);
	cv2.imwrite("p13-" + str(count) + ".jpg", p13);
	cv2.imwrite("p14-" + str(count) + ".jpg", p14);
	cv2.imwrite("p15-" + str(count) + ".jpg", p15);
	cv2.imwrite("p16-" + str(count) + ".jpg", p16);
	cv2.imwrite("p17-" + str(count) + ".jpg", p17);
	cv2.imwrite("p18-" + str(count) + ".jpg", p18);
	cv2.imwrite("p19-" + str(count) + ".jpg", p19);
	cv2.imwrite("p20-" + str(count) + ".jpg", p20);
	cv2.imwrite("p21-" + str(count) + ".jpg", p21);
	cv2.imwrite("p22-" + str(count) + ".jpg", p22);
	cv2.imwrite("p23-" + str(count) + ".jpg", p23);
	cv2.imwrite("p24-" + str(count) + ".jpg", p24);
	cv2.imwrite("p25-" + str(count) + ".jpg", p25);
	cv2.imwrite("p26-" + str(count) + ".jpg", p26);
	cv2.imwrite("p27-" + str(count) + ".jpg", p27);
	cv2.imwrite("p28-" + str(count) + ".jpg", p28);
	cv2.imwrite("p29-" + str(count) + ".jpg", p29);
	cv2.imwrite("p30-" + str(count) + ".jpg", p30);
	cv2.imwrite("p31-" + str(count) + ".jpg", p31);

cv2.destroyAllWindows()


