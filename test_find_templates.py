#!/usr/bin/python2
import cv2
import numpy as np
from matplotlib import pyplot as plt
import os

img_color = cv2.imread("/home/joseph/Pictures/kfmIkJC.png")

img_gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
templates = []
for i,item in enumerate(os.listdir("/home/joseph/scratch/CV/templates")):
    print item
    templates.append(cv2.imread("/home/joseph/scratch/CV/templates/"+item))
    templates[i] = cv2.cvtColor(templates[i], cv2.COLOR_BGR2GRAY)
    w,h = templates[i].shape[::-1]
    res = cv2.matchTemplate(img_gray, templates[i], cv2.TM_CCOEFF_NORMED)
    thresh = 0.7
    loc = np.where( res >= thresh)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(img_color, pt, (pt[0]+w, pt[1]+h),(0,0,255),2)
    cv2.imwrite('out_'+item, img_color)
