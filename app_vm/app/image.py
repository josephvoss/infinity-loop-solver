import cv2
import numpy as np
import glob

#import objects.py

"""
Image detector functions

Tasks completed
    Init object
    Capture Image
    Identify different shapes
    Populate data in object and output
"""

img_color = cv2.imread("/home/joseph/scratch/CV/app_vm/data/screenshot.png")
img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
img_gray = cv2.Canny(img_gray,50,200)
templates = []
for i,item in enumerate(glob.glob("/home/joseph/scratch/CV/app_vm/data/templates/inf_loop_*.png")):
    print item
    templates.append(cv2.imread(item))
    templates[i] = cv2.cvtColor(templates[i], cv2.COLOR_BGR2GRAY)
    templates[i] = cv2.Canny(templates[i],50,200)
    w,h = templates[i].shape[::-1]
    res = cv2.matchTemplate(img_gray, templates[i], cv2.TM_CCOEFF_NORMED)
    shape_type = int(item.split('/')[-1].split('_')[2])
    print shape_type
    if shape_type == 1:
        thresh = 0.8
    elif shape_type == 2:
        thresh = 0.7
    elif shape_type == 3:
        thresh = 1
    elif shape_type == 4:
        thresh = 0.8
    elif shape_type == 5:
        thresh = 0.8
    else:
        thresh = 1
    loc = np.where(res >= thresh)
    print len(loc[0])
    img_color_temp = np.copy(img_color)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_color_temp, pt, (pt[0]+w, pt[1]+h),(0,0,255),2)
    window_name='out_'+item.split('/')[-1]
    cv2.namedWindow(window_name,cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name,400,600)
    cv2.imshow(window_name, img_color_temp)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
